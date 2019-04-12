import queue
import node

# define the boundary of the board
CELLS = set([(q, r) for q in range(-3, +3 + 1) for r in range(-3, +3 + 1) if -q - r in range(-3, +3 + 1)])

# steps requirement for one piece move from any grid to the closest destination
COST = {}


def print_board(board_dict: dict, message: str = "", debug: bool = False, **kwargs) -> None:
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


def find_next(piece: tuple, parent: tuple, blocks: list) -> list:
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

    # distance that can be reached by action JUMP
    jump = [
        [0, -2],
        [2, -2],
        [2, 0],
        [0, 2],
        [-2, 2],
        [-2, 0]
    ]

    next_coords = []
    directions = 6
    current_coord = piece

    for i in range(directions):
        # check move action
        move_action = (current_coord[0] + move[i][0], current_coord[1] + move[i][1])

        if (move_action not in blocks) and move_action != parent and piece_valid(move_action):
            next_coords.append((move_action, 1))
        else:
            # check jump action
            jump_action = (current_coord[0] + jump[i][0], current_coord[1] + jump[i][1])
            if (jump_action not in blocks) and jump_action != parent and piece_valid(jump_action):
                next_coords.append((jump_action, 2))

    # return allMoves and the flag indicates if they can be achieved by move or jump
    # 1 or 2
    return next_coords


def root_init(input_board: dict) -> 'node':
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

    initial_state = {
        "players": set([tuple(x) for x in input_board["pieces"]]),
        "goals": COLOURS[input_board["colour"]],
        "blocks": set([tuple(x) for x in input_board["blocks"]])
    }

    # remove unachievable goals
    for i in initial_state["blocks"]:
        if i in initial_state['goals']:
            initial_state['goals'].remove(i)

    for g in initial_state['goals']:
        cost_from_goal(g, initial_state["blocks"])

    initial_root = node.Node(state=initial_state)

    return initial_root


def cost_from_goal(goal: tuple, block: list) -> None:
    """
    Receive a goal coordinate and block list then calculate a pre
    """

    q = queue.Queue()

    # (cost_from_goal, ((MOVE_counter, JUMP_counter), coordinates))
    q.put((0, ((0, 0), goal)))

    cost = {goal: 0}

    COST[goal] = 1

    while not q.empty():

        current = q.get()

        successors = find_next(current[1][1], None, block)
        child_cost = current[0] + 1

        for s in successors:
            if s[0] not in cost:
                # since we are using BFS to findNext the coordinates
                # better solution will be always expanded first

                # s[1] indicates if the next move s is achieved by move (1) or jump (2)
                # used in calculating heuristic g
                # which separately consider jump and moves since jump does not need to /2
                # to reach a admissible heuristic
                # toSuc = (MOVE_counter, JUMP_counter) <- counting both moves and jumps
                if s[1] == 1:
                    s_counter = (current[1][0][0] + 1, current[1][0][1])
                elif s[1] == 2:
                    s_counter = (current[1][0][0], current[1][0][1] + 1)

                q.put((child_cost, (s_counter, s[0])))
                cost[s[0]] = child_cost

                # if the cost less then update the closest cost
                h = 0

                if s_counter[0] % 2 == 0:
                    h = h + (s_counter[0] / 2 + s_counter[1] + 1)
                else:
                    h = h + ((s_counter[0] - 1) / 2 + s_counter[1] + 2)

                if s[0] not in COST:
                    COST[s[0]] = h
                elif COST[s[0]] > h:
                    COST[s[0]] = h

    return

