import os
import requests
#import numpy as np
import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_percentage_error as mape

## A linear model may predict negative values. However, such 
## values can be meaningless because the salary can't be negative. 
## In this stage, handle negative predictions.

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
#print(data.corr())

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

#print(*result_coef, sep=",")

model1 = LinearRegression()
model1.fit(X_train.iloc[:, X_train.columns != "rating"], y_train)
y_pred1 = model1.predict(X_test.iloc[:, X_train.columns != "rating"])
result1_mape = mape(y_test, y_pred1)

model2 = LinearRegression()
model2.fit(X_train.iloc[:, X_train.columns != "age"], y_train)
y_pred2 = model2.predict(X_test.iloc[:, X_train.columns != "age"])
result2_mape = mape(y_test, y_pred2)

model3 = LinearRegression()
model3.fit(X_train.iloc[:, X_train.columns != "experience"], y_train)
y_pred3 = model3.predict(X_test.iloc[:, X_train.columns != "experience"])
result3_mape = mape(y_test, y_pred3)

model4 = LinearRegression()
model4.fit(X_train.loc[:, ['draft_round','experience','bmi']], y_train)
y_pred4 = model4.predict(X_test.loc[:, ['draft_round','experience','bmi']])
result4_mape = mape(y_test, y_pred4)

model5 = LinearRegression()
model5.fit(X_train.loc[:, ['rating','draft_round','bmi']], y_train)
y_pred5 = model5.predict(X_test.loc[:, ['rating','draft_round','bmi']])
result5_mape = mape(y_test, y_pred5)

model6 = LinearRegression()
model6.fit(X_train.loc[:, ['draft_round','age','bmi']], y_train)
y_pred6 = model6.predict(X_test.loc[:, ['draft_round','age','bmi']])
result6_mape = mape(y_test, y_pred6)

#print(result_mape)
#print(result1_mape)
#print(result2_mape)
#print(result3_mape)
#print(result4_mape)
#print(result5_mape)
#print(result6_mape)

## output
#print("{} {} {}".format(round(result_intercept, 5),
#                        round(result_coef[0], 5),
#                        round(result_mape, 5)))

result5_df = pd.DataFrame(y_pred5, columns=['residual'])
#print(result5_df)

y_pred5_0 = result5_df.copy()
y_pred5_med = result5_df.copy()
y_pred5_0.loc[y_pred5_0["residual"] < 0, "residual"] = 0
y_pred5_med.loc[y_pred5_med["residual"] < 0, "residual"] = y_train.median()

y_pred5_0_mape = mape(y_test, y_pred5_0)
y_pred5_med_mape = mape(y_test, y_pred5_med)

#print(y_pred5_0_mape)
#print(y_pred5_med_mape)

print(round(min([y_pred5_0_mape,y_pred5_med_mape]),5))
