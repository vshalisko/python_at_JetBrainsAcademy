import os
import requests
import sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

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
    y = houses.loc[:, ['Area','Room','Lon','Lat','Zip_area','Zip_loc']]

    X_train, X_test, y_train, y_test = \
        train_test_split(X.values, y.values,
                         stratify=X['Zip_loc'].values,
                         train_size=0.7, random_state=1)
    #print(X_test[:,5])
    val, count = np.unique(X_train[:,5], return_counts=True)
    d = dict(zip(val, count))

    converted = str()
    for key in d:
        converted += '"' + key + '": ' + str(d[key]) + ', '
    converted = '{' + converted + '}'
    print(converted)
