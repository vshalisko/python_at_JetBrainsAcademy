import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import Normalizer
from sklearn import metrics
import warnings
warnings.filterwarnings("ignore")

def fit_predict_eval(model, features_train, features_test, target_train, target_test):
    # here you fit the model
    model = model.fit(features_train, target_train)
    target_pred = model.predict(features_test)
    score = metrics.accuracy_score(target_test, target_pred).round(4)
    print(f'Model: {model}\nAccuracy: {round(score,3)}\n')
    return(score)

def fit_predict_eval_silent(model, features_train, features_test, target_train, target_test):
    # here you fit the model
    model = model.fit(features_train, target_train)
    target_pred = model.predict(features_test)
    score = metrics.accuracy_score(target_test, target_pred).round(4)
    #print(f'Model: {model}\nAccuracy: {score}\n')
    return(score)

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

## Stage 1
#print("Classes: {}".format(np.unique(y_train)))
#print("Features' shape: {}".format(np.shape(x_train)))
#print("Target's shape: {}".format(np.shape(y_train)))
#print("min: {}, max: {}".format(np.min(x_train),np.max(x_train)))

## Stage 2
#print("x_train shape: {}".format(np.shape(x_train)))
#print("x_test shape: {}".format(np.shape(x_test)))
#print("y_train shape: {}".format(np.shape(y_train)))
#print("y_test shape: {}".format(np.shape(y_test)))
#print('Proportion of samples per class in train set:')
#train_y_pd = pd.DataFrame(y_train, columns=['y'])
#proportion = train_y_pd.y.value_counts(normalize=True).round(2)
#proportion.index.name = None
#proportion.name = None
#print(proportion)

## Stage 3
models = [KNeighborsClassifier(),
          DecisionTreeClassifier(random_state=40),
          LogisticRegression(random_state=40),
          RandomForestClassifier(random_state=40)]

score_list_raw = {}
for i, model in enumerate(models):
    score = fit_predict_eval_silent(
        model=model,
        features_train=x_train,
        features_test=x_test,
        target_train=y_train,
        target_test=y_test
    )
    score_list_raw[model] = score

score_list = {}
for i, model in enumerate(models):
    score = fit_predict_eval(
        model=model,
        features_train=x_train_norm,
        features_test=x_test_norm,
        target_train=y_train,
        target_test=y_test
    )
    score_list[model] = score

# Sort models
sorted_score_list = dict(sorted(score_list.items(), key=lambda kv: kv[1], reverse=True))

# Find the best model
best_raw = max(score_list_raw, key=score_list_raw.get)
best = max(score_list, key=score_list.get)

answer_1 = "no"
if (score_list_raw[best_raw].round(3) < score_list[best].round(3)):
    answer_1 = "yes"
print("The answer to the 1st question: {}\n".format(answer_1))

#print("The answer to the 2nd question: {}-{}".format(
#            type(best).__name__,
#            score_list[best].round(3)))

#res = []
#res_key = []
answer_2 = "The answer to the 2nd question: "
for j, key in enumerate(sorted_score_list.keys()):
    #res.append(sorted_score_list[key])
    #res_key.append(key)
    if j < 2:
        answer_2 += type(key).__name__ + "-"
        answer_2 += str(round(sorted_score_list[key],3))
        #if j < (len(sorted_score_list.keys()) - 1):
        if j < 1:
            answer_2 += ", "

print(answer_2)

#print(sorted_score_list.values())
#print(sorted_score_list.keys())
#print(res)
#print(res_key)
#print(type(res_key[2]).__name__)
#print(res[2])
