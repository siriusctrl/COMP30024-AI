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


def cal_all(current_board, next_bor, colour, colour_e, colour_p, action, arrange, tun, exit_this=False, offset=0):
    rew = 0

    d_heurii = cal_rheu(current_board, next_bor, colour, colour_e[colour])

    if exit_this:
        rew += config.EXIT_RW
    else:
        pass

    log_uti = get_utility(current_board, next_bor, colour, d_heurii, colour_e, arrange)

    piece_difference = cal_pdiff(current_board, next_bor, colour)
    danger_piece = cal_dpiei(current_board, next_bor, colour, colour_e)

    other_rheu = cal_otherrheu(current_board, next_bor, colour, colour_e)

    et = False

    if action[0] in ("JUMP",):
        fr = action[1][0]
        to = action[1][1]
        sk = (fr[0] + (to[0] - fr[0]) / 2, fr[1] + (to[1] - fr[1]) / 2)
        if next_bor[sk] == colour and current_board[sk] != next_bor[sk]:
            et = True
    close = cal_clo(current_board, next_bor, colour, colour_e)

    ev = hard_code_eva_function(piece_difference, d_heurii, danger_piece, colour_p[colour], colour_e[colour], action,
                                other_rheu, tun, close, offset)
    rew += check_heuristic_rew(colour_e, next_bor, colour, d_heurii)

    # if ev == -1:
    # print_board(current_board)
    # print_board(next_bor)
    # print(colour)
    # print("============")

    return [rew, d_heurii, log_uti, ev]


def get_utility(current_board, suc_bo, colour, re, colour_ea, arrange):
    piece_difference = cal_pdiff(current_board, suc_bo, colour)
    danger_piece = cal_dpiei(current_board, suc_bo, colour, colour_ea)

    utility = [
        re,
        piece_difference,
        danger_piece
    ]

    utility += player_es(colour_ea, False, arrange)

    utility += cal_heuristic(suc_bo, colour, colour_ea, arrange)

    return utility


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
    t_cur = copy.deepcopy(current_board)

    if action[0] in ("MOVE", "JUMP"):
        t_cur[action[1][0]] = "empty"
        t_cur[action[1][1]] = colour
        if action[0] in ("JUMP",):
            fr = action[1][0]
            to = action[1][1]
            sk = (fr[0] + (to[0] - fr[0]) / 2, fr[1] + (to[1] - fr[1]) / 2)

            # well I dont freaking know what im thinking about
            if t_cur[sk] != "empty" and t_cur[sk] != colour:
                t_cur[sk] = colour

    elif action[0] in ("EXIT",):
        t_cur[action[1]] = "empty"

    return t_cur


def player_es(colour_e, exit_this, arrange):
    # only red here wait for more colours
    rest_ps = [colour_e[k] for k in arrange]

    if exit_this:
        rest_ps[0] = rest_ps[0] + 1

    return rest_ps


def cal_heuristic(suc_bo, colour, colour_exit, arrange):
    heuris = [heuristic([x for x in suc_bo.keys() if suc_bo[x] == c], c, colour_exit[c]) for c in arrange]
    return heuris


'''
    calculation of variables used in eval func
'''


def cal_pdiff(cur_state, next_state, colour):
    c_or = [k for k in cur_state.keys() if cur_state[k] != "empty" and cur_state[k] == colour]
    n_r = [k for k in next_state.keys() if next_state[k] != "empty" and next_state[k] == colour]

    c_ors = len(c_or)
    n_s = len(n_r)
    return n_s - c_ors


def cal_dpiei(cur_state, next_state, colour, colour_e):
    nxt_pl = [k for k in next_state.keys() if next_state[k] == colour]
    nxt_pl.sort(key=lambda x: importance_of_pa(x, colour))

    need = 4 - colour_e[colour]
    nxt_pl = nxt_pl[:need]

    nxt_ot = [k for k in next_state.keys() if next_state[k] != "empty" and next_state[k] != colour]

    tmp_current_board = {x: "empty" for x in config.CELLS}
    for p in nxt_pl:
        tmp_current_board[p] = "n"
    for p in nxt_ot:
        tmp_current_board[p] = "n"

    dengr = set({})

    for p in nxt_ot:
        p_nxt = find_next(p, tmp_current_board)
        for d in p_nxt:
            if d[2] == 2:
                if d[3] in nxt_pl:
                    dengr.add(d[3])

    return len(dengr)


def cal_rheu(cur_state, next_state, colour, player_exit):
    cur_pl = [x for x in cur_state.keys() if cur_state[x] == colour]
    nxt_pl = [x for x in next_state.keys() if next_state[x] == colour]

    cur_heuri = heuristic(cur_pl, colour, player_exit)
    nxt_heuri = heuristic(nxt_pl, colour, player_exit)

    return nxt_heuri - cur_heuri


'''
    eval func
'''


def hard_code_eva_function(pieces_difference: int, reduced_heuristic: float, danger_pieces: int, players, player_exit,
                           action, other_rheu, tun, close, offset: float) -> float:
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
        res += 30 * pieces_difference + (-1) * reduced_heuristic + (danger_pieces - max(0, pieces_difference)) * (-20)
    elif t == 4:
        res += 1 * pieces_difference + (danger_pieces - max(0, pieces_difference)) * (-20) + 1.5 * others
        if tun > 30:
            res += close * (-0.1) + (-1) * reduced_heuristic + 1.5 * others
        else:
            res += close * (-0.8) + (-4) * reduced_heuristic + 1 * others
    else:
        res += 1 * pieces_difference + (danger_pieces - max(0, pieces_difference)) * (-10)
        if tun > 30:
            res += close * (-0.1) + (-1) * reduced_heuristic + 1.5 * others
        else:
            res += close * (-0.8) + (-4) * reduced_heuristic + 1 * others
    return res


def check_heuristic_rew(colour_exit, suc_bo, colour, d_heur):
    n_r = [k for k in suc_bo.keys() if suc_bo[k] != "empty" and suc_bo[k] == colour]
    exited = colour_exit[colour]

    count = exited + len(n_r)

    if d_heur > 0:
        return config.D_HEURISTIC
    elif d_heur == 0:
        return config.D_HEURISTIC_HORIZONTAL

    return 0


def cal_clo(cur_state, next_state, colour, colour_exit):
    need = 4 - colour_exit[colour]
    py = [x for x in next_state.keys() if next_state[x] == colour]

    if (need == 0) or (len(py) == 0):
        return 0

    py.sort(key=lambda x: importance_of_pa(x, colour))

    py = py[:need]

    # consider_num = max(len(py) - need + 1, 1)
    res = []
    # if consider_num > 0:
    # if len(py) < consider_num:
    # print(py, next_state)
    # for i in range(consider_num):
    alldist = cal_all_distance(py, py[0])
    # shit
    # res.append(alldist)

    return alldist


def cal_otherrheu(cur_state, next_state, colour, colour_exit):
    colours = ["red", "green", "blue"]
    colours.remove(colour)

    c_rh = {
    }

    for c in colours:
        c_rh[c] = cal_rheu(cur_state, next_state, c, colour_exit[c])

    return c_rh


def cal_all_distance(py, pa):
    thr = pa[0], -(pa[0] + pa[1]), pa[1]
    din = 0
    for pj in py:
        pjt = pj[0], -(pj[0] + pj[1]), pj[1]

        dn = (abs(thr[0] - pjt[0]) + abs(thr[1] - pjt[1]) + abs(thr[2] - pjt[2])) / 2

        din += dn

    return din


def importance_of_pa(pa, colour):
    return config.COST[colour][pa]
