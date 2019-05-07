import numpy as np
import HardCode.utils as uitls
import HardCode.config as config


class MaxN:

    def __init__(self, current_state):
        self.current_state = current_state
        self.next_move = {"red": "green", "green": "blue", "blue": "red"}
        self.choices = [[i] for i in current_state.expand()]

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

    def chose(self, ply=1):
        moves = ply * 3
        layers = dict()
        layers['layers1'] = self.choices

        for i in range(2, moves):
            pre_layer = 'layer' + str(i - 1)
            curr_layer = 'layer' + str(i)
            layers[curr_layer] = []

            for node_set in layers[pre_layer]:
                layers[curr_layer] += self.explore_all(node_set)

        # back propagate the choice
        for i in range(moves - 1, 1, -1):
            curr_layer = 'layer' + str(i)

            for node_set in layers[curr_layer]:
                pass
