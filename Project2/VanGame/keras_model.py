import numpy as np
import VanGame.utils as utils
import pickle
import os


class dnn:

    def __init__(self, filename='trained_model'):

        self.activation_function = {
                                    "relu": utils.ReLu.forward,
                                    "linear": utils.Linear.forward,
                                    "tanh": utils.Tanh.forward
        }

        self.params = {}
        self.arch = []
        # load the feed-forward NN weights and bias
        self.load(os.path.join(os.getcwd(), "VanGame", filename))

    def forward(self, i, l, prop):
        activation = self.activation_function[prop['activation']]
        weights = self.params['weight' + str(l)]
        bias = self.params['bias' + str(l)]
        o = np.dot(i, weights) + bias
        return activation(o)

    def predict(self, init_input):
        output = np.array([])
        for level, prop in enumerate(self.arch):
            if output.shape[0] != 0:
                output = self.forward(output, level, prop)
            else:
                output = self.forward(init_input, level, prop)

        return output

    def load(self, filename) -> None:
        """
        load the proper weights
        :param filename: the name of the file
        """

        with open(filename, 'rb') as f:
            m = pickle.load(f)

        for i in range(len(m)):
            if i % 2 == 0:
                self.arch.append({"input_size": m[i].shape[0], "output_size": m[i].shape[1], "activation": "relu"})
                self.params['weight' + str(i // 2)] = m[i]
            else:
                self.params['bias' + str(i // 2)] = m[i]

        self.arch[-1]['activation'] = 'tanh'
        # print(self.params)
