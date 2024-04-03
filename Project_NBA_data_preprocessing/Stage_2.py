import pandas as pd
import re
import os
import requests
import math

def clean_data(path):
    data = pd.read_csv(path)
    data['b_day'] = pd.to_datetime(data['b_day'], format='%m/%d/%y')
    data['draft_year'] = pd.to_datetime(data['draft_year'], format='%Y')
    data.fillna({'team': 'No Team'}, inplace=True)
    data.loc[data['country'] != 'USA', 'country'] = 'Not-USA'
    data.loc[data['draft_round'] == 'Undrafted', 'draft_round'] = '0'
    data['height'] = data['height'].apply(lambda x: re.sub(r'^\d+-\d+\s+/\s+', '', str(x)))
    data['height'] = data['height'].astype('float')
    data['weight'] = data['weight'].apply(lambda x: re.sub(r'^\d+\s+lbs\.\s+/\s+', '', str(x)))
    data['weight'] = data['weight'].apply(lambda x: re.sub(r'\s+kg\.$', '', str(x)))
    data['weight'] = data['weight'].astype('float')
    data['salary'] = data['salary'].str.replace('$', '')
    data["salary"] = data["salary"].astype('float')
    return data

def drop_high_cardinality(data):
    high_cardinality_features = []
    for column in data.columns:
        if len(data[column].unique()) > 50:
            if data[column].dtype == object:
                high_cardinality_features.append(column)
    data.drop(high_cardinality_features, axis=1, inplace=True)
    return data

def feature_data(data):
    data.loc[data['version'] == 'NBA2k20', 'version'] = '2020'
    data.loc[data['version'] == 'NBA2k21', 'version'] = '2021'
    data['version'] = pd.to_datetime(data['version'], format='%Y')
    data['age'] = (data['version'] - data['b_day']).dt.days / 365
    data['age'] = data['age'].apply(lambda x: math.ceil(x))
    data['experience'] = (data['version'] - data['draft_year']).dt.days / 365
    data['experience'] = data['experience'].apply(lambda x: round(x))
    data['bmi'] = data['weight'] / data['height']**2
    data.drop(columns=['version', 'b_day', 'draft_year', 'weight', 'height'], inplace=True)
    data = drop_high_cardinality(data)
    return data

# Checking ../Data directory presence
if not os.path.exists('../Data'):
    os.mkdir('../Data')

# Download data if it is unavailable.
if 'nba2k-full.csv' not in os.listdir('../Data'):
    print('Train dataset loading.')
    url = "https://www.dropbox.com/s/wmgqf23ugn9sr3b/nba2k-full.csv?dl=1"
    r = requests.get(url, allow_redirects=True)
    open('../Data/nba2k-full.csv', 'wb').write(r.content)
    print('Loaded.')

data_path = "../Data/nba2k-full.csv"
df_cleaned = clean_data(data_path)
#print(df_cleaned[['b_day', 'team', 'height', 'weight', 'country', 'draft_round', 'draft_year', 'salary']].head())

df = feature_data(df_cleaned)

print(df[['age', 'experience', 'bmi']].head())
