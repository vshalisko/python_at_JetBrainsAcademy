## Note: some code inspired by review of Cata77 GitHub user example: 
## https://github.com/Cata77/Spam-Filter/blob/main/spam-filter.py

import pandas as pd
import spacy
import re
from sklearn.feature_extraction.text import CountVectorizer
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score

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

def calculate_confusion_matrix(df):
    TP = 0
    TN = 0
    FP = 0
    FN = 0
    for i in df.index:
        if df.at[i, 'Predicted'] == 'spam' and df.at[i, 'Actual'] == 'spam':
            TP += 1
        elif df.at[i, 'Predicted'] == 'ham' and df.at[i, 'Actual'] == 'ham':
            TN += 1
        elif df.at[i, 'Predicted'] == 'spam' and df.at[i, 'Actual'] == 'ham':
            FP += 1
        elif df.at[i, 'Predicted'] == 'ham' and df.at[i, 'Actual'] == 'spam':
            FN += 1

    accuracy = (TP + TN) / (TP + TN + FP + FN)
    recall = TP / (TP + FN)
    precision = TP / (TP + FP)
    F1 = 2 * precision * recall / (precision + recall)
    performance_results = {'Accuracy': accuracy, 'Recall': recall, 'Precision': precision, 'F1': F1}

    return performance_results

def split_data(data: pd.DataFrame) -> (pd.DataFrame, pd.DataFrame):
    shuffle = data.sample(frac=1, random_state=43)
    last = int(shuffle.shape[0] * 0.8)
    return shuffle[:last], shuffle[last:]

class CustomNaiveBayes:
    def __init__(self, alpha=1.0):
        self.alpha: float = alpha
        self.p_words: pd.DataFrame = pd.DataFrame()
        self.p_spam: float = 0.0
        self.p_ham: float = 0.0
        self.vocab_set: set[str] = set()

    def fit(self, data: pd.DataFrame):
        vectorizer = CountVectorizer()
        vectorizer.fit(data['SMS'])
        word_counts = pd.DataFrame(vectorizer.transform(data['SMS']).toarray(),
                                   columns=vectorizer.get_feature_names_out())
        bag_of_words = data.reset_index(drop=True).join(word_counts)
        n_words = bag_of_words.groupby('Target').sum(numeric_only=True).T
        self.p_words = (n_words + self.alpha) / (n_words.sum() + self.alpha * n_words.shape[0])
        self.p_ham, self.p_spam = data['Target'].value_counts() / data.shape[0]
        self.vocab_set = set(self.p_words.index)

    def predict(self, msg: str) -> str:
        words = [w for w in msg.split() if w in self.vocab_set]
        p_msg: pd.Series = self.p_words.loc[words].prod() * [self.p_ham, self.p_spam]
        result = 'unknown'
        if p_msg['spam'] > p_msg['ham']:
            result = 'spam'
        if p_msg['spam'] < p_msg['ham']:
            result = 'ham'
        return result

def bag_of_words(data_set, vectorizer):
    bow = vectorizer.transform(data_set['SMS'])
    result_df = pd.DataFrame(bow.toarray(), columns=vectorizer.get_feature_names_out())
    return result_df

def convert_column_to_binary(dataframe):
    dataframe['Target'] = (dataframe['Target'] == 'spam').astype('int')
    return dataframe


def model_performance(train_set, test_set):
    test_set = pd.DataFrame(test_set)
    vector = CountVectorizer()
    vector.fit(train_set['SMS'])
    train_bow = bag_of_words(train_set, vector)
    test_bow = bag_of_words(test_set, vector)

    train_set = convert_column_to_binary(train_set)
    test_set = convert_column_to_binary(test_set)

    model = MultinomialNB()
    X_train = train_bow.values
    y_train = train_set['Target'].values
    model.fit(X_train, y_train)

    X_test = test_bow.values
    y_test = test_set['Target'].values
    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)
    recall = recall_score(y_test, predictions)
    precision = precision_score(y_test, predictions)
    f1 = f1_score(y_test, predictions)
    performance_results = {'Accuracy': accuracy, 'Recall': recall, 'Precision': precision, 'F1': f1}

    return predictions
    #return performance_results

def main():
    data = pd.read_csv("spam.csv", encoding="iso-8859-1")
    data = data[['v1', 'v2']]
    data.rename({"v1": "Target", "v2": "SMS"},
            axis='columns', inplace=True)
    data['Target'] = data['Target'].apply(str.lower)
    data['SMS'] = data['SMS'].apply(str.lower)

    lemmatization_model = spacy.load("en_core_web_sm")
    data = lemmatization(data, lemmatization_model)

    train_set, test_set = split_data(data)

    model = CustomNaiveBayes()
    model.fit(train_set)
    actual = test_set['Target']
    predicted = test_set['SMS'].apply(model.predict)
    classification_df_test = pd.DataFrame({'Predicted': predicted,
                        'Actual': actual})
    #print(calculate_confusion_matrix(classification_df_test))

    predicted2 = model_performance(train_set, test_set)
    classification_df_test2 = pd.DataFrame({'Predicted': predicted2,
                        'Actual': actual})
    classification_df_test2 = classification_df_test2.astype(str)
    classification_df_test2.loc[classification_df_test2['Predicted'] == '0', 'Predicted'] = 'ham'
    classification_df_test2.loc[classification_df_test2['Predicted'] == '1', 'Predicted'] = 'spam'
    #print(classification_df_test2)
    print(calculate_confusion_matrix(classification_df_test2))

if __name__ == '__main__':
    main()
