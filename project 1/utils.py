import os, queue
import math
import node
import heapq

# define the boundary of the board
CELLS = set([(q,r) for q in range(-3, +3+1) for r in range(-3, +3+1) if -q-r in range(-3, +3+1)])

COST = {}

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

def pieceValid(piece: tuple) -> bool:
    return piece in CELLS

def expand(piece: tuple, parent: tuple, blocks: list) -> list:
    """
    this method are tring to find all the possible movement for
    all the avaliable pieces on the board as next possible
    states based on the current position of pieces, and trate
    them like the child of this node.
    """
    # TODO: also need to consider when pieces can exit the board
    nearSix = [
        [0, -1],
        [1, -1],
        [1, 0],
        [0, 1],
        [-1, 1],
        [-1, 0]
    ]

    further = [
        [0, -2],
        [2, -2],
        [2, 0],
        [0, 2],
        [-2, 2],
        [-2, 0]
    ]

    # allMoves = dict()
    allMoveNodes = []
    numOfAllPossible = 6
    tmpPiece = tuple(piece + ())
        # tmpCanMovePieces = []
        

    for i in range(numOfAllPossible):
        checkingCoordin = (tmpPiece[0] + nearSix[i][0], tmpPiece[1] + nearSix[i][1])
        if (not (checkingCoordin in blocks)) and checkingCoordin != parent and pieceValid(checkingCoordin):
            allMoveNodes.append(checkingCoordin)
        else:
            furtherCoordin = (tmpPiece[0] + further[i][0], tmpPiece[1] + further[i][1])
            if (not (furtherCoordin in blocks)) and furtherCoordin != parent and pieceValid(furtherCoordin):
                allMoveNodes.append(furtherCoordin)

    # allMoves[tmpPiece] = tmpCanMovePieces

    # return allMoves
    return allMoveNodes


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

    # remove unachiavable goals
    for i in initialSt["blocks"]:
        if i in initialSt['goals']:
            initialSt['goals'].remove(i)

    distances = {}

    for g in initialSt['goals']:
        distances[g] = costFromGoal(g, initialSt['blocks'])
    

    for k in distances[initialSt['goals'][0]].keys():
        dis = []
        for g in initialSt['goals']:
            dis.append(distances[g][k])
        COST[k] = min(dis)


    initialNd = node.Node(state=initialSt)

    return initialNd


def costFromGoal(goal:tuple, block) -> dict:
    q = queue.Queue()
    cost = {}
    q.put((0,goal))

    cost[goal] = 0

    while not q.empty():

        current = q.get()
        # (cost, coordinates)
        successors = expand(current[1], None, block)
        child_cost = current[0] + 1

        for s in successors:
            if s in cost:
                if cost[s] > child_cost:
                    cost[s] = child_cost
                    q.put((child_cost, s))
                    print("pass")
            else:
                q.put((child_cost, s))
                cost[s] = child_cost

    return cost
        

        