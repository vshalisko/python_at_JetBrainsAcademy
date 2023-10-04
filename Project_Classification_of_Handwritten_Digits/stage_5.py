import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import Normalizer
from sklearn import metrics
import warnings
warnings.filterwarnings("ignore")

#train_ds = tf.keras.datasets.mnist.load_data(path="mnist.npz")
(x, y), (_, _) = tf.keras.datasets.mnist.load_data()

#x_train = x_train.reshape(60000, 784).astype('float32') / 255
x = x.reshape(60000, 784)

x_train, x_test, y_train, y_test = train_test_split(x[:6000], y[:6000], train_size=0.7, random_state=40)

transformer = Normalizer().fit(x)
#x_train_norm = transformer.transform(x_train)
#x_test_norm = transformer.transform(x_test)

x_train_norm = transformer.fit_transform(x_train)
x_test_norm = transformer.fit_transform(x_test)

KNN_param_grid = {'n_neighbors': [3, 4], 'weights': ['uniform', 'distance'], 'algorithm': ['auto', 'brute']}
RF_param_grid = {'n_estimators': [300, 500], 'max_features': ['sqrt', 'log2'], 'class_weight': ['balanced', 'balanced_subsample']}

RF_param_grid_red = {'n_estimators': [300], 'max_features': ['sqrt'], 'class_weight': ['balanced', 'balanced_subsample']}

grid_search_KNN = GridSearchCV(
    estimator=KNeighborsClassifier(),
    param_grid=KNN_param_grid,
    scoring='accuracy',
    n_jobs=2
)

grid_search_RF = GridSearchCV(
    estimator=RandomForestClassifier(random_state=40),
    param_grid=RF_param_grid,
    scoring='accuracy',
    n_jobs=2
)

print("K-nearest neighbours algorithm")

grid_search_KNN.fit(x_train_norm, y_train)
print("best estimator: {}".format(grid_search_KNN.best_estimator_))
#print(grid_search_KNN.best_score_)
#print(grid_search_KNN.best_params_)

best_KNN_model = KNeighborsClassifier()
best_KNN_model.set_params(**grid_search_KNN.best_params_)
best_KNN_model.fit(x_train_norm, y_train)
y_predict_KNN = best_KNN_model.predict(x_test_norm)

score_KNN = metrics.accuracy_score(y_test, y_predict_KNN).round(4)
print(f'accuracy: {round(score_KNN, 3)}\n')

print("Random forest algorithm")
grid_search_RF.fit(x_train_norm, y_train)
print("best estimator: {}".format(grid_search_RF.best_estimator_))
#print(grid_search_RF.best_score_)
#print(grid_search_RF.best_params_)

best_RF_model = RandomForestClassifier(random_state=40)
best_RF_model.set_params(**grid_search_RF.best_params_)
best_RF_model.fit(x_train_norm, y_train)
y_predict_RF = best_RF_model.predict(x_test_norm)

score_RF = metrics.accuracy_score(y_test, y_predict_RF).round(4)
print(f'accuracy: {round(score_RF, 3)}\n')
