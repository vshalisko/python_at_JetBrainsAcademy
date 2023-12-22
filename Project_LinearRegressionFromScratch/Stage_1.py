import numpy as np

class CustomLinearRegression:

    def __init__(self, *, fit_intercept=True):

        self.fit_intercept = fit_intercept
        self.coefficient = []
        self.intercept = []

    def fit(self, X, y):
        Xt = np.transpose(X)
        a = np.dot(Xt, y)
        b = np.dot(Xt, X)
        solution = np.dot(np.linalg.inv(b), a)
        self.intercept = solution[-1]
        self.coefficient = solution[0:-1]
        if (self.fit_intercept == True):
            result = {'Intercept': self.intercept,
                      'Coefficient': self.coefficient}
        else:
            result = {'Coefficient': self.coefficient}
        return(result)

x = [4.0, 4.5, 5, 5.5, 6.0, 6.5, 7.0]
y = [33, 42, 45, 51, 53, 61, 62]

X = np.array([x,np.ones(7)]).T
y = np.array(y)

lr = CustomLinearRegression(fit_intercept=True)
print(lr.fit(X, y))
