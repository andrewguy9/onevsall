args = argv()
items_file = args{1}
theta_file = args{2}
predictions_file = args{3}

load("-text", theta_file)

data = csvread(items_file);
fprintf("Data Dims");
[rows, cols] = size(data)

ids = data(:,  1       ); 
X   = data(:, [2:cols] ); 
[m, n] = size(X);
X = [ones(m, 1) X];

p = predictOneVsAll(theta, X);
size(p)

output = [ids p];
csvwrite(predictions_file, output)
