import numpy as np
import HardCode2.utils as uitls
import HardCode2.config as config


class MaxN:

    def __init__(self, current_state):
        self.current_state = current_state
        self.next_move = {"red": "green", "green": "blue", "blue": "red"}
        self.choices = [i for i in current_state.expand()]
        self.root_colour = current_state.colour
        self.all_colour = {"red":["green", "blue"], "green": ["red", "blue"], "blue": ["red", "green"]}
        self.next_colour = {"red":"green", "green": "blue", "blue": "red"}

    @staticmethod
    def explore_next(node, colour, discard_rate):

        successor = node.expand(colour)
        utils = []

        for i in successor:
            utils.append((i.cald[3], i))

        utils = sorted(utils, key=lambda x: x[0])

        utils = utils[len(utils) // discard_rate:]

        return [i[-1] for i in utils]

    def chose(self, rounds=1):
        depth = 2 + max(rounds - 1, 0) * 3
        further_utils = []

        for c in self.choices:
            further_utils.append((self.chose_next(c, depth), c))

        refactored_utils = sorted(further_utils, key=lambda x: self.evaluate_weights(x[0], self.root_colour))

        # return the node with highest utility value
        return refactored_utils[-1][-1]

    def chose_next(self, node, depth):
        if depth < 0:
            return node.get_full_utilities()

        values = [self.chose_next(n, depth - 1) for n in self.explore_next(node, self.next_colour[node.colour], 3)]
        return self.max_value(values, node.colour)

    def max_value(self, values, colour):

        refactored_values = sorted(values, key=lambda x: self.evaluate_weights(x, colour))

        return refactored_values[-1]

    def evaluate_weights(self, x, colour):
        # define how we make trade off between our gain and other opponents lost in utility
        opp_one = self.all_colour[self.root_colour][0]
        opp_two = self.all_colour[self.root_colour][1]
        return x[colour] + (x[opp_one] + x[opp_two]) * config.TRADE_OFF
