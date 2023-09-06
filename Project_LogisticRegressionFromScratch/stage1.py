import numpy as np
import pandas as pd
import math
from sklearn import datasets
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

coeficients = [0.77001597, -2.12842434, -2.39305793]

class CustomLogisticRegression:

    def __init__(self, fit_intercept=True, l_rate=0.01, n_epoch=100):
        self.fit_intercept = fit_intercept
        self.l_rate = l_rate
        self.n_epoch = n_epoch

    def sigmoid(self, t):
        return 1 / (1 + math.exp(-t))

    def predict_proba(self, row, coef_):
        #print(row)
        #print(coef_)
        t = coef_[0]
        for i in range(1, len(coef_)):
            t += coef_[i] * row[i-1]
        #print(t)
        return self.sigmoid(t)

data = datasets.load_breast_cancer()
X = pd.DataFrame(data.data, columns=data.feature_names)
X = X.loc[:,['worst concave points','worst perimeter']]
y = data['target']

#print(X)
#print(y)

scale= StandardScaler()
scaled_X = pd.DataFrame(scale.fit_transform(X),
                        columns=['worst concave points','worst perimeter'])
#print(scaled_X)

X_train, X_test, y_train, y_test = train_test_split(scaled_X, y, train_size=0.8, random_state=43)
#print(X_train)
#print(X_test)
#print(y_train)
#print(y_test)

result = []

for j in range(0,10):
    #print(X.iloc[j,:])
    clr = CustomLogisticRegression()
    prediction = clr.predict_proba(row = X_test.iloc[j,:], coef_ = coeficients)
    #print(prediction)
    result.append(prediction)

print(result)
