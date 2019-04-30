import numpy as np
import os
import json

# define the boundary of the board
CELLS = sorted([(q, r) for q in range(-3, +3 + 1) for r in range(-3, +3 + 1) if -q - r in range(-3, +3 + 1)])

P_MAPPING = {
    "red": 1,
    "green": 2,
    "blue": 3,
    "empty": 0
}

START = {
    'red': [(-3, 3), (-3, 2), (-3, 1), (-3, 0)],
    'green': [(0, -3), (1, -3), (2, -3), (3, -3)],
    'blue': [(3, 0), (2, 1), (1, 2), (0, 3)],
}

# goals of players in each color
GOALS = {
        "red": [
            (3, -3),
            (3, -2),
            (3, -1),
            (3, 0)
        ],
        "green": [
            (-3, 3),
            (-2, 3),
            (-1, 3),
            (0, 3)
        ],
        "blue": [
            (0, -3),
            (-1, -2),
            (-2, -1),
            (-3, 0)
        ]
    }

MORE_RW = 5
LESS_RW = 15
EXIT_RW = 100
D_HEURISTIC = -30
D_HEURISTIC_HORIZONTAL = D_HEURISTIC / 5

RED_MAIN = [
            "red",
            "green",
            "blue"
        ]

BLUE_MAIN = [
    "blue",
    "red",
    "green"
]

GREEN_MAIN= [
    "green",
    "blue",
    "red"
]

MAIN = {
    "red": RED_MAIN,
    "green": GREEN_MAIN,
    "blue": BLUE_MAIN
}


def print_board(board_dict: dict, message: str = "", debug: bool = False, **kwargs) -> None:
    """
    Helper function to print a drawing of a hexagonal board's contents.
    """

    # Set up the board template:
    if not debug:
        # Use the normal board template (smaller, not showing coordinates)
        template = """# {0}
    #           .-'-._.-'-._.-'-._.-'-.
    #          |{16:}|{23:}|{29:}|{34:}| 
    #        .-'-._.-'-._.-'-._.-'-._.-'-.
    #       |{10:}|{17:}|{24:}|{30:}|{35:}| 
    #     .-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
    #    |{05:}|{11:}|{18:}|{25:}|{31:}|{36:}| 
    #  .-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
    # |{01:}|{06:}|{12:}|{19:}|{26:}|{32:}|{37:}| 
    # '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
    #    |{02:}|{07:}|{13:}|{20:}|{27:}|{33:}| 
    #    '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
    #       |{03:}|{08:}|{14:}|{21:}|{28:}| 
    #       '-._.-'-._.-'-._.-'-._.-'-._.-'
    #          |{04:}|{09:}|{15:}|{22:}|
    #          '-._.-'-._.-'-._.-'-._.-'"""
    else:
        # Use the debug board template (larger, showing coordinates)
        template = """# {0}
    #              ,-' `-._,-' `-._,-' `-._,-' `-.
    #             | {16:} | {23:} | {29:} | {34:} | 
    #             |  0,-3 |  1,-3 |  2,-3 |  3,-3 |
    #          ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-.
    #         | {10:} | {17:} | {24:} | {30:} | {35:} |
    #         | -1,-2 |  0,-2 |  1,-2 |  2,-2 |  3,-2 |
    #      ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-. 
    #     | {05:} | {11:} | {18:} | {25:} | {31:} | {36:} |
    #     | -2,-1 | -1,-1 |  0,-1 |  1,-1 |  2,-1 |  3,-1 |
    #  ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-.
    # | {01:} | {06:} | {12:} | {19:} | {26:} | {32:} | {37:} |
    # | -3, 0 | -2, 0 | -1, 0 |  0, 0 |  1, 0 |  2, 0 |  3, 0 |
    #  `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' 
    #     | {02:} | {07:} | {13:} | {20:} | {27:} | {33:} |
    #     | -3, 1 | -2, 1 | -1, 1 |  0, 1 |  1, 1 |  2, 1 |
    #      `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' 
    #         | {03:} | {08:} | {14:} | {21:} | {28:} |
    #         | -3, 2 | -2, 2 | -1, 2 |  0, 2 |  1, 2 | key:
    #          `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' ,-' `-.
    #             | {04:} | {09:} | {15:} | {22:} |   | input |
    #             | -3, 3 | -2, 3 | -1, 3 |  0, 3 |   |  q, r |
    #              `-._,-' `-._,-' `-._,-' `-._,-'     `-._,-'"""

    # prepare the provided board contents as strings, formatted to size.
    ran = range(-3, +3 + 1)
    cells = []
    for qr in [(q, r) for q in ran for r in ran if -q - r in ran]:
        if qr in board_dict:
            cell = str(board_dict[qr]).center(5)
        else:
            cell = "     "  # 5 spaces will fill a cell
        cells.append(cell)

    # fill in the template to create the board drawing, then print!
    board = template.format(message, *cells)
    print(board, **kwargs)


def piece_valid(piece: tuple) -> bool:
    """
    return True only if the given piece are still on the board or
    move to a unoccupied grid
    """
    return piece in CELLS


def find_next(piece: tuple, current_board: dict) -> list:
    """
    this method are trying to find all the possible movement for
    the give coordinate on the board.
    """

    # distance that can be reached by action MOVE
    move = [
        [0, -1],
        [1, -1],
        [1, 0],
        [0, 1],
        [-1, 1],
        [-1, 0]
    ]

    next_coords = []
    directions = 6

    for i in range(directions):
        # check move action
        move_action = (piece[0] + move[i][0], piece[1] + move[i][1])
        jump_action = (piece[0] + 2 * move[i][0], piece[1] + 2 * move[i][1])

        if move_action in current_board and current_board[move_action] == "empty" and piece_valid(move_action):
            next_coords.append((piece, move_action, 1, (-1, -1)))
        elif piece_valid(move_action) and current_board[move_action] != "empty":
            # check jump action
            if jump_action in current_board and current_board[jump_action] == "empty" and piece_valid(jump_action):
                next_coords.append((piece, jump_action, 2, (move_action)))

    # return allMoves and the flag indicates if they can be achieved by move or jump
    # 1 or 2
    return next_coords


def generate_record(record) -> None:
    """
    TODO:  open the file add the record to the end of the file and then close it
    """
    with open("replay.txt", 'w+') as f:
        for r in record:
            f.writelines(r)


def discount_rewards(rewards, discount_rate):
    discounted_rewards = np.empty(len(rewards))
    cumulative_reward = 0
    for step in reversed(range(len(rewards))):
        cumulative_rewards = rewards[step] + cumulative_reward * discount_rate
        discounted_rewards[step] = cumulative_rewards
    return discounted_rewards


def load_l(path):
    rex = {'green': 1, 'red': 2, 'blue': 3, 'empty': 0}
    fn = os.path.basename(path)
    a_ca = fn.split("cao")
    t = a_ca[1]
    colour = t[:t.index("jiba")]

    with open(path, "r") as f:
        data = json.load(f)
        for m in range(len(data)):
            data[m]["board"] = {to_array(a): rex[data[m]["board"][a]] for a in data[m]["board"].keys()}

        datafin = data
    
    return datafin, rex[colour]

def to_array(s_t):
    splited_dict = s_t.split(", ")
    first = splited_dict[0][1:]
    secon = splited_dict[1][:-1]

    return (int(first), int(secon))


def chose(options: list):
    ops = np.array(options)
    ops = (ops - ops.mean()) / ops.std()
    prob = softmax(np.array(ops))
    # print("\n", options, "\n", prob, "\n")
    prob = prob.reshape(len(prob),)
    # print(prob.shape)

    return np.random.choice(len(options), 1, p=prob)[0]
    # return np.argmax(prob)


def softmax(x):
    """Compute softmax values for each sets of scores in x."""
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum(axis=0)


class Linear:

    @staticmethod
    def forward(x):
        return x

    @staticmethod
    def backward(x):
        return x


class ReLu:
    """
    Two additional major benefits of ReLUs are sparsity and a reduced
    likelihood of vanishing gradient. But first recall the definition
    of a ReLU is :math:`h=max(0,a)` where :math:`a=Wx+b`.
    One major benefit is the reduced likelihood of the gradient to vanish.
    This arises when :math:`a>0`. In this regime the gradient has a constant value.
    In contrast, the gradient of sigmoid becomes increasingly small as the
    absolute value of :math:`x` increases. The constant gradient of ReLUs results in
    faster learning.

    The other benefit of ReLUs is sparsity. Sparsity arises when :math:`a≤0`.
    The more such units that exist in a layer the more sparse the resulting
    representation. Sigmoid on the other hand are always likely to generate
    some non-zero value resulting in dense representations. Sparse representations
    seem to be more beneficial than dense representations.
    """

    @staticmethod
    def forward(x):
        return np.maximum(0.0, x)

    @staticmethod
    def backward(a, x):
        ap = np.array(a, copy=True)
        ap[x <= 0] = 0
        return ap
