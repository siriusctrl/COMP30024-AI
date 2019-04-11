import os, queue
import math
import node
import heapq

# define the boundary of the board
CELLS = set([(q,r) for q in range(-3, +3+1) for r in range(-3, +3+1) if -q-r in range(-3, +3+1)])

# steps requirment for one piece move from any grid to the cloest destination
COST = {}

def print_board(board_dict:dict, message:str="", debug:bool=False, **kwargs) -> None :
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
    """
    return True only if the given piece are still on the board or 
    move to a unoccupied grid
    """

    return piece in CELLS


def findNext(piece: tuple, parent: tuple, blocks: list) -> list:
    """
    this method are tring to find all the possible movement for
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

    # distance that can be reached by action JUMP
    jump = [
        [0, -2],
        [2, -2],
        [2, 0],
        [0, 2],
        [-2, 2],
        [-2, 0]
    ]

    nextPositions = []
    directions = 6
    currentPosition = piece

    for i in range(directions):
        # check single move
        checkingCoordin = (currentPosition[0] + move[i][0], currentPosition[1] + move[i][1])
        if (not (checkingCoordin in blocks)) and checkingCoordin != parent and pieceValid(checkingCoordin):
            nextPositions.append((checkingCoordin, 1))
        else:
            # check jump
            furtherCoordin = (currentPosition[0] + jump[i][0], currentPosition[1] + jump[i][1])
            if (not (furtherCoordin in blocks)) and furtherCoordin != parent and pieceValid(furtherCoordin):
                nextPositions.append((furtherCoordin, 2))

    # return allMoves and the flag indicates if they can be achieved by move or jump
    # 1 or 2
    return nextPositions


def initialRoot(inputBoard: dict) -> node.Node:
    """
    the root of the tree will be init here
    
    `inputBoard` -- the input board which read from the json file

    """

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

    for g in initialSt['goals']:
        costFromGoal(g, initialSt["blocks"])

    initialRoot = node.Node(state=initialSt)

    return initialRoot


def costFromGoal(goal:tuple, block:list) -> dict:
    """
    Receive a goal coordiate 
    """

    q = queue.Queue()
    q.put((0, ((0, 0),goal)))

    COST[goal] = (0, 0)

    while not q.empty():

        current = q.get()
        # (cost, coordinates)
        successors = findNext(current[1][1], None, block)
        child_cost = current[0] + 1

        for s in successors:
            if s[0] not in COST:
                # since we are using BFS to findNext the coordinates
                # better solution will be always expanded first

                # s[1] indicates if the next move s is achieved by
                # move or jump
                # 1 for move and 2 for jump
                # used when calculating heuristic g
                # which separately consider jump and moves
                if s[1] == 1:
                    toSuc = (current[1][0][0] + 1, current[1][0][1])
                elif s[1] == 2:
                    toSuc = (current[1][0][0], current[1][0][1] + 1)


                q.put((child_cost, (toSuc, s[0])))

                # if the cost less then update
                if ((s in COST) and sum(COST[s[0]]) > child_cost):
                    COST[s[0]] = toSuc
                if not s in COST:
                    COST[s[0]] = toSuc
                    
    return 0

        