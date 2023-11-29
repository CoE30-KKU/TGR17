% Clear workspaces
clc, clear, close all

% Read the data
h1 = readtable('dataset5.xlsx', 'Sheet', 'Hdata1', 'Range', 'B10:M40');
q1 = readtable('dataset5.xlsx', 'Sheet', 'Qdata1', 'Range', 'B11:M41');
q2 = readtable('dataset5.xlsx', 'Sheet', 'Qdata2', 'Range', 'B11:M41');

% Convert tables to arrays
h1_array = table2array(h1);
q1_array = table2array(q1);
q2_array = table2array(q2);


% Flatten the arrays
h1_flat = h1_array(:);
q1_flat = q1_array(:);
q2_flat = q2_array(:);

% Remove NaN values
h1_flat = h1_flat(~isnan(h1_flat));
q1_flat = q1_flat(~isnan(q1_flat));
q2_flat = q2_flat(~isnan(q2_flat));

% Number of hidden neurons
hiddenLayerSize = 10;  % Adjust as needed

% Create a feedforward neural network
net = fitnet(hiddenLayerSize);

% Configure the division of data into training, validation, and testing sets
net.divideParam.trainRatio = 70/100;
net.divideParam.valRatio = 15/100;
net.divideParam.testRatio = 15/100;

% Train the network
[net, tr] = train(net, h1_flat', q1_flat');

% View the network
view(net)

% Predict outputs
y_nn_est = net(h1_flat');

% Evaluate performance
displayMetrics(q1_flat', y_nn_est);

% Plot original data and NN fit
figure, scatter(h1_flat, q1_flat); hold on;
plot(h1_flat, y_nn_est, 'b-', 'LineWidth', 2);
xlabel('h1');
ylabel('q1');
title('NN Fit to Data');
legend('Data', 'Neural Network Fit');
hold off;

% Function to display metrics
function displayMetrics(y, y_est)
    R_squared = 1 - sum((y - y_est).^2) / sum((y - mean(y)).^2);
    MSE = mean((y - y_est).^2);
    MAE = mean(abs(y - y_est));
    fprintf("R-Squared: %f\n", R_squared)
    fprintf("MSE: %.4f\n", MSE)
    fprintf("MAE: %f\n", MAE)
end




