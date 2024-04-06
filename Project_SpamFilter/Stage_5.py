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

def features_probability_calculator(data_set):
    alpha = 1
    feature_df = pd.DataFrame({'feature': [], 'N_spam': [], 'N_ham': []})
    spam_world_counter = 0
    ham_world_counter = 0
    features = data_set.columns.tolist()
    total_world_counter = len(features[2:])
    for feature in features[2:]:
        #N_feature_spam = data_set.loc[data_set['Target'] == "spam", feature].astype(bool).sum(axis=0)
        N_feature_spam = data_set.loc[data_set['Target'] == "spam", feature].sum(axis=0)
        #N_feature_ham = data_set.loc[data_set['Target'] == "ham", feature].astype(bool).sum(axis=0)
        N_feature_ham = data_set.loc[data_set['Target'] == "ham", feature].sum(axis=0)
        spam_world_counter += N_feature_spam
        ham_world_counter += N_feature_ham
        new_row = pd.DataFrame({'feature': [feature], 'N_spam': [N_feature_spam], 'N_ham': [N_feature_ham]})
        feature_df = pd.concat([feature_df, new_row], ignore_index=True)
        #print("{} {} {}".format(feature,N_feature_spam,N_feature_ham))

    feature_df['Spam Probability'] = (feature_df['N_spam'] + alpha) / (spam_world_counter + alpha * total_world_counter)
    feature_df['Ham Probability'] = (feature_df['N_ham'] + alpha) / (ham_world_counter + alpha * total_world_counter)
    feature_df.set_index('feature', inplace=True)
    feature_df.index.name = None
    feature_df.drop(['N_spam','N_ham'], axis=1, inplace=True)
    return(feature_df)

def classifier(data_set, P_spam, P_ham, train_feature_df):
    classification_df = pd.DataFrame({'Predicted': [], 'Actual': []})
    for i in range(len(data_set)):
        SMS = data_set.iloc[i, 1]
    ## the following is problematic as it iterates taking the index order
    #for ind in data_set.index:
        #SMS = data_set['SMS'][ind]
        #print(SMS)
        sms_list = SMS.split()
        spam_probability = P_spam
        ham_probability = P_ham
        for word in sms_list:
            if word in train_feature_df.index:
                spam_probability *= train_feature_df.loc[word]['Spam Probability']
                ham_probability *= train_feature_df.loc[word]['Ham Probability']

        predicted = 'unknown'
        if spam_probability > ham_probability:
            predicted = 'spam'
        elif spam_probability < ham_probability:
            predicted = 'ham'
        # print("p spam: {} P ham:{} Decision:{}".format(
        #                       spam_probability, ham_probability, predicted))
        #new_row = pd.DataFrame({'Predicted': [predicted],
        #                        'Actual': [data_set['Target'][ind]]},
        #                       index=[ind])
        new_row = pd.DataFrame({'Predicted': [predicted],
                                'Actual': [data_set.iloc[i,0]]},
                                index=[data_set.iloc[[i, 1]].index[0]])
        classification_df = pd.concat([classification_df, new_row])
    return classification_df

def calculate_confusion_matrix(df):
    TP = 0
    TN = 0
    FP = 0
    FN = 0
    for i in df.index:
        if df.at[i, 'Predicted'] == 'spam' and df.at[i, 'Actual'] == 'spam':
            TN += 1
        elif df.at[i, 'Predicted'] == 'ham' and df.at[i, 'Actual'] == 'ham':
            TP += 1
        elif df.at[i, 'Predicted'] == 'spam' and df.at[i, 'Actual'] == 'ham':
            FN += 1
        elif df.at[i, 'Predicted'] == 'ham' and df.at[i, 'Actual'] == 'spam':
            FP += 1

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
    ## Class other user
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

    vectorizer = CountVectorizer()
    vectorizer.fit(train_set['SMS'])
    train_bow = bag_of_words(train_set, vectorizer)
    train_set_wo_index = train_set.reset_index(drop=True)
    train_set_bow = pd.concat([train_set_wo_index[['Target','SMS']], train_bow], axis=1)

    pd.options.display.max_columns = train_set_bow.shape[1]
    pd.options.display.max_rows = train_set_bow.shape[0]
    #print(train_set_bow.iloc[0:200, 0:50])

    train_feature_df = features_probability_calculator(train_set_bow)
    #print(train_feature_df.iloc[:200, :])

    N_spam = train_set_bow.loc[train_set_bow['Target'] == "spam", :].shape[0]
    N_ham = train_set_bow.loc[train_set_bow['Target'] == "ham", :].shape[0]
    N_total = train_set_bow.shape[0]
    P_spam = N_spam / N_total
    P_ham = N_ham / N_total
    #print(P_spam)
    #print(P_ham)

    classification_df_test = classifier(test_set, P_spam, P_ham, train_feature_df)
    #print(classification_df_test.iloc[:50, :])
    print(calculate_confusion_matrix(classification_df_test))

    ## Alternative (faster and better) using class developed by other user
    #model = CustomNaiveBayes()
    #model.fit(train_set)
    #actual_1 = test_set['Target']
    #predicted_1 = test_set['SMS'].apply(model.predict)
    #classification_df_test1 = pd.DataFrame({'Predicted': predicted_1,
    #                    'Actual': actual_1})
    #print(calculate_confusion_matrix(classification_df_test1))

if __name__ == '__main__':
    main()
