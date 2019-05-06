import queue
import HardCode.utils as utils

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

MORE_RW = 10
LESS_RW = 100
EXIT_RW = 100
D_HEURISTIC = 5
D_HEURISTIC_HORIZONTAL = 1

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

COST = {
            "red": {},
            "blue": {},
            "green": {}
        }

def cost_from_goal(goal: tuple, tmp_current_board: dict, colour) -> None:
        """
        Receive a goal coordinate and block list then calculate a pre
        """

        q = queue.Queue()

        # (cost_from_goal, ((MOVE_counter, JUMP_counter), coordinates))
        q.put((0, ((0, 0), goal)))

        cost = {goal: 0}

        COST[colour][goal] = 1

        while not q.empty():

            current = q.get()

            successors = utils.find_next(current[1][1], tmp_current_board)
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

                    if s[1] not in COST[colour]:
                        COST[colour][s[1]] = h
                    elif COST[colour][s[1]] > h:
                        COST[colour][s[1]] = h

        return

tmp_current_board = {x: "empty" for x in CELLS}


for g in GOALS:
    for go in GOALS[g]:
            cost_from_goal(go, tmp_current_board, g)
