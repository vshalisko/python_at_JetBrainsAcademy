import os
import requests
#import numpy as np
import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_percentage_error as mape

## In the previous stages, you used only one independent variable. Now, your task
## is to include other variables into a model.
## Print the model coefficients separated by a comma.

## checking ../Data directory presence
if not os.path.exists('../Data'):
    os.mkdir('../Data')

## download data if it is unavailable
if 'data.csv' not in os.listdir('../Data'):
    url = "https://www.dropbox.com/s/3cml50uv7zm46ly/data.csv?dl=1"
    r = requests.get(url, allow_redirects=True)
    open('../Data/data.csv', 'wb').write(r.content)

## read data
data = pd.read_csv('../Data/data.csv')

# print(data)

## data splitting and variable definition
X, y = data.iloc[:, data.columns != "salary"], data["salary"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=100)

## model fitting end evaluation
model = LinearRegression()
model.fit(X_train, y_train)
result_coef = model.coef_
result_intercept = model.intercept_
y_test_pred = model.predict(X_test)
result_mape = mape(y_test, y_test_pred)

print(*result_coef, sep=",")
## output
#print("{} {} {}".format(round(result_intercept, 5),
#                        round(result_coef[0], 5),
#                        round(result_mape, 5)))

#print(round(min([result_mape, result2_mape,result3_mape,result4_mape]),5))
