import numpy as np

class CustomLinearRegression:

    def __init__(self, *, fit_intercept=True):
        self.fit_intercept = fit_intercept
        self.coefficient = []
        self.intercept = []
        self.prediction = []

    def fit(self, X, y):
        Xt = np.transpose(X)
        a = np.dot(Xt, y)
        b = np.dot(Xt, X)
        solution = np.dot(np.linalg.inv(b), a)
        if self.fit_intercept:
            self.intercept = solution[0]
            self.coefficient = solution[1:]
        else:
            self.coefficient = solution

    def predict(self, X):
        return np.dot(X, self.coefficient)

x = [4, 4.5, 5, 5.5, 6, 6.5, 7]
w = [1, -3, 2, 5, 0, 3, 6]
z = [11, 15, 12, 9, 18, 13, 16]
y = [33, 42, 45, 51, 53, 61, 62]

X = np.array([np.ones(len(x)),x,w,z]).T
y = np.array(y)

lr = CustomLinearRegression(fit_intercept=False)
lr.fit(X[:,1:], y)

#if (lr.fit_intercept == True):
#    result = {'Intercept': lr.intercept,
#              'Coefficient': lr.coefficient}
#else:
#    result = {'Coefficient': lr.coefficient}
#print(result)

yhat = lr.predict(X[:,1:])
print(yhat)
