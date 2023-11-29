% clear workspaces
clc; clearvars; close all;
% read dataset
Q3B = readtable('dataset-3b.xlsx', 'Sheet', 'Q1A', 'Range', 'A1:G61');

% extract time series data (dam height @ s1)
H1 = Q3B.Height_S1;

H1_last5 = H1(end-4:end);  % Last 5 values
H1_last5 = H1_last5(:)';   % Ensure it's a row vector

% Assuming no prior knowledge of delay states, initializing with zeros
xi1 = zeros(1, 2);

% inference
[y1_forecast, ~] = ts_nn_h_s1(H1_last5, xi1);

% Plotting original data
figure;
plot(H1, 'b-o');
hold on;

% Plotting forecasted values
forecastIndex = length(H1) + (1:length(y1_forecast));
plot(forecastIndex, y1_forecast, 'g-x');

% Enhancing the plot
title('Height Forecasting');
xlabel('Time Step');
ylabel('Height');
legend('Original Data', 'Forecasted Values');
grid on;

% Only compare the last 5 actual values with the forecasted values
actual_last5 = H1(end-4:end);

% Compute the Metrics
R_squared = 1 - sum((actual_last5 - y1_forecast').^2) / sum((actual_last5 - mean(actual_last5)).^2);
MSE = mean((actual_last5 - y1_forecast').^2);
MAE = mean(abs(actual_last5 - y1_forecast'));

disp('Forecasted Values:');
disp(y1_forecast);


% begin convert to discharge by train NN and calculate discharge
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

% Predict discharge rates
predicted_Q_S1 = net(y1_forecast);
disp("Calculated Discharge Value")
disp(predicted_Q_S1)

api_url = 'http://192.168.1.98/predictWater/';

name = 'M7';

for i = 1:5
    day = 60 + i;
    Predict_height = y1_forecast(i);
    Predict_discharge = predicted_Q_S1(i);
    data_to_send = struct('day', day, 'discharge_rate', Predict_discharge, 'height', Predict_height, 'name', name);
    data_to_send_json = jsonencode(data_to_send);
    options = weboptions('RequestMethod', 'post', 'MediaType', 'application/json', 'Timeout', 20);
    try
        response = webwrite(api_url, data_to_send_json, options);
        disp('Response from the API:')
        disp(response)
    catch ME
        disp('Error occurred:')
        disp(ME.message)
    end
end


