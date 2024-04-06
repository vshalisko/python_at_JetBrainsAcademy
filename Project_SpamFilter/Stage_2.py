import pandas as pd
import spacy
import re
from sklearn.feature_extraction.text import CountVectorizer
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation


def replace_digits_with_aanumbers(text):
    pattern = re.compile(r'^.*\d.*$')
    result = re.sub(pattern, 'aanumbers', text)
    return result

def lemmatization(data_set, lemmatization_model):
    for i in range(len(data_set)):
        lemmatized = lemmatization_model(data_set.loc[i, "SMS"])
        lemmatized_result = []
        for j in lemmatized:
            j.lemma_ = j.lemma_.translate(str.maketrans('', '', punctuation))
            j.lemma_ = replace_digits_with_aanumbers(j.lemma_)
            if (j.lemma_ not in STOP_WORDS) and (j.pos_ != 'PUNCT') and (len(j.lemma_) > 1):
                lemmatized_result.append(j.lemma_)
        data_set.loc[i, "SMS"] = ' '.join(lemmatized_result)
    return data_set

def bag_of_words(data_set, vectorizer):
    bow = vectorizer.transform(data_set['SMS'])
    result_df = pd.DataFrame(bow.toarray(), columns=vectorizer.get_feature_names_out())
    return result_df

def main():
    data = pd.read_csv("spam.csv", encoding="iso-8859-1")
    data = data[['v1', 'v2']]
    data.rename({"v1": "Target", "v2": "SMS"},
            axis='columns', inplace=True)
    data['Target'] = data['Target'].apply(str.lower)
    data['SMS'] = data['SMS'].apply(str.lower)

    lemmatization_model = spacy.load("en_core_web_sm")
    data = lemmatization(data, lemmatization_model)

    data_random = data.sample(frac=1, random_state=43)
    data_random.reset_index(drop=True, inplace=True)
    train_last_index = int(data_random.shape[0] * 0.8)
    train_set = data_random[0:train_last_index]
    test_set = data_random[train_last_index:]
    test_set_model = pd.DataFrame(test_set)

    vectorizer = CountVectorizer()
    vectorizer.fit(train_set['SMS'])
    train_bow = bag_of_words(train_set, vectorizer)
    train_set = pd.concat([train_set[['Target','SMS']], train_bow], axis=1)

    pd.options.display.max_columns = train_set.shape[1]
    pd.options.display.max_rows = train_set.shape[0]
    print(train_set.iloc[0:200, 0:50])

if __name__ == '__main__':
    main()
