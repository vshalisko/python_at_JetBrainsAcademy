import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split

#train_ds = tf.keras.datasets.mnist.load_data(path="mnist.npz")
(x, y), (_, _) = tf.keras.datasets.mnist.load_data()

#x_train = x_train.reshape(60000, 784).astype('float32') / 255
x = x.reshape(60000, 784)

x_train, x_test, y_train, y_test = train_test_split(x[:6000], y[:6000], train_size=0.7, random_state=40)

#print("Classes: {}".format(np.unique(y_train)))
#print("Features' shape: {}".format(np.shape(x_train)))
#print("Target's shape: {}".format(np.shape(y_train)))
#print("min: {}, max: {}".format(np.min(x_train),np.max(x_train)))

print("x_train shape: {}".format(np.shape(x_train)))
print("x_test shape: {}".format(np.shape(x_test)))
print("y_train shape: {}".format(np.shape(y_train)))
print("y_test shape: {}".format(np.shape(y_test)))

print('Proportion of samples per class in train set:')
train_y_pd = pd.DataFrame(y_train, columns=['y'])
proportion = train_y_pd.y.value_counts(normalize=True).round(2)
proportion.index.name = None
proportion.name = None
print(proportion)
