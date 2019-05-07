import numpy as np
import HardCode.utils as uitls
import HardCode.config as config


class MaxN:

    def __init__(self, current_state):
        self.current_state = current_state
        self.next_move = {"red": "green", "green": "blue", "blue": "red"}

    def predict(self):
        successor = self.current_state.expand()
        successor[0].expand_opponent(self.next_move[successor[0].colour])

