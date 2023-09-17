import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

np.random.seed(52)

def create_bootstrap(X, y, n = 1):
    b_X = []
    b_y = []
    size = len(X)
    for i in range(n):
        #mask = np.random.choice([True, False], size=size, \
        #                       replace=True)
        #X_mask = X[mask]
        #y_mask = y[mask]
        y_mask = np.random.choice(y, size = size, \
                               replace=True)
        #b_X.append(X_mask)
        b_y.append(y_mask)
    return b_X, b_y


def convert_embarked(x):
    if x == 'S':
        return 0
    elif x == 'C':
        return 1
    else:
        return 2



if __name__ == '__main__':
    data = pd.read_csv('https://www.dropbox.com/s/4vu5j6ahk2j3ypk/titanic_train.csv?dl=1')

    data.drop(
        ['PassengerId', 'Name', 'Ticket', 'Cabin'],
        axis=1,
        inplace=True
    )
    data.dropna(inplace=True)

    # Separate these back
    y = data['Survived'].astype(int)
    X = data.drop('Survived', axis=1)

    X['Sex'] = X['Sex'].apply(lambda x: 0 if x == 'male' else 1)
    X['Embarked'] = X['Embarked'].apply(lambda x: convert_embarked(x))

    X_train, X_val, y_train, y_val = \
        train_test_split(X.values, y.values, stratify=y, train_size=0.8)

    boot_X, boot_y = create_bootstrap(X_train, y_train)
    #print(boot_X)
    #print(boot_y)
    print(boot_y[0][:10].tolist())


    # Creating a DecisionTreeClassifier object
    clf = DecisionTreeClassifier()

    # Training a model
    clf = clf.fit(X_train, y_train)
    #test_pred = clf.predict(X_val)
    test_score = clf.score(X_val, y_val)

    #print(round(test_score, 3))
