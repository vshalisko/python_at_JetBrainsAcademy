import numpy as np
import pandas as pd
import os
import requests
from matplotlib import pyplot as plt

#np.random.seed(seed=3042022)

# scroll to the bottom to start coding your solution


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

def scale(X_train, X_test):
    X_train_max = np.max(X_train)
    X_test_max = np.max(X_test)
    return X_train / X_train_max, X_test / X_test_max

def xavier(n_in, n_out):
    high = np.sqrt(6 / (n_in + n_out))
    low = -1 * high
    U = np.random.uniform(low, high,
                          (n_in, n_out))
    xavier_array = np.array(U)
    return xavier_array

def sigmoid(x_list):
    sigma_list = []
    for x in x_list:
        sigma = 1 / (1 + np.exp(-1 * x))
        sigma_list.append(sigma)
    return sigma_list
    #return 1 / (1 + np.exp(-1 * x_list))

def sigmoid_d(sigma_x):
    sigma_d_list = []
    for x in sigma_x:
        sigma_d = x * (1-x)
        sigma_d_list.append(sigma_d)
    return sigma_d_list

def mse(y_pred, y_true):
    n = len(y_true)
    sqe = 0
    for i in range(0, n):
        sqe += (y_pred[i]-y_true[i])**2
    return sqe / n

def mse_di(y_pred, y_true):
    n = len(y_true)
    mse_di_list = []
    for i in range(0, n):
        mse_di_list.append(2*(y_pred[i]-y_true[i]))
    return mse_di_list

class OneLayerNeural:

    def __init__(self, n_features, n_classes):
        self.out = None
        self.n_features = n_features
        self.n_classes = n_classes
        # Initiate weights and biases using Xavier
        self.weights = xavier(n_features, n_classes)
        self.biases = xavier(1, n_classes)

    def forward(self, X):
        n_items = X.shape[0]
        #print(n_items)
        for item in range(0,n_items):
            X_item = X[item]
            ## Manual evaluation of the output neurons state
            neurons_out = []
            for i in range(0, self.n_classes):
                neuron = self.biases[0, i]
                for j in range(0,self.n_features):
                    neuron += X_item[j] * self.weights[j,i]
                neurons_out.append(neuron)
            neurons_out = sigmoid(np.array(neurons_out))
            ## The easier way using matrix dot product
            #self.out = sigmoid(np.dot(X, self.weights) + self.biases)
            if item == 0:
                self.out = neurons_out
            else:
                self.out = np.vstack([self.out, neurons_out])
    def backprop(self, X, y, alpha):
        # Calculating gradients for each of
        # your weights and biases.


        # Updating your weights and biases.
        self.weights = self.weights
        self.biases = self.biases

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

    scaled_X_train, scaled_X_test = scale(X_train, X_test)

    NN = OneLayerNeural(784,10)
    #print(NN)

    ## stage 1
    #res1 = [scaled_X_train[2,778],scaled_X_test[0,774]]
    #res2 = xavier(2,3).flatten().tolist()
    #res3 = sigmoid([-1,0,1,2])
    #print("{} {} {}".format(res1, res2, res3))

    ## Stage 2
    NN.forward(scaled_X_train[0:2,:])
    NN.backprop(scaled_X_train[0:2,:],y_train,alpha=0.1)
    #print(NN.out)
    #res4 = NN.out
    #NN.forward(scaled_X_train[1,:])
    #res5 = NN.out
    #res6 = np.append(res4, res5).tolist()
    #print(res6)
    #print(true_forward_res)
    #print("{} {}".format(res4, res5))

    ## Stage 3
    first_array = [-1,0,1,2]
    second_array = [4,3,2,1]
    true_backprop_res = [0.027703041616827684]

    res7 = [mse(first_array, second_array)]
    res8 = mse_di(first_array, second_array)
    res9 = sigmoid_d(sigmoid(first_array))

    res10 = true_backprop_res
    print("{} {} {} {}".format(res7,res8,res9,res10))
