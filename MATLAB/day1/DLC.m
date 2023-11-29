% Clear workspaces
clc, clear, close all

fileName = "DLC.xlsx";

% Read the data
h1 = readtable(fileName, 'Sheet', 'HM7', 'Range', 'B10:M40');
q1 = readtable(fileName, 'Sheet', 'QM7', 'Range', 'B11:M41');
q2 = readtable(fileName, 'Sheet', 'QE98', 'Range', 'B11:M41');
q3 = readtable(fileName, 'Sheet', 'QM182', 'Range', 'B11:M41');

% Convert tables to arrays
h1_array = table2array(h1);
q1_array = table2array(q1);
q2_array = table2array(q2);
q3_array = table2array(q3);

% Flatten the arrays
h1_flat = h1_array(:);
q1_flat = q1_array(:);
q2_flat = q2_array(:);
q3_flat = q3_array(:);

% Remove NaN values
h1_flat = h1_flat(~isnan(h1_flat));
q1_flat = q1_flat(~isnan(q1_flat));
q2_flat = q2_flat(~isnan(q2_flat));
q3_flat = q3_flat(~isnan(q3_flat));


delta = q3_flat - q1_flat - q2_flat;

bar(delta)

% Start date
startDate = datetime(2015, 4, 1);

% Create time vectors for each data set (assuming they all have the same length for simplicity)
timeVector = startDate + days(0:(length(h1_flat)-1));

% Assuming your data and timeVector are already defined

% Set the StartDate and create time series with time as numeric values
ts_h1 = timeseries(h1_flat, (0:(length(h1_flat)-1)), 'Name', 'Water Level Data');
ts_q1 = timeseries(q1_flat, (0:(length(q1_flat)-1)), 'Name', 'Discharge Rate Q1');
ts_q2 = timeseries(q2_flat, (0:(length(q2_flat)-1)), 'Name', 'Discharge Rate Q2');
ts_q3 = timeseries(q3_flat, (0:(length(q3_flat)-1)), 'Name', 'Discharge Rate Q3');

startDate = datetime(2015, 4, 1);

% Set the StartDate in a recognized format
dateFormat = 'dd-mmm-yyyy'; % Example format
ts_h1.TimeInfo.StartDate = datestr(startDate, dateFormat);
ts_q1.TimeInfo.StartDate = datestr(startDate, dateFormat);
ts_q2.TimeInfo.StartDate = datestr(startDate, dateFormat);
ts_q3.TimeInfo.StartDate = datestr(startDate, dateFormat);


% Time units (daily in this case)
ts_h1.TimeInfo.Units = 'days';
ts_q1.TimeInfo.Units = 'days';
ts_q2.TimeInfo.Units = 'days';
ts_q3.TimeInfo.Units = 'days';

ts_q_delta = ts_q1 - (ts_q2 + ts_q3);

% f = (Q1 + Q2) / Q3
f = (ts_q1 + ts_q2) / ts_q3;

plot(f)




