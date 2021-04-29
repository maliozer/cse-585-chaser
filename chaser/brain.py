import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'

import tensorflow as tf

from tensorflow.keras.layers import *
from tensorflow.keras import Sequential
import numpy as np


class Brain():
    def __init__(self):
        self.model = self.create_model()

    def softmax(self, x):
        """Compute softmax values for each sets of scores in x."""
        return np.exp(x) / np.sum(np.exp(x), axis=0)

    def hardmax(self, x):
        return np.argmax(x)

    def create_model(self):
        model = Sequential()
        model.add(Dense(5, input_shape=(5,), activation='relu'))
        model.add(Dense(7, input_shape=(5,), activation='relu'))
        model.add(Dense(4, input_shape=(7,), activation='sigmoid'))
        model.add(Dense(4, input_shape=(4,), activation='softmax'))

        model.compile(loss='categorical_crossentropy', optimizer='sgd')

        return model

    def get_decision(self, X, Y):

        #self.model.fit(X, Y)
        #print("Target is ", Y)
        return self.hardmax(self.model.predict(X)[0])


    def update_weights(self):
        #self.model.get_weights()
        #print(type(self.model.get_weights()[0]))
        pass

    def loss_fn():
        pass

    def checkpoint(self):
        checkpoint_path = "chaser/checkpoint/cp.ckpt"
        checkpoint_dir = os.path.dirname(checkpoint_path)

        # Create a callback that saves the model's weights

        self.model.save_weights(checkpoint_path.format(epoch=0))

    def load_checkpoint(self):
        checkpoint_path = "chaser/checkpoint/cp.ckpt"
        checkpoint_dir = os.path.dirname(checkpoint_path)
        latest = tf.train.latest_checkpoint(checkpoint_dir)
        self.model.load_weights(latest)
        print("loaded")