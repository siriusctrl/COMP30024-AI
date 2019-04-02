import os
import numpy as np
import math
import node
import heapq

def print_board(board_dict:dict, message:str="", debug:bool=False, **kwargs):
    """
    Helper function to print a drawing of a hexagonal board's contents.

    Arguments:

    * `board_dict` -- dictionary with tuples for keys and anything printable
    for values. The tuple keys are interpreted as hexagonal coordinates (using 
    the axial coordinate system outlined in the project specification) and the 
    values are formatted as strings and placed in the drawing at the corres- 
    ponding location (only the first 5 characters of each string are used, to 
    keep the drawings small). Coordinates with missing values are left blank.

    Keyword arguments:

    * `message` -- an optional message to include on the first line of the 
    drawing (above the board) -- default `""` (resulting in a blank message).
    * `debug` -- for a larger board drawing that includes the coordinates 
    inside each hex, set this to `True` -- default `False`.
    * Or, any other keyword arguments! They will be forwarded to `print()`.
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
    ran = range(-3, +3+1)
    cells = []
    for qr in [(q,r) for q in ran for r in ran if -q-r in ran]:
        if qr in board_dict:
            cell = str(board_dict[qr]).center(5)
        else:
            cell = "     " # 5 spaces will fill a cell
        cells.append(cell)

    # fill in the template to create the board drawing, then print!
    board = template.format(message, *cells)
    print(board, **kwargs)

def harmonic_mean(nums:list) -> float:
    """
    find the harmoic mean of a list a number
    """

    n = len(nums)
    return n/sum([1/i for i in nums])

def eud(p1:tuple, p2:tuple) -> float:
    """
    calculate the euclidean distance between two point
    """
    return math.sqrt(sum([(i-j)**2 for i,j in zip(p1,p2)]))

def initialNode(inputBoard: dict):
    COLOURS = {
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

    initialSt = {}
    initialSt["players"] = [tuple(x) for x in inputBoard["pieces"]]
    initialSt["goals"] = COLOURS[inputBoard["colour"]]
    initialSt["blocks"] = [tuple(x) for x in inputBoard["blocks"]]

    initialNd = node.Node(state=initialSt)

    # remove unachiavable goals
    for i in initialSt["blocks"]:
        if i in initialNd.state['goals']:
            initialNd.state['goals'].remove(i)

    return initialNd


def findHubNode(destinations:[node.Node]) -> [node.Node]:
    frontier = []
    visited = {}
    findAll = False  # a flag to indicate whether we finish a layer or not if we find a target node
    res = []

    for i in destinations:
        visited[tuple(sorted(i.state["players"]))] = i
        heapq.heappush(frontier, (i.g, i))

    layer = 0

    while True:
        if len(frontier) == 0:
            return res

        if findAll and (layer < frontier[0][1]):
            return res

        current = heapq.heappop(frontier)[1]

        successors = current.expand()

        if (len(successors) > 2):
            findAll = True
            layer = current.g
            res.append(current)
        
        if not findAll:
            for i in successors:
                if tuple(sorted(i.state["players"])) not in visited:
                    heapq.heappush(frontier, (i.g, i))

        