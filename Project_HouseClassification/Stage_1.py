import os
import requests
import sys
import pandas as pd

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
    #print(houses.head(5))
    print(houses.shape[0])
    print(houses.shape[1])
    print(houses.isnull().values.any())
    print(houses.loc[:,['Room']].max().item())
    print(round(houses.loc[:, ['Area']].mean().item(),1))
    print(houses.loc[:, ['Zip_loc']].nunique().item())
