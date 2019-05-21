import numpy as np
import VanGame.utils as utils
import VanGame.config as config

import random
import math


class MaxN:

    def __init__(self, current_state):
        self.current_state = current_state
        self.next_move = {"red": "green", "green": "blue", "blue": "red"}
        self.choices = [i for i in current_state.expand()]

        self.choices = sorted(self.choices, key=lambda x: x.eval[3])

        self.choices = self.choices[int(len(self.choices) // 2):]
        self.root_colour = current_state.colour
        self.all_colour = {"red":["green", "blue"], "green": ["red", "blue"], "blue": ["red", "green"]}
        self.next_colour = {"red":"green", "green": "blue", "blue": "red"}
        self.count = 0

    @staticmethod
    def explore_next(node, colour, discard_rate):

        successor = node.expand(colour=colour)
        utils = []

        '''for i in successor:
            utils.append((i.calculated[3], i))'''

        utils = sorted(successor, key=lambda x: x.eval[3])

        utils = utils[len(utils) // discard_rate:]
        
        return utils

    def chose(self, rounds=1):
        depth = 2 + max(rounds - 1, 0) * 3
        further_utils = []

        for c in self.choices:
            further_utils.append((self.chose_next(c, depth), c))

        refactored_utils = sorted(further_utils, key=lambda x: x[0][1].evals[self.current_state.colour][-1])

        best = refactored_utils[-1][0][1]


        return refactored_utils[-1][-1]

    def chose_next(self, node, depth):
        self.count += 1
        if depth == 0:
            return 0, node
        
        values = [self.chose_next(n, depth - 1) for n in self.explore_next(node, self.next_colour[node.colour], 2)]
        
        # mv = self.max_value(values, node.colour)

        mv = sorted(values, key=lambda x: x[1].evals[node.colour][-1])

        return mv[-1]
