import tensorflow as tf
from keras import models, layers
import numpy as np
from keras.models import load_model
import keras
import os


class dnn():

    def __init__(self, name=os.path.join(os.getcwd(), 'VanGame', 'my_model.h5')):
        self.model = load_model(name)

    def predict(self, state):
        s = np.array([state])
        return self.model.predict(s)[0][0]
