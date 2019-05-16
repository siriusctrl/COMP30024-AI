import numpy as np
import HardCode3.utils as utils
import HardCode3.config as config


class MaxN:

    def __init__(self, current_state):
        self.current_state = current_state
        self.next_move = {"red": "green", "green": "blue", "blue": "red"}
        self.choices = [i for i in current_state.expand()]
        self.root_colour = current_state.colour
        self.all_colour = {"red":["green", "blue"], "green": ["red", "blue"], "blue": ["red", "green"]}
        self.next_colour = {"red":"green", "green": "blue", "blue": "red"}
        self.count = 0

    @staticmethod
    def explore_next(node, colour, discard_rate):

        successor = node.expand(colour)
        utils = []

        '''for i in successor:
            utils.append((i.calculated[3], i))'''

        utils = sorted(successor, key=lambda x: x.calculated[3])

        utils = utils[len(utils) // discard_rate:]
        

        return utils

    def chose(self, rounds=1):
        depth = 2 + max(rounds - 1, 0) * 3
        further_utils = []

        for c in self.choices:
            further_utils.append((self.chose_next(c, depth), c))
        print(self.count)

        refactored_utils = sorted(further_utils, key=lambda x: x[0][1].calculateds[self.current_state.colour][-1])

        best = refactored_utils[-1][0][1]

        return refactored_utils[-1][-1]

    def chose_next(self, node, depth):
        self.count += 1
        if depth == 0:
            return node.get_full_utilities(), node
        
        values = [self.chose_next(n, depth - 1) for n in self.explore_next(node, self.next_colour[node.colour], 2)]
        
        # mv = self.max_value(values, node.colour)

        mv = sorted(values, key=lambda x: x[1].calculateds[node.colour][-1])

        return mv[-1]

    def max_value(self, values, colour):

        refactored_values = sorted(values, key=lambda x: self.evaluate_weights(x[0], colour))

        return refactored_values[-1]

    def evaluate_weights(self, x, colour):
        # define how we make trade off between our gain and other opponents lost in utility
        opp_one = self.all_colour[colour][0]
        opp_two = self.all_colour[colour][1]
        return x[colour] + (x[opp_one] + x[opp_two]) * config.TRADE_OFF


def softmax_chose(options: list):
    ops = np.array(options)
    prob = softmax(np.array(ops))
    # print("\n", options, "\n", prob, "\n")
    prob = prob.reshape(len(prob),)
    return np.random.choice(len(options), 1, p=prob)[0]


def softmax(x):
    """Compute softmax values for each sets of scores in x."""
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum(axis=0)
