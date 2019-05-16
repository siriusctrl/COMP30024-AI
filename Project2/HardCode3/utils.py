import HardCode3.config as config
import copy


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
    return piece in config.CELLS


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


def calculate_related(current_board, next_board, colour, colour_exit, colour_p, action, arrange, turn, exit_this=False, offset=0):
    rew = 0

    reduced_heu = calculate_reduced_heuristic(current_board, next_board, colour, colour_exit[colour])

    log_uti = []

    piece_difference = calculate_piece_difference(current_board, next_board, colour)
    danger_piece = calculate_danger(current_board, next_board, colour, colour_exit)
    other_rheu = calculate_otherreducedheu(current_board, next_board, colour, colour_exit)
    close = calculate_close(current_board, next_board, colour, colour_exit)
    utility_value = hard_code_eva_function(piece_difference, reduced_heu, danger_piece, 
                                colour_p[colour], colour_exit[colour], action,
                                other_rheu, turn, close, offset)


    return [rew, reduced_heu, log_uti, utility_value]


def heuristic(players, colour, player_exit):
    h = 0

    tmp_h = []

    for p in players:
        tmp_h.append(config.COST[colour][p])

    tmp_h.sort()

    if len(players) + player_exit >= 4:
        h = sum(tmp_h[:4 - player_exit])
    else:
        h = sum(tmp_h)
        h += (4 - (len(players) + player_exit)) * 15

    return h


def get_next_curbo(current_board, action, colour):
    next_board = copy.deepcopy(current_board)

    if action[0] in ("MOVE", "JUMP"):
        next_board[action[1][0]] = "empty"
        next_board[action[1][1]] = colour
        if action[0] in ("JUMP",):
            fr = action[1][0]
            to = action[1][1]
            sk = (fr[0] + (to[0] - fr[0]) / 2, fr[1] + (to[1] - fr[1]) / 2)

            # well I dont freaking know what im thinking about
            if next_board[sk] != "empty" and next_board[sk] != colour:
                next_board[sk] = colour

    elif action[0] in ("EXIT",):
        next_board[action[1]] = "empty"

    return next_board


'''
    calculation of variables used in eval func
'''
def calculate_piece_difference(cur_state, next_state, colour):
    cur_pieces = [k for k in cur_state.keys() if cur_state[k] != "empty" and cur_state[k] == colour]
    next_pieces = [k for k in next_state.keys() if next_state[k] != "empty" and next_state[k] == colour]

    cur_pieces_board = len(cur_pieces)
    next_pieces_board = len(next_pieces)
    return next_pieces_board - cur_pieces_board


def calculate_danger(cur_state, next_state, colour, colour_exit):
    next_players = [k for k in next_state.keys() if next_state[k] == colour]
    next_players.sort(key=lambda x: importance_of_pa(x, colour))

    need = 4 - colour_exit[colour]
    next_players = next_players[:need]

    next_others = [k for k in next_state.keys() if next_state[k] != "empty" and next_state[k] != colour]

    tmp_current_board = {x: "empty" for x in config.CELLS}
    for p in next_players:
        tmp_current_board[p] = "n"
    for p in next_others:
        tmp_current_board[p] = "n"

    dengr = set({})

    for p in next_others:
        p_next_action = find_next(p, tmp_current_board)
        for action in p_next_action:
            if action[2] == 2:
                if action[3] in next_players:
                    dengr.add(action[3])

    return len(dengr)


def calculate_reduced_heuristic(cur_state, next_state, colour, player_exit):
    cur_pieces = [x for x in cur_state.keys() if cur_state[x] == colour]
    next_pieces = [x for x in next_state.keys() if next_state[x] == colour]

    cur_heuri = heuristic(cur_pieces, colour, player_exit)
    nxt_heuri = heuristic(next_pieces, colour, player_exit)

    return nxt_heuri - cur_heuri


'''
    eval func
'''

def hard_code_eva_function(pieces_difference: int, reduced_heuristic: float, danger_pieces: int, players, player_exit,
                           action, other_rheu, turn, close, offset: float) -> float:
    """
    1. # possible safety movement (*1)
    2. reduced heuristic to dest (positive means increased, negative means decreased) *(-2)
    3. # of piece in danger (could be taken by opponent by one JUMP action) *(-5)
    """
    # print(pieces_difference, reduced_heuristic, danger_pieces)
    t = len(players) + player_exit

    if player_exit == 4:
        return 99999

    others = sum(other_rheu.values())

    res = 0 - offset

    if action[0] == "EXIT" and (t >= 4):
        res += 35

    if t < 4:
        res += 30 * pieces_difference + (-1) * reduced_heuristic + danger_pieces * (-20)
    elif t == 4:
        res += 1 * pieces_difference + max((danger_pieces - max(0, pieces_difference)), 0) * (-25)

        if turn > 15:
            res += close * (-0.1) + (-8) * reduced_heuristic + 0.5 * others
        else:
            res += close * (-0.4) + (-2) * reduced_heuristic + 0.5 * others
    else:

        res += 1 * pieces_difference + max((danger_pieces - max(0, pieces_difference)), 0) * (-15) + 0.5 * others

        if turn > 15:
            res += close * (-0.1) + (-8) * reduced_heuristic
        else:
            res += close * (-0.4) + (-2) * reduced_heuristic
    return res


def calculate_close(cur_state, next_state, colour, colour_exit):
    need = 4 - colour_exit[colour]
    next_players = [x for x in next_state.keys() if next_state[x] == colour]

    if (need == 0) or (len(next_players) == 0):
        return 0

    next_players.sort(key=lambda x: importance_of_pa(x, colour))
    next_players = next_players[:need]

    alldist = cal_all_distance(next_players, next_players[0])

    return alldist


def calculate_otherreducedheu(cur_state, next_state, colour, colour_exit):
    colours = ["red", "green", "blue"]
    colours.remove(colour)

    c_rh = {}
    for c in colours:
        c_rh[c] = calculate_reduced_heuristic(cur_state, next_state, c, colour_exit[c])

    return c_rh


def cal_all_distance(next_players, player):
    player_transformed = player[0], -(player[0] + player[1]), player[1]
    distance = 0

    for next_player in next_players:
        next_player_ted = next_player[0], -(next_player[0] + next_player[1]), next_player[1]

        dis = (abs(player_transformed[0] - next_player_ted[0]) + abs(player_transformed[1] - next_player_ted[1]) + abs(player_transformed[2] - next_player_ted[2])) / 2

        distance += dis

    return distance


def importance_of_pa(pa, colour):
    return config.COST[colour][pa]
