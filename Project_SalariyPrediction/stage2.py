import os
import requests
import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_percentage_error as mape

## Linear regression with predictor transformation
## On the scatterplot of rating vs salary, you may have noticed
## that the relationship between these two variables seems to
## be different from linear and looks like a polynomial function.
## Let's try to raise the rating by several degrees (2, 3, 4)
## and see whether it improves the score.
## Print the best MAPE obtained by fitting and running the models described above.
## The MAPE is a float number rounded to five decimal places.

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
X, y = data.iloc[:, :1], data["salary"]
X2, y = pow(data.iloc[:, :1],2), data["salary"]
X3, y = pow(data.iloc[:, :1],3), data["salary"]
X4, y = pow(data.iloc[:, :1],4), data["salary"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=100)
X2_train, X2_test = train_test_split(X2, test_size=0.3, random_state=100)
X3_train, X3_test = train_test_split(X3, test_size=0.3, random_state=100)
X4_train, X4_test = train_test_split(X4, test_size=0.3, random_state=100)

# print(y_train)
# print(X_train)
# print(y_test)
# print(X_test)

## model fitting end evaluation
model = LinearRegression()
model.fit(X_train, y_train)
result_coef = model.coef_
result_intercept = model.intercept_
y_test_pred = model.predict(X_test)
result_mape = mape(y_test, y_test_pred)

model2 = LinearRegression()
model2.fit(X2_train, y_train)
result2_coef = model2.coef_
result2_intercept = model2.intercept_
y_test2_pred = model2.predict(X2_test)
result2_mape = mape(y_test, y_test2_pred)

model3 = LinearRegression()
model3.fit(X3_train, y_train)
result3_coef = model3.coef_
result3_intercept = model3.intercept_
y_test3_pred = model3.predict(X3_test)
result3_mape = mape(y_test, y_test3_pred)

model4 = LinearRegression()
model4.fit(X4_train, y_train)
result4_coef = model4.coef_
result4_intercept = model4.intercept_
y_test4_pred = model4.predict(X4_test)
result4_mape = mape(y_test, y_test4_pred)

## output
#print("{} {} {}".format(round(result_intercept, 5),
#                        round(result_coef[0], 5),
#                        round(result_mape, 5)))

print(round(min([result_mape, result2_mape,result3_mape,result4_mape]),5))
