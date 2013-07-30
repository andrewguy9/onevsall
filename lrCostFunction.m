function [J, grad] = lrCostFunction(theta, X, y, lambda)
%LRCOSTFUNCTION Compute cost and gradient for logistic regression with
%regularization
%   J = LRCOSTFUNCTION(theta, X, y, lambda) computes the cost of using
%   theta as the parameter for regularized logistic regression and the
%   gradient of the cost w.r.t. to the parameters.

% Initialize some useful values
m = length(y); % number of training examples
n = size(theta); % number of features.

% You need to return the following variables correctly
J = 0;
grad = zeros(size(theta));

% ====================== YOUR CODE HERE ======================
% Instructions: Compute the cost of a particular choice of theta.
%               You should set J to the cost.
%               Compute the partial derivatives and set grad to the partial
%               derivatives of the cost w.r.t. each parameter in theta
%
% Hint: The computation of the cost function and gradients can be
%       efficiently vectorized. For example, consider the computation
%
%           sigmoid(X * theta)
%
%       Each row of the resulting matrix will contain the value of the
%       prediction for that example. You can make use of this to vectorize
%       the cost function and gradient computations.
%
% Hint: When computing the gradient of the regularized cost function,
%       there're many possible vectorized solutions, but one solution
%       looks like:
%           grad = (unregularized gradient for logistic regression)
%           temp = theta;
%           temp(1) = 0;   % because we don't add anything for j = 0
%           grad = grad + YOUR_CODE_HERE (using the temp variable)
%

theta;

sizeof_y = size(y);

z = X * theta;
sizeof_z = size(z);

h = sigmoid(z);
sizeof_h = size(h);

first = (-y' * log(h));
sizeof_first = size(first);

second = (1-y')*log(1-h);
sizeof_second = size(second);

J_raw = (first - second)/m;

thetas = theta(2:n,:);
thetas_sq = thetas .^ 2;
theta_cost = (lambda/ (2*m) ) * sum(thetas_sq);

J = J_raw + theta_cost;


errs = (h - y);
sizeof_errs = size(errs);

for dim = 1:n
  dim_errs = errs .* X(:,dim);
  sizeof_dim_err = size(dim_errs);

  total_err = sum(dim_errs) / m;
  sizeof_total_err = size(total_err);

  grad(dim) = total_err;
end

dim_cost = (lambda / m) .* theta;
dim_cost(1) = 0;
sizeof_dim_cost = size(dim_cost);

grad = grad + dim_cost;

% =============================================================

% grad = grad(:);

end
