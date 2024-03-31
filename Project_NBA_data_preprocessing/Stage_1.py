import pandas as pd
import re
import os
import requests

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

df = clean_data(data_path)
print(df[['b_day', 'team', 'height', 'weight', 'country', 'draft_round', 'draft_year', 'salary']].head())
