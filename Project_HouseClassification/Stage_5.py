import os
import requests
import sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import OrdinalEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from category_encoders import TargetEncoder

if __name__ == '__main__':
    if not os.path.exists('../Data'):
        os.mkdir('../Data')

    # Download data if it is unavailable.
    if 'house_class.csv' not in os.listdir('../Data'):
        sys.stderr.write("[INFO] Dataset is loading.\n")
        url = "https://www.dropbox.com/s/7vjkrlggmvr5bc1/house_class.csv?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/house_class.csv', 'wb').write(r.content)
        sys.stderr.write("[INFO] Loaded.\n")

    # write your code here
    houses = pd.read_csv('../Data/house_class.csv')

    ## Stage 1
    #print(houses.head(5))
    #print(houses.shape[0])
    #print(houses.shape[1])
    #print(houses.isnull().values.any())
    #print(houses.loc[:,['Room']].max().item())
    #print(round(houses.loc[:, ['Area']].mean().item(),1))
    #print(houses.loc[:, ['Zip_loc']].nunique().item())

    ## Stage 2
    X = houses.loc[:, ['Area','Room','Lon','Lat','Zip_area','Zip_loc']]
    y = houses.loc[:, ['Price']]

    X_train, X_test, y_train, y_test = \
        train_test_split(X, y,
                         stratify=X['Zip_loc'].values,
                         train_size=0.7, random_state=1)

    #print(X_test[:,5])
    #val, count = np.unique(X_train[:,5], return_counts=True)
    #d = dict(zip(val, count))

    #converted = str()
    #for key in d:
    #    converted += '"' + key + '": ' + str(d[key]) + ', '
    #converted = '{' + converted + '}'
    #print(converted)

    ## Stage 5
    #print(type(X_train))
    #X_train = pd.DataFrame(X_train, columns=X.columns)
    #X_test = pd.DataFrame(X_test, columns=X.columns)
    #y_train = pd.DataFrame(y_train, columns=y.columns)
    #y_test = pd.DataFrame(y_test, columns=y.columns)
    #print(type(X_train))

    #enc = OneHotEncoder(drop='first')
    enc = TargetEncoder(cols=['Zip_area', 'Room', 'Zip_loc'])
    enc.fit(X_train[['Zip_area', 'Room', 'Zip_loc']], y_train)

    #print(enc.transform(X_train[['Zip_area', 'Zip_loc', 'Room']]).toarray())
    #X_train_transformed = pd.DataFrame(enc.transform(X_train[['Zip_area', 'Zip_loc', 'Room']]).toarray(),
    #                                   index=X_train.index)
    X_train_transformed = pd.DataFrame(enc.transform(X_train[['Zip_area', 'Room', 'Zip_loc']]),
                                       index=X_train.index)
    X_train_final = X_train[['Area', 'Lon', 'Lat']].join(X_train_transformed)
    #print(X_train_final)

    #X_test_transformed = pd.DataFrame(enc.transform(X_test[['Zip_area', 'Zip_loc', 'Room']]).toarray(),
    #                                   index=X_test.index)
    X_test_transformed = pd.DataFrame(enc.transform(X_test[['Zip_area', 'Room', 'Zip_loc']]),
                                       index=X_test.index)
    X_test_final = X_test[['Area', 'Lon', 'Lat']].join(X_test_transformed)
    #print(X_test_final)

    dtree = DecisionTreeClassifier(criterion='entropy', max_features=3, splitter='best', max_depth=6, min_samples_split=4, random_state=3)
    dtree.fit(X_train_final.values, y_train.values)
    y_pred = dtree.predict(X_test_final.values)
    print(accuracy_score(y_test, y_pred))
