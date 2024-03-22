import pandas as pd
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
import re

def replace_digits_with_aanumbers(text):
    pattern = r'\b(?:\d+\w*|\w*\d+\w*)\b'
    result = re.sub(pattern, 'aanumbers', text)
    return result

data = pd.read_csv("spam.csv", encoding="iso-8859-1")

data = data[['v1','v2']]
data.rename({"v1": "Target", "v2": "SMS"},
            axis='columns', inplace=True)

data['Target'] = data['Target'].apply(str.lower)
data['SMS'] = data['SMS'].apply(str.lower)

lemmatization_model = spacy.load("en_core_web_sm")

for i in range(len(data)):
#for i in range(20):
    #print(data.loc[i, "SMS"])
    lemmatized = lemmatization_model(data.loc[i, "SMS"])
    lemmatized_result = []
    for j in lemmatized:
        j.lemma_ = j.lemma_.translate(str.maketrans('', '', punctuation))
        j.lemma_ = replace_digits_with_aanumbers(j.lemma_)
        if (j.lemma_ not in STOP_WORDS) and (j.pos_ != 'PUNCT') and (len(j.lemma_) > 1):
            lemmatized_result.append(j.lemma_)
    data.loc[i, "SMS"] = ' '.join(lemmatized_result)

pd.options.display.max_columns = data.shape[1]
pd.options.display.max_rows = data.shape[0]
#print(data.info())
print(data.head(200))

