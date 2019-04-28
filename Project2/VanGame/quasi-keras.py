import numpy as np
import scipy as sp
import VanGame.utils as utils


class NeuralNetwork:

   def __init__(self, arch):
       self.layers = len(arch)
       self.weights = {}

       for idx, layer in enumerate(arch):
           print("idx=",idx)
           print("layer", layer)