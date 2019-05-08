import numpy as np
import HardCode2.utils as utils
import HardCode2.config as config


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

        refactored_utils = sorted(further_utils, key=lambda x: self.evaluate_weights(x[0][0], self.root_colour))
        # print("\n$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$count=", self.count)
        # print("\nutility=", [i[0] for i in refactored_utils])
        for i in refactored_utils:
            utils.print_board(i[-1].current_board, i[-1].calds)
            print(i[0][0])
            print("\nfrom=\n")
            utils.print_board(i[0][-1].current_board, i[-1].calds)
        # return the node with highest utility value
        return refactored_utils[-1][-1]

    def chose_next(self, node, depth):
        self.count += 1
        if depth == 0:
           # if node.calds["green"][-1] > -200:
                # utils.print_board(node.current_board, node.calds)
            return (node.get_full_utilities(), node)

        values = [self.chose_next(n, depth - 1) for n in self.explore_next(node, self.next_colour[node.colour], 2)]
        
        mv = self.max_value(values, node.colour)

        return mv

    def max_value(self, values, colour):

        refactored_values = sorted(values, key=lambda x: self.evaluate_weights(x[0], colour))

        return refactored_values[-1]

    def evaluate_weights(self, x, colour):
        # define how we make trade off between our gain and other opponents lost in utility
        opp_one = self.all_colour[self.root_colour][0]
        opp_two = self.all_colour[self.root_colour][1]
        return x[colour] + (x[opp_one] + x[opp_two]) * config.TRADE_OFF
