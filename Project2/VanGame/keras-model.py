import tensorflow as tf
from keras import models, layers
import numpy as np
from keras.models import load_model


class dnn():

    def __init__(self, name='my_model.h5'):
        self.model = load_model(name)

    def predict(self, board):
        return self.model.predict(board)[0][0]
