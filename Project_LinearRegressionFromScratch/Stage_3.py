import math
import numpy as np

class CustomLinearRegression:

    def __init__(self, *, fit_intercept=True):
        self.fit_intercept = fit_intercept
        self.coefficient = []
        self.intercept = []
        self.solution = []
        self.r2 = []
        self.rmse = []

    def fit(self, X, y):
        if self.fit_intercept:
            X = np.column_stack((np.ones(len(X)), X))
        Xt = np.transpose(X)
        a = np.dot(Xt, y)
        b = np.dot(Xt, X)
        solution = np.dot(np.linalg.inv(b), a)
        if self.fit_intercept:
            self.solution = solution
            self.intercept = solution[0]
            self.coefficient = solution[1:]
        else:
            self.solution = solution
            self.coefficient = solution

    def predict(self, X):
        if self.fit_intercept:
            X = np.column_stack((np.ones(len(X)), X))
        return np.dot(X, self.solution)

    def r2_score(self, y, yhat):
        ssres = 0
        sstot = 0
        ymean = np.sum(y) / len(y)
        for (i, yi) in enumerate(y):
            ssres += pow(yi - yhat[i], 2)
            sstot += pow(yi - ymean, 2)
        self.r2 = 1 - (ssres / sstot)

    def rmse_score(self, y, yhat):
        mse = 0
        for (i, yi) in enumerate(y):
            mse += pow(yi - yhat[i], 2)
        mse = mse / len(y)
        self.rmse = math.sqrt(mse)

capacity = [0.9, 0.5, 1.75, 2.0, 1.4, 1.5, 3.0, 1.1, 2.6, 1.9]
age = [11, 11, 9, 8, 7, 7, 6, 5, 5, 4]
cost_per_ton = [21.95, 27.18, 16.9, 15.37, 16.03, 18.15, 14.22, 18.72, 15.4, 14.69]

y = cost_per_ton

X = np.array([capacity, age]).T
y = np.array(y)

lr = CustomLinearRegression(fit_intercept=True)
lr.fit(X, y)

yhat = lr.predict(X)
#print(yhat)

lr.rmse_score(y, yhat)
lr.r2_score(y, yhat)

if (lr.fit_intercept == True):
    result = {'Intercept': lr.intercept,
              'Coefficient': lr.coefficient,
              'R2': lr.r2,
              'RMSE': lr.rmse}
else:
    result = {'Coefficient': lr.coefficient,
              'R2': lr.r2,
              'RMSE': lr.rmse}

print(result)
