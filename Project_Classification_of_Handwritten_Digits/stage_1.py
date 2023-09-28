import numpy as np
import tensorflow as tf

#train_ds = tf.keras.datasets.mnist.load_data(path="mnist.npz")
(x_train, y_train), (_, _) = tf.keras.datasets.mnist.load_data()

#x_train = x_train.reshape(60000, 784).astype('float32') / 255
x_train = x_train.reshape(60000, 784)

#print(len(x_train))
print("Classes: {}".format(np.unique(y_train)))
print("Features' shape: {}".format(np.shape(x_train)))
print("Target's shape: {}".format(np.shape(y_train)))
print("min: {}, max: {}".format(np.min(x_train),np.max(x_train)))
