import numpy as np
import pandas as pd
import os
import requests
from matplotlib import pyplot as plt

#np.random.seed(seed=3042022)

def one_hot(data: np.ndarray) -> np.ndarray:
    y_train = np.zeros((data.size, data.max() + 1))
    rows = np.arange(data.size)
    y_train[rows, data] = 1
    return y_train


def plot(loss_history: list, accuracy_history: list, filename='plot'):

    # function to visualize learning process at stage 4

    n_epochs = len(loss_history)

    plt.figure(figsize=(20, 10))
    plt.subplot(1, 2, 1)
    plt.plot(loss_history)

    plt.xlabel('Epoch number')
    plt.ylabel('Loss')
    plt.xticks(np.arange(0, n_epochs, 4))
    plt.title('Loss on train dataframe from epoch')
    plt.grid()

    plt.subplot(1, 2, 2)
    plt.plot(accuracy_history)

    plt.xlabel('Epoch number')
    plt.ylabel('Accuracy')
    plt.xticks(np.arange(0, n_epochs, 4))
    plt.title('Accuracy on test dataframe from epoch')
    plt.grid()

    plt.savefig(f'{filename}.png')

def scale(train, test):
    X_max = np.max(train)
    train = train / X_max
    test = test / X_max
    return train, test

def xavier(n_in, n_out):
    low = -np.sqrt(6 / (n_in + n_out))
    high = np.sqrt(6 / (n_in + n_out))
    return np.random.uniform(low, high, (n_in, n_out))

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    return sigmoid(x) * (1 - sigmoid(x))

def mse(x, y):
    return np.mean((x - y) ** 2)

def mse_derivative(x, y):
    return 2 * np.subtract(x, y)

class OneLayerNeural:
    def __init__(self, n_features, n_classes):
        self.W = xavier(n_features, n_classes)
        self.b = xavier(1, n_classes)
        self.z = []
        self.acc = None
        self.loss = None

    def forward(self, X):
        self.z = np.dot(X, self.W) + self.b
        return sigmoid(self.z)

    def backprop(self, X, y, alpha):
        error = (mse_derivative(self.forward(X), y) *
                 sigmoid_derivative(np.dot(X, self.W) + self.b))

        delta_W = (np.dot(X.T, error)) / X.shape[0]
        delta_b = np.mean(error, axis=0)

        self.W -= alpha * delta_W
        self.b -= alpha * delta_b

class TwoLayerNeural:
    def __init__(self, n_features, n_classe, n_hidden):
        self.hidden_neurone = OneLayerNeural(n_features, n_hidden)
        self.output_neurone = OneLayerNeural(n_hidden, n_classe)
        #self.network = [n_features, n_hidden, n_classe]
        self.acc = None
        self.loss = None

    def forward(self, X):
        propagation_set = self.hidden_neurone.forward(X)
        output = self.output_neurone.forward(propagation_set)
        return output

    def backprop(self, X, y, alpha):
        result_network = self.output_neurone.forward(self.hidden_neurone.forward(X))

        # Perform the backward pass
        error2 = ((result_network - y) *
                  sigmoid_derivative(self.output_neurone.z))
        delta_W2 = np.dot(self.hidden_neurone.forward(X).T, error2)
        delta_b2 = np.sum(error2, axis=0, keepdims=True)
        error1 = (np.dot(error2, self.output_neurone.W.T) *
                  sigmoid_derivative(self.hidden_neurone.z))
        delta_W1 = np.dot(X.T, error1)
        delta_b1 = np.sum(error1, axis=0)

        # Update the weights and biases
        self.output_neurone.W -= alpha * delta_W2 / X.shape[0]
        self.output_neurone.b -= alpha * delta_b2 / X.shape[0]
        self.hidden_neurone.W -= alpha * delta_W1 / X.shape[0]
        self.hidden_neurone.b -= alpha * delta_b1 / X.shape[0]

        #print(self.output_neurone.b)


def train(model, X, y, alpha, batch_size=100):
    n = X.shape[0]
    for i in range(0, n, batch_size):
        model.backprop(X[i:i + batch_size], y[i:i + batch_size], alpha)


def accuracy(model, X, y):
    y_pred = np.argmax(model.forward(X), axis=1)
    y_true = np.argmax(y, axis=1)
    model.loss = np.mean((y_pred - y_true) ** 2)
    model.acc = np.mean(y_pred == y_true)



if __name__ == '__main__':

    if not os.path.exists('../Data'):
        os.mkdir('../Data')

    # Download data if it is unavailable.
    if ('fashion-mnist_train.csv' not in os.listdir('../Data') and
            'fashion-mnist_test.csv' not in os.listdir('../Data')):
        print('Train dataset loading.')
        url = "https://www.dropbox.com/s/5vg67ndkth17mvc/fashion-mnist_train.csv?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/fashion-mnist_train.csv', 'wb').write(r.content)
        print('Loaded.')

        print('Test dataset loading.')
        url = "https://www.dropbox.com/s/9bj5a14unl5os6a/fashion-mnist_test.csv?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/fashion-mnist_test.csv', 'wb').write(r.content)
        print('Loaded.')

    # Read train, test data.
    raw_train = pd.read_csv('../Data/fashion-mnist_train.csv')
    raw_test = pd.read_csv('../Data/fashion-mnist_test.csv')

    X_train = raw_train[raw_train.columns[1:]].values
    X_test = raw_test[raw_test.columns[1:]].values

    y_train = one_hot(raw_train['label'].values)
    y_test = one_hot(raw_test['label'].values)

    X_train, X_test = scale(X_train, X_test)
    n_features = X_train.shape[1]

    #NN = OneLayerNeural(n_features, 10)
    NN2 = TwoLayerNeural(n_features, 10, 64)

    #r3 = NN2.forward(X_train[:2, :])
    #NN2.backprop(X_train[:2, :], y_train[:2], alpha=0.1)
    #r4 = NN2.forward(X_train[:2, :])
    #print(r3.flatten().tolist())
    #print(r4.flatten().tolist())

    #print(mse(r4, y_train[:2]).flatten().tolist())

    ## Stage 4
    #accuracy(NN2, X_test, y_test)
    #r1 = NN2.acc.flatten().tolist()
    acc = []
    loss = []
    for _ in range(20):
        train(NN2, X_train, y_train, alpha=0.5)
        accuracy(NN2, X_test, y_test)
        #print(NN2.acc)
        acc.append(NN2.acc)
        loss.append(NN2.loss)

    print(np.array(acc).flatten().tolist())

    plot(loss, acc)
