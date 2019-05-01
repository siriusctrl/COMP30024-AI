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

MORE_RW = 0
LESS_RW = 0
EXIT_RW = 0.25
D_HEURISTIC = 0
D_HEURISTIC_HORIZONTAL = 0

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