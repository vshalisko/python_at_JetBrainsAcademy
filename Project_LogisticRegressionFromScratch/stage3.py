import numpy as np
import pandas as pd
import math
from sklearn import datasets
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

#coeficients = [0.77001597, -2.12842434, -2.39305793]

class CustomLogisticRegression:
    cut_value = 0.5

    def __init__(self, fit_intercept=True, l_rate=0.01, n_epoch=1000):
        self.fit_intercept = fit_intercept
        self.l_rate = l_rate
        self.n_epoch = n_epoch
        self.coef_ = None
        self.epoch = []

    def sigmoid(self, t):
        return 1 / (1 + math.exp(-t))

    def sgd_element(self, yi, yi_hat):
        # Function to modify coeficients in Stochastic gradient descent with MSE
        return self.l_rate * (yi_hat - yi) * yi_hat * (1 - yi_hat)

    def sgd_ll_element(self, yi, yi_hat, N):
        # Function to modify coeficients in Stochastic gradient descent with log-loss
        return self.l_rate * (yi_hat - yi) / N

    def predict_proba(self, row, coef_):
        if self.fit_intercept:
            t = coef_[0]
            for i in range(1, len(coef_)):
                t += coef_[i] * row[i-1]
        else:
            for i in range(0, len(coef_)-1):
                t += coef_[i] * row[i]
        return self.sigmoid(t)

    def fit_mse(self, X_train, y_train):

        # Determining the number of rows and coeficients
        N = len(X_train)
        n_vars = len(X_train.columns.tolist())

        # initialize weights (set all to 0)
        if self.fit_intercept:
            count = n_vars + 1
        else:
            count = n_vars
        self.coef_ = np.zeros(count)

        for _ in range(self.n_epoch):
            #errors = []
            for i in range(N):
                # estimate y_hat with given coefs
                y = y_train[i]
                y_hat = self.predict_proba(X_train.iloc[i,:], self.coef_)

                # update coefs
                if self.fit_intercept:
                    self.coef_[0] = self.coef_[0] - self.sgd_element(y, y_hat)
                    for j in range(0, n_vars):
                        self.coef_[j+1] = (self.coef_[j+1] -
                                         self.sgd_element(y, y_hat) *
                                         X_train.iloc[i,j])
                else:
                    for j in range(0, n_vars):
                        self.coef_[j] = (self.coef_[j] -
                                         self.sgd_element(y, y_hat) *
                                         X_train.iloc[i,j])
            # error = ((y_hat - y) ** 2) / N
            # errors.append(error.item())
            # print(error)
            #self.epoch.append(errors)
            #self.coef_ = coef_
            #print(self.coef_)

    def fit_log_loss(self, X_train, y_train):
        # Stochastic gradient descent implementation with log-loss

        # Determining the number of rows and coeficients
        N = len(X_train)
        n_vars = len(X_train.columns.tolist())

        # initialize weights (set all to 0)
        if self.fit_intercept:
            count = n_vars + 1
        else:
            count = n_vars
        self.coef_ = np.zeros(count)

        for _ in range(self.n_epoch):
            #errors = []
            for i in range(N):
                # estimate y_hat with given coefs
                y = y_train[i]
                y_hat = self.predict_proba(X_train.iloc[i,:], self.coef_)

                # update coefs
                if self.fit_intercept:
                    self.coef_[0] = self.coef_[0] - self.sgd_ll_element(y, y_hat, N)
                    for j in range(0, n_vars):
                        self.coef_[j+1] = (self.coef_[j+1] -
                                         self.sgd_ll_element(y, y_hat, N) *
                                         X_train.iloc[i,j])
                else:
                    for j in range(0, n_vars):
                        self.coef_[j] = (self.coef_[j] -
                                         self.sgd_ll_element(y, y_hat, N) *
                                         X_train.iloc[i,j])

    def predict(self, X_test, cut_off=0.5):
        # predictions are binary values - 0 or 1
        predictions = []
        M = len(X_test)
        for i in range(M):
            y_hat = self.predict_proba(X_test.iloc[i,:], self.coef_)
            predictions.append(y_hat)
        predictions = np.array(predictions)
        predictions[predictions >= cut_off] = 1
        predictions[predictions < cut_off] = 0
        return predictions

data = datasets.load_breast_cancer()
X = pd.DataFrame(data.data, columns=data.feature_names)
X = X.loc[:,['worst concave points','worst perimeter','worst radius']]
y = data['target']

scale = StandardScaler()
scaled_X = pd.DataFrame(scale.fit_transform(X),
                        columns=['worst concave points','worst perimeter','worst radius'])

# Alternative to StandardScaler() method
#X['worst concave points'] = (X['worst concave points'] - X['worst concave points'].mean()) / X['worst concave points'].std()
#X['worst perimeter'] = (X['worst perimeter'] - X['worst perimeter'].mean()) / X['worst perimeter'].std()
#X['worst radius'] = (X['worst radius'] - X['worst radius'].mean()) / X['worst radius'].std()
#scaled_X = X

#print(X)
#print(scaled_X)

X_train, X_test, y_train, y_test = train_test_split(scaled_X, y, train_size=0.8, random_state=43)

#result = []
#for j in range(0,10):
#    #print(X.iloc[j,:])
#    clr = CustomLogisticRegression()
#    prediction = clr.predict_proba(row = X_test.iloc[j,:], coef_ = coeficients)
#    #print(prediction)
#    result.append(prediction)

## result stage 1
#print(result)

# Train model with train dataset
mse_model = CustomLogisticRegression()
mse_model.fit_log_loss(X_train, y_train)

# Test set with test dataset and estimate accuracy
y_hat_test = mse_model.predict(X_test)
acc = accuracy_score(y_test, y_hat_test)

result_coef = mse_model.coef_.tolist()
#d = {'coef_': result_coef, 'accuracy': round(acc, 2)}
d = {'coef_': result_coef, 'accuracy': acc}

## result stage 2
print(d)
