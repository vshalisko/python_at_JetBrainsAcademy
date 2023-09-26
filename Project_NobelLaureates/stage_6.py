import pandas as pd
import os
import requests
import sys
import re
import numpy as np
import matplotlib.pyplot as plt


def extract_year(date):
    #print(date)
    year = re.findall(r"[0-9]{4,7}", date)[0]
    return(int(year))

def make_autopct(values):
        def my_autopct(pct):
            total = sum(values)
            val = int(round(pct * total / 100.0))
            return '{p:.2f}%\n({v:d})'.format(p=pct, v=val)
        return my_autopct

def flatten(l):
    return [item for sublist in l for item in sublist]

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
    #print(data['year_born'].values.tolist())
    #print(data['age_of_winning'].values.tolist())

    pbc = data.groupby('born_in').agg({'country': ['count']})
    #print(pbc)
    pbc.reset_index(inplace=True)
    pbc.columns = pbc.columns.droplevel(0)
    pbc.rename(columns={'': 'born_in','count': 'n'}, inplace=True)
    #pbc.set_index()

    other_counter = 0
    drop_index = []
    for j in range(pbc.shape[0]):
        if (pbc.iloc[j,].loc['n'] < 25):
            drop_index.append(j)
            other_counter += pbc.iloc[j,].loc['n']
    #print(drop_index)
    pbc.drop(index=drop_index, inplace=True)
    other = pd.DataFrame([['Other countries',other_counter]], columns=['born_in','n'])
    pbc = pd.concat([other,pbc])
    pbc.sort_values(['n'], ascending=False, inplace=True)

    #plt.figure(figsize=(12,12))
    #values = pbc['n']
    #labels = pbc['born_in']
    #colors = ['blue', 'orange', 'red', 'yellow', 'green', 'pink', 'brown', 'cyan', 'purple']
    #myexplode = [0,0,0] + [0.08] * (pbc.shape[0] - 3)
    #plt.pie(values, labels=labels, autopct=make_autopct(values), explode=myexplode, colors=colors)
    #plt.show()

    data['category'].replace('', None, inplace=True)
    data.dropna(subset=['category'], inplace=True)
    pcg = data.groupby(['gender','category']).agg({'country': ['count']})
    pcg.reset_index(inplace=True)
    pcg.columns = pcg.columns.droplevel(0)
    pcg.columns = ['gender','category','n']

    categories = flatten(pcg.iloc[0:6,1:2].values.tolist())
    female = flatten(pcg.iloc[0:6,2:].values.tolist())
    male = flatten(pcg.iloc[6:12, 2:].values.tolist())

    age = []
    age_by_group = data.groupby('category')

    for k in categories:
        age_category = age_by_group.get_group(k)['age_of_winning'].values.tolist()
        age.append(age_category)
    age.append(data['age_of_winning'].values.tolist())
    categories.append('All categories')
    #print(age)

    plt.figure(figsize=(10,10))
    #x_axis = np.arange(len(categories))
    #plt.bar(x_axis - 0.2, male, width=0.4, label='Males', color='blue')
    #plt.bar(x_axis + 0.2, female, width=0.4, label='Females', color='crimson')
    plt.boxplot(age, labels=categories, showmeans=True)
    #plt.xticks(x_axis, categories)
    plt.xlabel('Category', fontsize=14)
    plt.ylabel('Age of Obtaining the Nobel Prize', fontsize=14)
    plt.title('Distribution of Ages by Category', fontsize=20)
    #plt.legend()
    plt.show()
