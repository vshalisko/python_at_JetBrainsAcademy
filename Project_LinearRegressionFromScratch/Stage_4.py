import math
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

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

f1 = [2.31, 7.07, 7.07, 2.18, 2.18, 2.18, 7.87, 7.87, 7.87, 7.87]
f2 = [65.2, 78.9, 61.1, 45.8, 54.2, 58.7, 96.1, 100.0, 85.9, 94.3]
f3 = [15.3, 17.8, 17.8, 18.7, 18.7, 18.7, 15.2, 15.2, 15.2, 15.2]
y = [24.0, 21.6, 34.7, 33.4, 36.2, 28.7, 27.1, 16.5, 18.9, 15.0]

X = np.array([f1, f2, f3]).T
y = np.array(y)

lr = CustomLinearRegression(fit_intercept=True)
lr.fit(X, y)

yhat = lr.predict(X)
#print(yhat)

lr.rmse_score(y, yhat)
lr.r2_score(y, yhat)

regSci = LinearRegression(fit_intercept=True)
regSci.fit(X, y)

yhat2 = regSci.predict(X)
rmse2 = math.sqrt(mean_squared_error(y, yhat2))
r2_2 = r2_score(y, yhat2)

result = {'Intercept': lr.intercept,
              'Coefficient': lr.coefficient,
              'R2': lr.r2,
              'RMSE': lr.rmse}

result2 = {'Intercept': regSci.intercept_,
          'Coefficient': regSci.coef_,
          'R2': r2_2,
          'RMSE': rmse2}

diff = {'Intercept': regSci.intercept_ - lr.intercept,
          'Coefficient': regSci.coef_ - lr.coefficient,
          'R2': r2_2 - lr.r2,
          'RMSE': rmse2 - lr.rmse}

#print(result)
#print(result2)
print(diff)
