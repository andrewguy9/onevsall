args = argv()
data_file = args{1}
num_labels = str2num(args{2})
max_iter = str2num(args{3})
theta_file = args{4}

data = csvread(data_file);
fprintf("Data Dims");
[rows, cols] = size(data)

ids = data(:,  1       ); 
y   = data(:,  2       ); 
X   = data(:, [3:cols] ); 
[m, n] = size(X);
X = [ones(m, 1) X];

lambda = 0.1;
lambda
[theta] = oneVsAll(X, y, num_labels, lambda, max_iter)

save("-text", theta_file, "theta")
