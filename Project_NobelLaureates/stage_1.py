import pandas as pd
import os
import requests
import sys
import json



if __name__ == '__main__':
    if not os.path.exists('../Data'):
        os.mkdir('../Data')

    # Download data if it is unavailable.
    if 'Nobel_laureates.json' not in os.listdir('../Data'):
        sys.stderr.write("[INFO] Dataset is loading.\n")
        url = "https://www.dropbox.com/s/m6ld4vaq2sz3ovd/nobel_laureates.json?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/Nobel_laureates.json', 'wb').write(r.content)
        sys.stderr.write("[INFO] Loaded.\n")

    data = pd.read_json('../Data/Nobel_laureates.json')
    #print(data.info())
    print(len(data[data.duplicated()]) > 0)
    data.dropna(subset='gender', inplace=True)
    data.reset_index(drop=True, inplace=True)
    print(data[:20][['country','name']].to_dict())
