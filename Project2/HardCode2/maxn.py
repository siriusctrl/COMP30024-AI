import numpy as np
import HardCode2.utils as uitls
import HardCode2.config as config


class MaxN:

    def __init__(self, current_state):
        self.current_state = current_state
        self.next_move = {"red": "green", "green": "blue", "blue": "red"}
        self.choices = [i for i in current_state.expand()]

    @staticmethod
    def explore_next(node, discard_rate):

        successor = node.expand()
        utils = []

        for i in successor:
            utils.append((i.cald[3], i))

        utils = sorted(utils, key=lambda x: x[0])

        utils = utils[len(utils) // discard_rate:]

        return utils

    def explore_all(self, nodes, discard_rate=3):
        successor = []

        for n in nodes:
            successor.append([self.explore_next(n, discard_rate)])

        # return [[node_set1], [node_set2]]
        return successor

    def chose(self, rounds=1):
        depth = 2 + max(rounds - 1, 0) * 3
        further_utils = []

        for c in self.choices:
            further_utils.append((self.chose_next(c, depth), c))

        refactored_utils = sorted(further_utils, key=lambda x: self.evaluate_weights(x[0]))
        
        # return the node with highest utility value
        return refactored_utils[-1][-1]

    def chose_next(self, node, depth):
        if depth < 0:
            return node.get_full_utilities()

        return self.max_value([self.chose_next(n, depth - 1) for n in node.expand()])

    def max_value(self, values):

        refactored_values = sorted(values, key=self.evaluate_weights)

        return refactored_values[-1]

    @staticmethod
    def evaluate_weights(x):
        # define how we make trade off between our gain and other opponents lost in utility
        return x[0] + (x[1] + x[2]) * config.TRADE_OFF
