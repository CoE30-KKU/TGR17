% clear workspace
clc
clearvars
close all

Height_S1 = readtable('dataset-3b.xlsx', 'Sheet', 'Q1A', 'Range', 'B02:F61');
Height_S1 = table2array(Height_S1);

Discharge_S1 = readtable('dataset-3b.xlsx', 'Sheet', 'Q1A', 'Range', 'C02:C61');
Discharge_S1 = table2array(Discharge_S1);

days = readtable('dataset-3b.xlsx', 'Sheet', 'Q1A', 'Range', 'A02:A61');
days = table2array(days);

api_url = 'http://192.168.1.98/waters/';
nameValue = 'M7';

numDataPoints = length(Height_S1);

new_data = [];

for i = 1:numDataPoints
    data_point = struct('day', days(i), 'discharge_rate', Discharge_S1(i), 'height', Height_S1(i), 'name', nameValue);
    new_data = [new_data, data_point];
end

data_to_send = struct('data', new_data);
data_to_send_json = jsonencode(data_to_send);

options = weboptions('RequestMethod', 'post', 'MediaType', 'application/json', 'Timeout', 20)
try
    response = webwrite(api_url, data_to_send_json, options)
    disp('Response from the API:')
    disp(response)
catch ME
    disp('Error occurred:')
    disp(ME.message)
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

% Read the data
Q3B  = readtable('dataset-3b.xlsx', 'Sheet', 'Q1A'  , 'Range', 'A1:F61');
QHS1 = readtable('dataset-3b.xlsx', 'Sheet', 'QH_S1', 'Range', 'A1:B366');

% Do neural network for QH1
H_S1 = QHS1.H_S1;
Q_S1 = QHS1.Q_S1;

% Number of hidden neurons
hiddenLayerSize = 10;  % Adjust as needed

% Create a feedforward neural network
net = fitnet(hiddenLayerSize);

% Configure the division of data into training, validation, and testing sets
net.divideParam.trainRatio = 70/100;
net.divideParam.valRatio = 15/100;
net.divideParam.testRatio = 15/100;

% Train the network
% Note: Transpose H_S1 for training (inputs are row vectors)
[net, tr] = train(net, H_S1', Q_S1');

% Predict outputs
% Note: Transpose H_S1 for prediction
y_nn_est_s1 = net(H_S1');

% Evaluate performance
displayMetrics(Q_S1', y_nn_est_s1);

% Plot original data and NN fit
figure, scatter(H_S1, Q_S1); hold on;
plot(H_S1, y_nn_est_s1, 'b-', 'LineWidth', 2);
xlabel('Dam Height (H_S1)');
ylabel('Discharge Rate (Q_S1)');
title('NN Fit to Data: Predicting Discharge Rate from Dam Height');
legend('Data', 'Neural Network Fit');
hold off;

% Preparing data for prediction
% Assume decoded_data_height contains the heights for prediction
% Transpose it before feeding into the network
decoded_data_height = decoded_data_height(end-4:end)';  % Transpose to row vector

% Predict discharge rates
predicted_Q_S1 = net(decoded_data_height);

% Create table for the predicted discharge rates
discharge_table = array2table(predicted_Q_S1', 'VariableNames', {'Predicted_Discharge'});

% Write the predicted discharge rates to the Excel file
try
    writetable(discharge_table, 'dataset-3b.xlsx', 'Sheet', 'Q1A', 'Range', 'C57:C61', 'WriteVariableNames', false);
    disp('Predicted discharge data written to Excel file successfully.');
catch
    error('Error writing data to Excel file. Check file permissions and try again.');
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
