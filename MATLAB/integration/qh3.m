% clear workspace
clc, clearvars, close all

% load dataset
Q3B  = readtable('dataset-3b.xlsx', 'Sheet', 'Q1A'  , 'Range', 'A1:G61');
QHS3 = readtable('dataset-3b.xlsx', 'Sheet', 'QH_S3_FLAG',...
    'Range', 'A1:C366');

% Extract data for QH3
Q_S3 = QHS3.Q_S3; % Assuming Q_S3 is the discharge rate
H_S3 = QHS3.H_S3; % Assuming H_S3 is the height of the dam
FLAG = QHS3.CLEAN_FLAG;

% Find indices where FLAG is 0 (dirty data)
dirtyIdx = find(FLAG == 0);

% Interpolate missing/dirty data
Q_S3(dirtyIdx) = interp1(find(FLAG == 1), Q_S3(FLAG == 1), dirtyIdx, 'linear', 'extrap');
H_S3(dirtyIdx) = interp1(find(FLAG == 1), H_S3(FLAG == 1), dirtyIdx, 'linear', 'extrap');

% Number of hidden neurons
hiddenLayerSize = 10;  % Adjust as needed

% Create a feedforward neural network
net = fitnet(hiddenLayerSize);

% Configure the division of data into training, validation, and testing sets
net.divideParam.trainRatio = 70/100;
net.divideParam.valRatio = 15/100;
net.divideParam.testRatio = 15/100;

% Train the network
[net, tr] = train(net, Q_S3', H_S3');

% Predict outputs
y_nn_est_s3 = net(Q_S3');

displayMetrics(H_S3,y_nn_est_s3')

% Plotting actual data vs. NN fit
figure; % Open a new figure window
scatter(Q_S3, H_S3, 'b', 'DisplayName', 'Actual Data') % Scatter plot of actual data
hold on; % Hold the current plot
plot(Q_S3, y_nn_est_s3', 'r', 'LineWidth', 2, 'DisplayName', 'NN Fit') % Line plot of NN fit
xlabel('Discharge Rate (Q_S3)')
ylabel('Dam Height (H_S3)')
title('Comparison of Actual Data and NN Fit')
legend('show') % Show legend
hold off % Release the plot hold

target_Q_S3 = Q3B.Discharge_S3;
calc_H_S3 = net(target_Q_S3');

H_S3_table = array2table(calc_H_S3', 'VariableNames', {'Height_S3'});
try
    writetable(H_S3_table, fullfile(pwd, 'dataset-3b.xlsx'), 'Sheet', 'Q1A', 'Range', 'F1:F61');
    disp('Data written to Excel file successfully.');
catch
    error('Error writing data to Excel file. Check file permissions and try again.');
end

api_url = 'http://192.168.1.98/rawWater/';

try
    data = webread(api_url);
catch
    error('Error fetching data from the API. Make sure the server is accessible.');
end

disp('Data fetched from the API:');

if ischar(data.data)
    dataString = data.data;
else
    dataString = jsonencode(data.data);
end

decoded_data = jsondecode(dataString);
decoded_data_height = [];

if isfield(decoded_data, 'height')
    for i = 1:numel(decoded_data)
        decoded_data_height = [decoded_data_height; decoded_data(i).height];
    end
    height_table = array2table(decoded_data_height(end-4:end), 'VariableNames', {'Height'});
    try
        writetable(height_table, 'dataset-3b.xlsx', 'Sheet', 'Q1A', 'Range', 'B57:B62', 'WriteVariableNames', false);
        disp('Data written to Excel file successfully.');
    catch
        error('Error writing data to Excel file. Check file permissions and try again.');
    end
else
    disp('The structure does not have a ''height'' field.');
end

Height_S3 = readtable('dataset-3b.xlsx', 'Sheet', 'Q1A', 'Range', 'F02:F61');
Height_S3 = table2array(Height_S3);

Discharge_S3 = readtable('dataset-3b.xlsx', 'Sheet', 'Q1A', 'Range', 'E02:E61');
Discharge_S3 = table2array(Discharge_S3);

days = readtable('dataset-3b.xlsx', 'Sheet', 'Q1A', 'Range', 'A02:A61');
days = table2array(days);

api_url = 'http://192.168.1.98/waters/';
nameValue = 'S3';
numDataPoints = length(Height_S3);

new_data = [];

for i = 1:numDataPoints
    data_point = struct('day', days(i), 'discharge_rate', Discharge_S3(i), 'height', Height_S3(i), 'name', nameValue);
    new_data = [new_data, data_point];
end

data_to_send = struct('data', new_data)
data_to_send_json = jsonencode(data_to_send)
options = weboptions('RequestMethod', 'post', 'MediaType', 'application/json', 'Timeout', 20)
try
    response = webwrite(api_url, data_to_send_json, options)
    disp('Response from the API:')
    disp(response)
catch ME
    disp('Error occurred:')
    disp(ME.message)
end


% Function to display metrics
function displayMetrics(y, y_est)
    R_squared = 1 - sum((y - y_est).^2) / sum((y - mean(y)).^2);
    MSE = mean((y - y_est).^2);
    MAE = mean(abs(y - y_est));
    fprintf("R-Squared: %f\n", R_squared)
    fprintf("MSE: %.8f\n", MSE)
    fprintf("MAE: %.8f\n", MAE)
end
