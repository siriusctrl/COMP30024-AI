import copy
import HardCode3.config as config


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
    
    returns:
        list of next moves of all pieces : [(piece, move_to, 1 or 2, skipped piece), ]
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


def calculate_related(current_board, next_board, colour, colour_exit,
                      colour_p, action, turn, exit_this=False, offset=0):
    """
        calculate all related utility values
        but currently, rew and log_uti is ignored and abandoned.

        return a list : [0, reduced heuristic, [], utility value]
    """
    rew = 0

    reduced_heu = calculate_reduced_heuristic(current_board,
                                              next_board, colour, colour_exit[colour])

    log_uti = []

    piece_difference = calculate_piece_difference(current_board,
                                                  next_board, colour)

    danger_piece = calculate_danger(current_board, next_board, colour,
                                    colour_exit)

    other_reduced_heuristic = calculate_others_reduced_heuristic(current_board, next_board, colour,
                                                                 colour_exit)

    close = calculate_close(current_board, next_board, colour,
                            colour_exit)

    utility_value = hard_code_eva_function(piece_difference, reduced_heu,
                                           danger_piece, colour_p[colour],
                                           colour_exit[colour], action, other_reduced_heuristic,
                                           turn, close, offset)

    return [rew, reduced_heu, log_uti, utility_value]


def heuristic(players, colour, player_exit):
    """
        heuristic function

        evaluate how much distance we need to get
        this state to goal state.

        intuitively, its the number of move steps we should further take
        But the value is calculated differently when the
        number of pieces (sum of exits and pieces in board)
        is varied around 4.

        args:
            players: list of coordinates of pieces of colour
            colour: player's colour
            player_exit: colour's count of exits

    """
    h = 0

    # all currently in-board pieces' distance to nearest goals.
    tmp_h = []

    for p in players:
        tmp_h.append(config.COST[colour][p])

    tmp_h.sort()

    # if exits + pieces in board >= 4
    if len(players) + player_exit >= 4:

        # get sum of the least 4 heuristics to be the overall heuristic of current state
        h = sum(tmp_h[:4 - player_exit])
    else:

        # pieces is not enough for winning
        # get sum of all in-board pieces' heuristics and for each of the number of lacking pieces, 15
        # which is the intuitively max steps taking from any where of the board to goal
        h = sum(tmp_h)
        h += (4 - (len(players) + player_exit)) * 15

    return h


def get_next_curbo(current_board, action, colour):
    """
        getting next board given current board and the action to change the board

        args:
            current_board: dict of board, {coordinates: colour, }
            action: action shown in spec, (action type, action params)
            colour: colour of player who did the action
    """

    next_board = copy.deepcopy(current_board)

    if action[0] in ("MOVE", "JUMP"):
        next_board[action[1][0]] = "empty"
        next_board[action[1][1]] = colour

        if action[0] in ("JUMP",):
            fr = action[1][0]
            to = action[1][1]

            # skipped piece
            sk = (fr[0] + (to[0] - fr[0]) / 2, fr[1] + (to[1] - fr[1]) / 2)

            if next_board[sk] != "empty" and next_board[sk] != colour:
                next_board[sk] = colour

    elif action[0] in ("EXIT",):
        next_board[action[1]] = "empty"

    return next_board


def calculate_piece_difference(cur_state, next_state, colour):
    """
        calculate piece difference of player in colour

        args:
            cur_state: dict of current board {coordinates:colour,}
            next_state: dict of next board {coordinates: colour,}
            colour: colour of player who is calculating piece difference
    """

    # current pieces of colour and next pieces of colours
    cur_pieces = [k for k in cur_state.keys() if cur_state[k] != "empty" and cur_state[k] == colour]
    next_pieces = [k for k in next_state.keys() if next_state[k] != "empty" and next_state[k] == colour]

    # numbers of pieces
    cur_pieces_board = len(cur_pieces)
    next_pieces_board = len(next_pieces)

    return next_pieces_board - cur_pieces_board


def calculate_danger(cur_state, next_state, colour, colour_exit):
    """
        danger pieces

        args:
            cur_state: dict of current board {coordinates :colour,}
            next_state: dict of next board {coordinates : colour,}
            colour: colour of player who is calculating piece difference
            colour_exit: all player's count of exits {colour: counts}
    """

    # next state's pieces sorted using importance (heuristic)
    next_players = [k for k in next_state.keys() if next_state[k] == colour]
    next_players.sort(key=lambda x: importance_of_pa(x, colour))

    # number of pieces that needs to calculate
    need = 4 - colour_exit[colour]
    next_players = next_players[:need]

    # others' pieces in board
    next_others = [k for k in next_state.keys() if next_state[k] != "empty" and next_state[k] != colour]

    tmp_current_board = {x: "empty" for x in config.CELLS}

    # tempory board
    for p in next_players:
        tmp_current_board[p] = "n"
    for p in next_others:
        tmp_current_board[p] = "n"

    dengr = set({})

    # for each of other pieces find if they can skip over colour's pieces
    for p in next_others:
        p_next_action = find_next(p, tmp_current_board)
        for action in p_next_action:

            # jump
            if action[2] == 2:
                if action[3] in next_players:
                    dengr.add(action[3])

    return len(dengr)


def calculate_reduced_heuristic(cur_state, next_state, colour, player_exit):
    """
        calculate reduced heuristic

        args:
            cur_state: current state {coordinates: colour}
            next_state: next state {coordinates: colour}
            colour: player's colour
            player_exit: player's exits count
    """

    # pieces in current state and next states
    cur_pieces = [x for x in cur_state.keys() if cur_state[x] == colour]
    next_pieces = [x for x in next_state.keys() if next_state[x] == colour]

    # total heuristics of two states
    cur_heuristic = heuristic(cur_pieces, colour, player_exit)
    nxt_heuristic = heuristic(next_pieces, colour, player_exit)

    return nxt_heuristic - cur_heuristic


def hard_code_eva_function(pieces_difference: int, reduced_heuristic: float, danger_pieces: int, players, player_exit,
                           action, other_reduced_heuristic, turn, close, offset: float) -> float:
    """
        utility

        args:
            pieces_difference: difference of pieces' count of current state and next state
            reduced_heuristic: heuristic difference
            danger_pieces: pieces in danger
            players: list of player's pieces coordinates
            player_exit: player's count of exits
            action: the action take from last state to this state
            other_rheu: other player's reduced heuristic
            turn: turns so far of current game
            close: how close that important pieces are

            more detailed explanation please refer to the report
    """

    # sum of exits and pieces in-board
    t = len(players) + player_exit

    # if the action causes win then just go
    if player_exit == 4:
        return 99999

    # other player's reduced heuristic
    # evaluate if we can stuck others and let them move backwards
    others = sum(other_reduced_heuristic.values())

    res = 0 - offset

    # if a piece can leave we assign it with a slightly higher marks
    # since we prefer it to leave early to gain advantages to win the
    # game unless that action could result in some other bad results
    if action[0] == "EXIT" and (t >= 4):
        res += 35

    # if now lacking pieces to win
    if t < 4:
        # emphasizes getting more pieces and save existing pieces and consider take which piece could
        # give our opponents more pain
        res += 30 * pieces_difference + (-1) * reduced_heuristic + danger_pieces * (-20) + 0.1 * others
    # we have just the right number of piece to win the game
    elif t == 4:
        res += 1 * pieces_difference + max((danger_pieces - max(0, pieces_difference)), 0) * (-25)

        # getting more pieces if we can
        # but more carefully move towards goal
        res += 3 * pieces_difference + max((danger_pieces - max(0, pieces_difference)), 0) * (-25)

        if turn > 15:
            res += close * (-0.1) + (-6) * reduced_heuristic + 0.5 * others
        else:
            res += close * (-0.4) + (-2) * reduced_heuristic + 0.3 * others
    # we now have at least one spare piece in terms of winning the game
    else:
        # do not prefer to get more pieces
        # highly recommend to move toward the goal
        # stuck others
        res += 1 * pieces_difference + max((danger_pieces - max(0, pieces_difference)), 0) * (-15) + 0.3 * others

        if turn > 15:
            res += close * (-0.1) + (-6) * reduced_heuristic
        else:
            res += close * (-0.4) + (-2) * reduced_heuristic
    return res


def calculate_close(cur_state, next_state, colour, colour_exit):
    """
        calculate how close player's pieces are

        args:
            cur_state: dict of all pieces {coordinate: colour
            next_state: dict of all pieces in next state {coordinate: colour}
            colour_exit: dict of players and count of exits {colour: count exits}
            colour: player
    """

    # how much pieces we need to calculate this variable
    need = 4 - colour_exit[colour]
    next_players = [x for x in next_state.keys() if next_state[x] == colour]

    if (need == 0) or (len(next_players) == 0):
        return 0

    # get important players to calculate
    next_players.sort(key=lambda x: importance_of_pa(x, colour))
    next_players = next_players[:need]

    # calculate distances between important players
    cohesive = cal_all_distance(next_players, next_players[0])

    return cohesive


def calculate_others_reduced_heuristic(cur_state, next_state, colour, colour_exit):
    """
        calculate other's reduced heuristics of current state and next state

        args:
            cur_state: dict {coordinate: colour}
            next_state: dict of next state {coordinate: colour}
            colour: player's colour
            colour_exit: dict of player and count exits {colour: exit counts}
    """

    colours = ["red", "green", "blue"]
    colours.remove(colour)

    # for each colour calculate for them
    c_rh = {}
    for c in colours:
        c_rh[c] = calculate_reduced_heuristic(cur_state, next_state, c, colour_exit[c])

    return c_rh


def cal_all_distance(next_players, player):
    """
        calculate distance between next_players and player

        args:
            next_players: list of pieces
            player: piece
    """
    player_transformed = player[0], -(player[0] + player[1]), player[1]
    distance = 0

    for next_player in next_players:
        next_player_ted = next_player[0], -(next_player[0] + next_player[1]), next_player[1]

        dis = (abs(player_transformed[0] - next_player_ted[0]) +
               abs(player_transformed[1] - next_player_ted[1]) +
               abs(player_transformed[2] - next_player_ted[2])) / 2

        distance += dis

    return distance


def importance_of_pa(pa, colour):
    """
        importance of a player in colour

        pa: piece
    """
    return config.COST[colour][pa]
