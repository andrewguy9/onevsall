function [J, grad] = costFunction(theta, X, y)
%COSTFUNCTION Compute cost and gradient for logistic regression
%   J = COSTFUNCTION(theta, X, y) computes the cost of using theta as the
%   parameter for logistic regression and the gradient of the cost
%   w.r.t. to the parameters.

% Initialize some useful values
m = length(y) % number of training examples
n = size(theta) % number of features.

% You need to return the following variables correctly 
J = 0;
grad = zeros(size(theta));

% ====================== YOUR CODE HERE ======================
% Instructions: Compute the cost of a particular choice of theta.
%               You should set J to the cost.
%               Compute the partial derivatives and set grad to the partial
%               derivatives of the cost w.r.t. each parameter in theta
%
% Note: grad should have the same dimensions as theta
%

theta;

sizeof_y = size(y);

z = X * theta;
sizeof_z = size(z)

h = sigmoid(z);
sizeof_h = size(h)

first = (-y' * log(h));
sizeof_first = size(first)

second = (1-y')*log(1-h);
sizeof_second = size(second)

J = (first - second)/m



errs = (h - y);
sizeof_errs = size(errs)

for dim = 1:n
  dim_errs = errs .* X(:,dim);
  sizeof_dim_err = size(dim_errs);

  total_err = sum(dim_errs) / m;
  sizeof_total_err = size(total_err);

  grad(dim) = total_err;
% =============================================================

end
