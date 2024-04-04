import pandas as pd
import re
import os
import requests
import math
import itertools
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder

def flatten(xss):
    return [x for xs in xss for x in xs]

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

def multicol_data(data):
    data_num = data.select_dtypes('number').drop(columns='salary')
    #print(data_num)
    corr_matrix = data_num.corr()
    #print(corr_matrix)
    high_correlation_features = []
    for column1, column2 in itertools.combinations(data_num.columns, 2):
        if corr_matrix[column1][column2] > 0.5 or corr_matrix[column1][column2] < -0.5:
            high_correlation_features.append(column1)
            high_correlation_features.append(column2)

    #print(high_correlation_features)
    stored_correlation = 1
    bad_column = ''
    for column in high_correlation_features:
        current_correlation = data.salary.corr(data[column])
        if stored_correlation > current_correlation:
            stored_correlation = current_correlation
            bad_column = column
    data = data.drop(columns=bad_column)
    return data

def transform_data(data):
    data_num = data.select_dtypes('number').drop(columns='salary')
    scaler = StandardScaler()
    numerical_columns = data_num.select_dtypes(include=['number']).columns.tolist()
    scaler.fit(data[numerical_columns])
    data_matrix = scaler.transform(data_num)
    data_num = pd.DataFrame(data_matrix, columns=data_num.columns.tolist())
    categorical_columns = data.select_dtypes(include=['object']).columns.tolist()
    encoder = OneHotEncoder(sparse_output=False)
    one_hot_encoded = encoder.fit_transform(data[categorical_columns])
    #one_hot_df = pd.DataFrame(one_hot_encoded, columns=encoder.get_feature_names_out(categorical_columns))
    one_hot_df = pd.DataFrame(one_hot_encoded, columns=flatten(encoder.categories_))
    X = pd.concat([data_num, one_hot_df], axis=1)
    y = data['salary']
    return X, y

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
df_featured = feature_data(df_cleaned)
df = multicol_data(df_featured)
#print(list(df.select_dtypes('number').drop(columns='salary')))
X, y = transform_data(df)

answer = {
    'shape': [X.shape, y.shape],
    'features': list(X.columns),
    }
print(answer)
