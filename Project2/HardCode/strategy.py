import HardCode.utils as utils
import HardCode.config as config
import HardCode.logger as logger
import copy
import queue


# 2 utility:
#  pieces less than 4 then up eating utility (include exit pieces)
#  more or equal to 4 then prevent to be eaten
class Strategy:

    def __init__(self, goals, colour):
        self.cost = {
            "red": {},
            "blue": {},
            "green": {}
        }

        self.colour = colour

        self.goals = goals

        self.arrange = config.MAIN[self.colour]

        tmp_current_board = {x: "empty" for x in config.CELLS}

        for g in self.goals:
            self.cost_from_goal(g, tmp_current_board, colour)
        # utils.print_board(self.cost[colour])

        for g in config.GOALS:
            if g != colour:
                for go in config.GOALS[g]:
                    self.cost_from_goal(go, tmp_current_board, g)
                # utils.print_board(self.cost[g])

        self.turn = 0

        self.logger = logger.Logger(self.colour)

    def get_possible_moves(self, current_board, colour, colour_p, goal, colour_e):

        self.turn += 1

        ps = colour_p[colour]

        ot = [y for x in colour_p.keys() for y in colour_p[x] if x != colour]

        action = tuple()

        final_cald = []
        rew = 0
        re = 0

        next_bor = {}

        for a in ps:
            if a in goal:
                action = ("EXIT", a)
                next_bor = self.get_next_curbo(current_board, action, colour)
                final_cald = self.cal_all(current_board, next_bor, colour, colour_e, colour_p, True)
                break

        if len(action) == 0:
            all_ms = []
            for p in ps:
                all_ms = all_ms + utils.find_next(p, current_board)

            if len(all_ms):
                all_state_players = []
                all_calds = []
                all_act = []

                for ms in all_ms:
                    m_action = tuple()
                    if ms[2] == 1:
                        m_action = ("MOVE", (ms[0], ms[1]))
                    elif ms[2] == 2:
                        m_action = ("JUMP", (ms[0], ms[1]))
                    
                    next_bor = self.get_next_curbo(current_board, m_action, colour)

                    # delta heuristic

                    cald = self.cal_all(current_board, next_bor, colour, colour_e,colour_p)

                    d_heurii = cald[0]
                    uti = cald[1]
                    ev = cald[2]

                    all_state_players.append(next_bor)
                    all_calds.append(cald)
                    all_act.append(m_action)

                # print(all_state_players)
                # print(all_state_players, ev)
                
                # print(ev)

                max_e = max(all_calds, key=lambda x: x[ 3])
                ie = all_calds.index(max_e)
                action = all_act[ie]
                final_cald = all_calds[ie]
                next_bor = all_state_players[ie]

            else:
                action = ("PASS", None)
                next_bor = self.get_next_curbo(current_board, action, colour)
                final_cald = self.cal_all(current_board, next_bor, colour, colour_e,colour_p)

        re = final_cald[1]
        utility = final_cald[2]
        ev = final_cald[3]
        rew = final_cald[0]

        self.logger.add_log(next_bor, action=action, rew=rew, d_heur=re, utility=utility, ev=ev, turns=self.turn)
        
        return action

        pass

    def get_utility(self, current_board, suc_bo, colour, re, colour_ea):
        piece_difference = self.cal_pdiff(current_board, suc_bo, colour)
        danger_piece = self.cal_dpiei(current_board, suc_bo ,colour)

        utility = [
                    re,
                    piece_difference,
                    danger_piece
                ]

        utility += self.player_es(colour_ea, False)

        utility += self.cal_heuristic(suc_bo, colour, colour_ea)

        return utility

    def cal_all(self, current_board, next_bor, colour, colour_e, colour_p, exit_this=False):

        rew = 0

        d_heurii = self.cal_rheu(current_board, next_bor, colour, -1)

        colour_ea = colour_e

        if exit_this:
            colour_ea = copy.deepcopy(colour_e)
            colour_ea[colour] += 1
            rew += config.EXIT_RW
            uti = self.get_utility(current_board, next_bor, colour, d_heurii, colour_ea)
        else:
            uti = self.get_utility(current_board, next_bor, colour, d_heurii, colour_e)

        piece_difference = self.cal_pdiff(current_board, next_bor, colour)
        danger_piece = self.cal_dpiei(current_board, next_bor,colour)

        ev = self.hard_code_eva_function(piece_difference, d_heurii, danger_piece, colour_p[colour], colour_e[colour])

        rew += self.check_heuristic_rew(colour_ea, next_bor, colour, d_heurii)

        return rew, d_heurii, uti, ev

    def heuristic(self, players, colour, player_exit):
        h = 0

        tmp_h = []
        for p in players:
            tmp_h.append(self.cost[colour][p])

        tmp_h.sort()
        if player_exit == -1:
            return sum(tmp_h)
        if len(players) + player_exit >= 4:
            h = sum(tmp_h[:4 - player_exit])
        else:
            h = sum(tmp_h)
            h += (4 - (len(players) + player_exit)) * 10

        return h

    @staticmethod
    def get_next_curbo(current_board, action, colour):

        t_cur = copy.deepcopy(current_board)
        
        if action[0] in ("MOVE", "JUMP"):
            t_cur[action[1][0]] = "empty"
            t_cur[action[1][1]] = colour
            if action[0] in ("JUMP", ):
                fr = action[1][0]
                to = action[1][1]
                sk = (fr[0] + (to[0] - fr[0]) / 2, fr[1] + (to[1] - fr[1]) / 2)

                # well I dont freaking know what im thinking about
                if t_cur[sk] != "empty" and t_cur[sk] != colour:
                    
                    

                    t_cur[sk] = colour

        elif action[0] in ("EXIT",):
            t_cur[action[1]] = "empty"

        return t_cur

    def cal_rheu(self, cur_state, next_state, colour, player_exit):
        cur_pl = [x for x in cur_state.keys() if cur_state[x] == colour]
        nxt_pl = [x for x in next_state.keys() if next_state[x] == colour]

        cur_heuri = self.heuristic(cur_pl, colour, player_exit)
        nxt_heuri = self.heuristic(nxt_pl, colour, player_exit)

        return nxt_heuri - cur_heuri

    def player_es(self, colour_e, exit_this):
        # only red here wait for more colours
        rest_ps = [colour_e[k] for k in self.arrange]

        if exit_this:
            rest_ps[0] = rest_ps[0] + 1

        return rest_ps

    def cal_heuristic(self, suc_bo, colour, colour_exit):

        heuris = [self.heuristic([x for x in suc_bo.keys() if suc_bo[x] == c],c,colour_exit[c]) for c in self.arrange]

        return heuris

    @staticmethod
    def cal_pdiff(cur_state, next_state, colour):
        c_or = [k for k in cur_state.keys() if cur_state[k] != "empty" and cur_state[k] == colour]
        n_r = [k for k in next_state.keys() if next_state[k] != "empty" and next_state[k] == colour]

        c_ors = len(c_or)
        n_s = len(n_r)
        return n_s - c_ors

    @staticmethod
    def cal_dpiei(cur_state, next_state, colour):
        nxt_pl = [k for k in next_state.keys() if next_state[k] == colour]
        nxt_ot = [k for k in next_state.keys() if next_state[k] != "empty" and next_state[k] != colour]

        tmp_current_board = {x: "empty" for x in config.CELLS}
        for p in nxt_pl:
            tmp_current_board[p] = "n"
        for p in nxt_ot:
            tmp_current_board[p] = "n"

        dengr = set({})
        
        for p in nxt_ot:
            p_nxt = utils.find_next(p, tmp_current_board)
            for d in p_nxt:
                if d[2] == 2:
                    if d[3] in nxt_pl:
                        dengr.add(d[3])
        
        return len(dengr)

    @staticmethod
    def hard_code_eva_function(pieces_difference: int, reduced_heuristic: float, danger_pieces: int, players, player_exit) -> float:
        """
        1. # possible safety movement (*1)
        2. reduced heuristic to dest (positive means increased, negative means decreased) *(-2)
        3. # of piece in danger (could be taken by opponent by one JUMP action) *(-5)
        """
        # print(pieces_difference, reduced_heuristic, danger_pieces)
        t = len(players) + player_exit

        if t < 4:
            return 20 * pieces_difference + (-2) * reduced_heuristic + danger_pieces * (-10)
        elif t == 4:
            return 5 * pieces_difference + (-2.4) * reduced_heuristic + danger_pieces * (-20)
        else:
            return 5 * pieces_difference + (-2.4) * reduced_heuristic + danger_pieces * (-2)

    @staticmethod
    def check_heuristic_rew(colour_exit, suc_bo, colour, d_heur):
        n_r = [k for k in suc_bo.keys() if suc_bo[k] != "empty" and suc_bo[k] == colour]
        exited = colour_exit[colour]

        count = exited + len(n_r)

        if d_heur > 0:
            return config.D_HEURISTIC
        elif d_heur == 0:
            return config.D_HEURISTIC_HORIZONTAL

        return 0

    def cost_from_goal(self, goal: tuple, tmp_current_board: dict, colour) -> None:
        """
        Receive a goal coordinate and block list then calculate a pre-define cost which
        represent the cost from any place to the cost goal
        """

        q = queue.Queue()

        # (cost_from_goal, ((MOVE_counter, JUMP_counter), coordinates))
        q.put((0, ((0, 0), goal)))

        cost = {goal: 0}

        self.cost[colour][goal] = 1

        while not q.empty():

            current = q.get()

            successors = utils.find_next(current[1][1], tmp_current_board)
            child_cost = current[0] + 1

            for s in successors:
                if s[1] not in cost:
                    # since we are using BFS to findNext the coordinates
                    # better solution will be always expanded first
                    counter = None
                    # s[1] indicates if the next move s is achieved by move (1) or jump (2)
                    # used in calculating heuristic g
                    if s[2] == 1:
                        counter = (current[1][0][0] + 1, current[1][0][1])
                    elif s[2] == 2:
                        counter = (current[1][0][0], current[1][0][1] + 1)

                    q.put((child_cost, (counter, s[1])))
                    cost[s[1]] = child_cost

                    # if the cost less then update the closest cost
                    h = counter[0] + 1

                    if s[1] not in self.cost[colour]:
                        self.cost[colour][s[1]] = h
                    elif self.cost[colour][s[1]] > h:
                        self.cost[colour][s[1]] = h

        return

