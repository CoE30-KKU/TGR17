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

% Define the exponential model function using fittype
exponentialModel = fittype('a*exp(b*x)+c', 'independent', 'x', 'dependent', 'y');

% Set up fit options if needed
options = fitoptions(exponentialModel);
options.StartPoint = [1 0.1 0];  % Example starting point for the fitting algorithm

% Perform the fitting for exponential model
[expFitResult, gof] = fit(h1_flat, q1_flat, exponentialModel, options);

% Display the fit coefficients for exponential model
expCoeffValues = coeffvalues(expFitResult);
fprintf("Exponential Fitted equation: %4.6f*exp(%4.6f x) + %4.6f\n\n",...
    expCoeffValues(1),expCoeffValues(2), expCoeffValues(3));

% Estimate y using the exponential fitted model
y_exp_est = expFitResult(h1_flat);

% Display metrics for exponential model
displayMetrics(q1_flat, y_exp_est);

% Perform polynomial fitting
polyDegree = 2; % Degree of the polynomial
[polyCoeffs, S] = polyfit(h1_flat, q1_flat, polyDegree);

% Display the polynomial coefficients
fprintf("\nPolynomial Coefficients (degree %d):\n", polyDegree);
disp(polyCoeffs);

% Estimate y using the polynomial fitted model
y_poly_est = polyval(polyCoeffs, h1_flat);

% Display metrics for polynomial model
displayMetrics(q1_flat, y_poly_est);

% Plot the original data
scatter(h1_flat, q1_flat); hold on;

% Plot the fitted exponential curve
fittedX_exp = linspace(min(h1_flat), max(h1_flat), 200); % Generate points for a smooth curve
fittedY_exp = expFitResult.a * exp(expFitResult.b * fittedX_exp) + expFitResult.c; % Calculate fitted values
plot(fittedX_exp, fittedY_exp, 'r-', 'LineWidth', 2); % Plot the exponential fit

% Plot the fitted polynomial curve
fittedY_poly = polyval(polyCoeffs, fittedX_exp);
plot(fittedX_exp, fittedY_poly, 'g-', 'LineWidth', 2); % Plot the polynomial fit

% Customize the graph
xlabel('h1');
ylabel('q1');
title('Fit to Data');
legend('Data', 'Exponential Fit', 'Polynomial Fit');
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
