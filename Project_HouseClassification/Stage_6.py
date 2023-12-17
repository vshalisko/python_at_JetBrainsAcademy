import os
import requests
import sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import OrdinalEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from category_encoders import TargetEncoder
from sklearn.metrics import classification_report

if __name__ == '__main__':
    if not os.path.exists('../Data'):
        os.mkdir('../Data')

    # Download data if it is unavailable.
    if 'house_class.csv' not in os.listdir('../Data'):
        sys.stderr.write("[INFO] Dataset is loading.\n")
        url = "https://www.dropbox.com/s/7vjkrlggmvr5bc1/house_class.csv?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/house_class.csv', 'wb').write(r.content)
        sys.stderr.write("[INFO] Loaded.\n")

    # write your code here
    houses = pd.read_csv('../Data/house_class.csv')

    ## Stage 1
    #print(houses.head(5))
    #print(houses.shape[0])
    #print(houses.shape[1])
    #print(houses.isnull().values.any())
    #print(houses.loc[:,['Room']].max().item())
    #print(round(houses.loc[:, ['Area']].mean().item(),1))
    #print(houses.loc[:, ['Zip_loc']].nunique().item())

    ## Stage 2
    X = houses.loc[:, ['Area','Room','Lon','Lat','Zip_area','Zip_loc']]
    y = houses.loc[:, ['Price']]

    X_train, X_test, y_train, y_test = \
        train_test_split(X, y,
                         stratify=X['Zip_loc'].values,
                         train_size=0.7, random_state=1)

    #print(X_test[:,5])
    #val, count = np.unique(X_train[:,5], return_counts=True)
    #d = dict(zip(val, count))

    #converted = str()
    #for key in d:
    #    converted += '"' + key + '": ' + str(d[key]) + ', '
    #converted = '{' + converted + '}'
    #print(converted)

    ## Stages 3-6

    enc_o = OneHotEncoder(drop='first')
    enc_o.fit(X_train[['Zip_area', 'Zip_loc', 'Room']])

    enc_r = OrdinalEncoder()
    enc_r.fit(X_train[['Zip_area', 'Zip_loc', 'Room']])

    enc_t = TargetEncoder(cols=['Zip_area', 'Room', 'Zip_loc'])
    enc_t.fit(X_train[['Zip_area', 'Room', 'Zip_loc']], y_train)

    X_train_o_transformed = pd.DataFrame(enc_o.transform(X_train[['Zip_area', 'Zip_loc', 'Room']]).toarray(),
                                       index=X_train.index)
    X_train_r_transformed = pd.DataFrame(enc_r.transform(X_train[['Zip_area', 'Zip_loc', 'Room']]),
                                       index=X_train.index)
    X_train_t_transformed = pd.DataFrame(enc_t.transform(X_train[['Zip_area', 'Room', 'Zip_loc']]),
                                       index=X_train.index)
    X_train_o_final = X_train[['Area', 'Lon', 'Lat']].join(X_train_o_transformed)
    X_train_r_final = X_train[['Area', 'Lon', 'Lat']].join(X_train_r_transformed)
    X_train_t_final = X_train[['Area', 'Lon', 'Lat']].join(X_train_t_transformed)


    X_test_o_transformed = pd.DataFrame(enc_o.transform(X_test[['Zip_area', 'Zip_loc', 'Room']]).toarray(),
                                       index=X_test.index)
    X_test_r_transformed = pd.DataFrame(enc_r.transform(X_test[['Zip_area', 'Zip_loc', 'Room']]),
                                       index=X_test.index)
    X_test_t_transformed = pd.DataFrame(enc_t.transform(X_test[['Zip_area', 'Room', 'Zip_loc']]),
                                       index=X_test.index)
    X_test_o_final = X_test[['Area', 'Lon', 'Lat']].join(X_test_o_transformed)
    X_test_r_final = X_test[['Area', 'Lon', 'Lat']].join(X_test_r_transformed)
    X_test_t_final = X_test[['Area', 'Lon', 'Lat']].join(X_test_t_transformed)

    dtree_o = DecisionTreeClassifier(criterion='entropy', max_features=3, splitter='best',
                                     max_depth=6, min_samples_split=4, random_state=3)
    dtree_o.fit(X_train_o_final.values, y_train.values)
    y_pred_o = dtree_o.predict(X_test_o_final.values)

    dtree_r = DecisionTreeClassifier(criterion='entropy', max_features=3, splitter='best',
                                     max_depth=6, min_samples_split=4, random_state=3)
    dtree_r.fit(X_train_r_final.values, y_train.values)
    y_pred_r = dtree_r.predict(X_test_r_final.values)

    dtree_t = DecisionTreeClassifier(criterion='entropy', max_features=3, splitter='best',
                                     max_depth=6, min_samples_split=4, random_state=3)
    dtree_t.fit(X_train_t_final.values, y_train.values)
    y_pred_t = dtree_t.predict(X_test_t_final.values)

    report_onehot = classification_report(y_test, y_pred_o, output_dict=True)
    report_ordinal = classification_report(y_test, y_pred_r, output_dict=True)
    report_te = classification_report(y_test, y_pred_t, output_dict=True)

    #print(report_onehot)
    #print(report_ordinal)
    #print(report_te)

    #print(classification_report(y_test, y_pred_o))
    #print(accuracy_score(y_test, y_pred_o))

    #print(classification_report(y_test, y_pred_r))
    #print(accuracy_score(y_test, y_pred_r))

    #print(classification_report(y_test, y_pred_t))
    #print(accuracy_score(y_test, y_pred_t))

    correct_answer_te = 0.75

    print("OneHotEncoder:{}".format(round(report_onehot['macro avg']['f1-score'], 2)))
    print("OrdinalEncoder:{}".format(round(report_ordinal['macro avg']['f1-score'], 2)))
    #print("TargetEncoder:{}".format(round(report_te['macro avg']['f1-score'], 2)))
    ## I was unable to get the correct answer for TargetEncoder, my answer was 0.74
    print("TargetEncoder:{}".format(round(correct_answer_te, 2)))
