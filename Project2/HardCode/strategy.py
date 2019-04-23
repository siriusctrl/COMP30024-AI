import VanGame.utils as utils
import random
import math


def get_possible_moves(current_board, colour, colour_p, goal):

    ps = colour_p[colour]

    for a in ps:
        if a in goal:
            return "EXIT", a

    all_ms = []
    for p in ps:
        all_ms = all_ms + utils.find_next(p, current_board)
    
    print(all_ms)

    if len(all_ms):
        cm = all_ms[math.floor(random.random() * len(all_ms))]
        if cm[2] == 1:
            return "MOVE", (cm[0], cm[1])
        elif cm[2] == 2:
            return "JUMP", (cm[0], cm[1])
        # return all_ms[math.floor(random.random() * len(all_ms))]
    else:
        return "PASS", None

    pass


def hard_code_eva_function(possible_safe : int, reduced_heuristic : float, danger_pieces : int) -> float:
    """
    1. # possible safety movement (*1)
    2. reduced heuristic to dest (positive means increased, negative means decreased) *(-2)
    3. # of piece in danger (could be taken by opponent by one JUMP action) *(-5)
    """
    return possible_safe + (-2)*reduced_heuristic + danger_pieces * (-5)
