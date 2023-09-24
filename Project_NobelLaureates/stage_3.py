import pandas as pd
import os
import requests
import sys
import re
import json

def extract_year(date):
    #print(date)
    year = re.findall(r"[0-9]{4,7}", date)[0]
    return(int(year))


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
    #print(len(data[data.duplicated()]) > 0)
    data.dropna(subset='gender', inplace=True)
    data.reset_index(drop=True, inplace=True)
    #data.loc[(data['born_in'] == '') & ~(data['place_of_birth'].isna()),'born_in'] = data.loc[(data['born_in'] == '') & ~(data['place_of_birth'].isna()),'place_of_birth'].str.split(',')

    for i in range(len(data)):
        if ((data.iloc[i,].loc['born_in'] == '' or data.iloc[i,].loc['born_in'] == None) and data.iloc[i,].loc['place_of_birth']):
            new_data_len = len(data.iloc[i,].loc['place_of_birth'].split(','))
            if (new_data_len < 2):
                new_value = ''
            else:
                new_value = data.iloc[i,].loc['place_of_birth'].split(',')[-1].strip()
            #print(str(i) + ' ' + str() + ' ' + new_value)
            data.at[i,'born_in'] = new_value
            data.at[i,'place_of_birth'] = new_value

    data.reset_index(drop=True, inplace=True)
    data['born_in'].replace('', None, inplace=True)
    data['born_in'].replace(['US', 'United States', 'U.S.'], 'USA', inplace=True)
    data['born_in'].replace('United Kingdom', 'UK', inplace=True)
    data.dropna(subset=['born_in'], inplace=True)

    data['year_born'] = data.apply(lambda x: extract_year(x['date_of_birth']), axis=1)

    #print(data['year_born'])
    #data['year_born'] = extract_year(data['date_of_birth'])
    data['age_of_winning'] = data['year'] - data['year_born']

    #print(data.info())
    #print(data.head(n = 20))
    #print(data[:20][['country','name']].to_dict())
    print(data['year_born'].values.tolist())
    print(data['age_of_winning'].values.tolist())
