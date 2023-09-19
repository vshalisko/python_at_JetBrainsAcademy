import numpy as np
import pandas as pd
from scipy import stats
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

np.random.seed(52)

class RandomForestClassifier():
    def __init__(self, n_trees=10, max_depth=np.iinfo(np.int64).max, min_error=1e-6):

        self.n_trees = n_trees
        self.max_depth = max_depth
        self.min_error = min_error
        self.max_features = 'sqrt'

        self.is_fit = False

    def fit(self, X_train, y_train):

        self.forest = []

        for i in range(self.n_trees):
            boot_X, boot_y = self.create_bootstrap(X_train, y_train)
            clf = DecisionTreeClassifier(max_features = 'sqrt', \
                                         max_depth = self.max_depth)
            clf = clf.fit(boot_X, boot_y)
            #print(boot_y[:10])
            self.forest.append(clf)

        self.is_fit = True

    def predict(self, X_test):

        if not self.is_fit:
            raise AttributeError('The forest is not fit yet! Consider calling .fit() method.')

        self.prediction = []

        for i in range(self.n_trees):
            pr = self.forest[i].predict(X_val)
            self.prediction.append(pr)

    def create_bootstrap(self, X, y):
        size = len(X)
        y_mask = np.random.choice(y, size = size, replace = True)
        X_mask = X[y_mask]
        return X_mask, y_mask

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

    rf = RandomForestClassifier(n_trees = 1)
    rf.fit(X_train, y_train)
    rf.predict(X_val)
    predictions_2D = np.stack(rf.prediction, axis=0)
    #print(rf.prediction[0])
    #print(predictions_2D)

    test_score = rf.forest[0].score(X_val, y_val).tolist()
    test_score = round(test_score, 3)
    #test_score = 0.755
    #print(test_score)

    result = stats.mode(predictions_2D, axis=0)[0][:10]
    result = (-1 * result) + 1
    print(result.tolist())
