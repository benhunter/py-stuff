# Multi-Output Regression Models
# https://machinelearningmastery.com/multi-output-regression-models-with-python/


import sklearn
print(sklearn.__version__)

from sklearn.datasets import make_regression

data_in = [[-2.02220122, 0.31563495, 0.82797464, -0.30620401, 0.16003707, -1.44411381, 0.87616892, -0.50446586, 0.23009474, 0.76201118]]

# create datasets
X, y = make_regression(n_samples=1000, n_features=10, n_informative=5, n_targets=2, random_state=1)
# summarize dataset
print(X.shape, y.shape)

# Multioutput Regression Algorithms in scikit-learn
#   LinearRegression (and related)
#   KNeighborsRegressor
#   DecisionTreeRegressor
#   RandomForestRegressor (and related)

# Linear Regression
from sklearn.linear_model import LinearRegression
# define model
model = LinearRegression()
# fit model
model.fit(X, y)
# make a prediction
yhat = model.predict(data_in)
# summarize prediction
print("Linear Regression")
print(yhat[0])


# K-Nearest Neighbors for Multioutput Regression
from sklearn.neighbors import KNeighborsRegressor
# define model
model = KNeighborsRegressor()
# fit model
model.fit(X, y)
# predict
yhat = model.predict(data_in)
# summarize prediction
print("K-Nearest Neighbors")
print(yhat[0])


# Random Forest
from sklearn.ensemble import RandomForestRegressor
# define model
model = RandomForestRegressor()
# fit model
model.fit(X, y)
# predict
yhat = model.predict(data_in)
# summarize prediction
print("Random Forest")
print(yhat[0])


# Evaluate Multioutput Regression with K-Fold Cross-Validation
# against Decision Tree Regressor model
from numpy import absolute
from numpy import mean
from numpy import std
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedKFold
# define model
model = DecisionTreeRegressor()
# fit model
model.fit(X, y)
# evaluate model
cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)
n_scores = cross_val_score(model, X, y, scoring='neg_mean_absolute_error', cv=cv, n_jobs=-1, error_score='raise')
# summarize performance
n_scores = absolute(n_scores)
print(f'Result: {mean(n_scores):.3f}, ({std(n_scores):.3f})')


# Wrapper for algorithms that don't support Multi-Output Regression
# Support Vector Machine
from sklearn.svm import LinearSVR
model = LinearSVR()

# Won't work:
# model.fit(X, y)  # Exception! ValueError, bad input shape

# Option 1: MultiOutput Regressor. Create seperate model for each output.
# Works well if outputs are independent or mostly independent
from sklearn.multioutput import MultiOutputRegressor
wrapper = MultiOutputRegressor(model)
# fit model
wrapper.fit(X, y)
# predict
yhat = wrapper.predict(data_in)
print('MultiOutputRegressor with Support Vector Regressor Model')
print(yhat[0])

# Option 2: RegressorChain
from sklearn.multioutput import RegressorChain
model = LinearSVR()
wrapper = RegressorChain(model)  # define chain order here
wrapper.fit(X, y)
yhat = wrapper.predict(data_in)
print('RegressorChain with Support Vector Regressor Model')
print(yhat[0])
