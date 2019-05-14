import queue

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

NEWGOAL = {
    "red": [
        (3, -3),
        (3, 0)
    ],
    "green": [
        (-3, 3),
        (0, 3)
    ],
    "blue": [
        (0, -3),
        (-3, 0)
    ]
}

# related to logger
MORE_RW = 10
LESS_RW = 100
EXIT_RW = 100
D_HEURISTIC = 5
D_HEURISTIC_HORIZONTAL = 1

# related to maxn
TRADE_OFF = -0.3

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

GREEN_MAIN = [
    "green",
    "blue",
    "red"
]

MAIN = {
    "red": RED_MAIN,
    "green": GREEN_MAIN,
    "blue": BLUE_MAIN
}

COST = {
    "red": {},
    "blue": {},
    "green": {}
}


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
        else:
            # check jump action
            if jump_action in current_board and current_board[jump_action] == "empty" and piece_valid(jump_action):
                next_coords.append((piece, jump_action, 2, (move_action)))

    # return allMoves and the flag indicates if they can be achieved by move or jump
    # 1 or 2
    return next_coords


def cost_from_goal(goal: tuple, tmp_current_board: dict, colour) -> None:
    """
    Receive a goal coordinate and block list then calculate a pre
    """

    q = queue.Queue()

    # (cost_from_goal, ((MOVE_counter, JUMP_counter), coordinates))
    q.put((0, ((0, 0), goal)))

    cost = {goal: 0}

    COST[colour][goal][goal] = 1

    while not q.empty():

        current = q.get()

        successors = find_next(current[1][1], tmp_current_board)
        child_cost = current[0] + 1

        for s in successors:
            if s[1] not in cost:
                # since we are using BFS to findNext the coordinates
                # better solution will be always expanded first

                # s[1] indicates if the next move s is achieved by move (1) or jump (2)
                # used in calculating heuristic g
                # which separately consider jump and moves since jump does not need to /2
                # to reach a admissible heuristic
                # toSuc = (MOVE_counter, JUMP_counter) <- counting both moves and jumps
                if s[2] == 1:
                    s_counter = (current[1][0][0] + 1, current[1][0][1])
                elif s[2] == 2:
                    s_counter = (current[1][0][0], current[1][0][1] + 1)

                q.put((child_cost, (s_counter, s[1])))
                cost[s[1]] = child_cost

                # if the cost less then update the closest cost
                h = s_counter[0] + 1

                '''if s_counter[0] % 2 == 0:
                    h = h + (s_counter[0] / 2 + s_counter[1] + 1)
                else:
                    h = h + ((s_counter[0] - 1) / 2 + s_counter[1] + 2)'''

                if s[1] not in COST[colour][goal]:
                    COST[colour][goal][s[1]] = h
                elif COST[colour][goal][s[1]] > h:
                    COST[colour][goal][s[1]] = h

    return


tmp_current_board = {x: "empty" for x in CELLS}

for g in NEWGOAL:
    for go in NEWGOAL[g]:
        COST[g][go] = {}
        cost_from_goal(go, tmp_current_board, g)

current_go = {
    "red": GOALS["red"][0],
    "green": GOALS["green"][0],
    "blue": GOALS["blue"][0]
}
