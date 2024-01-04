import pandas as pd

data = pd.read_csv("spam.csv", encoding="iso-8859-1")

data = data[['v1','v2']]
data.rename({"v1": "Target", "v2": "SMS"},
            axis='columns', inplace=True)

data['Target'] = data['Target'].apply(str.lower)
data['SMS'] = data['SMS'].apply(str.lower)

pd.options.display.max_columns = data.shape[1]
pd.options.display.max_rows = data.shape[0]
#print(data.info())
print(data.head(200))
