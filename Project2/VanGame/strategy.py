import VanGame.utils as utils
import random
import math, copy

import VanGame.logger as logger

import VanGame.keras_model as ker_m
import queue


class Strategy:

    def __init__(self, goals, colour):
        self.cost = {
            "red": {},
            "blue": {},
            "green": {}
        }

        self.colour = colour

        self.goals = goals

        self.arrange = utils.MAIN[self.colour]

        tmp_current_board = {x: "empty" for x in utils.CELLS}

        for g in self.goals:
            self.cost_from_goal(g, tmp_current_board, colour)
        utils.print_board(self.cost[colour])

        for g in utils.GOALS:
            if g != colour:
                for go in utils.GOALS[g]:
                    self.cost_from_goal(go, tmp_current_board, g)
                utils.print_board(self.cost[g])
        



        self.logger = logger.Logger(self.colour)

        self.mdl = ker_m.dnn()

    def get_possible_moves(self, current_board, colour, colour_p, goal, colour_e, turn_count):

        ps = colour_p[colour]

        action = tuple()

        for a in ps:
            if a in goal:
                action = ("EXIT", a)

        suc_bo = current_board
        re = 0
        rew = 0

        utility = []
        
        if(len(action) == 0):
            all_ms = []
            for p in ps:
                all_ms = all_ms + utils.find_next(p, current_board)


            
            acs = []

            all_score = []

            all_heu = []

            all_suc = []

            ie = -1

            if len(all_ms):
                for ms in all_ms:
                    if ms[2] == 1:
                        m_action = ("MOVE", (ms[0], ms[1]))
                    elif ms[2] == 2:
                        m_action = ("JUMP", (ms[0], ms[1]))
                    
                    # add action
                    acs.append(m_action)
                    
                    # next board after the action
                    next_bor = self.get_next_curbo(current_board, m_action, colour)

                    # delta heuristic
                    d_heurii = self.cal_rheu(current_board, next_bor, colour, -1)

                    # board in num representation used in predicting
                    next_n = self.get_board(next_bor, colour, d_heurii)

                    # add the estimate utility value
                    all_score.append(self.mdl.predict(next_n))

                    # add the next board to be chosen later
                    all_suc.append(next_bor)

                    # add the heuristic
                    all_heu.append(d_heurii)

                    # return all_ms[math.floor(random.random() * len(all_ms))]
                
                # get the right action chosen in this status
                ie = utils.chose(all_score)
                action = acs[ie]
            else:
                action = ("PASS", None)
            
            # get the current successor state and dheuri
            if (ie != -1):
                suc_bo = all_suc[ie]
                re = all_heu[ie]
        
        colour_ea = colour_e

        if action[0] == "EXIT":
            rew += 125
            re = -1
            suc_bo = self.get_next_curbo(current_board, action, colour)
            colour_ea = copy.deepcopy(colour_e)
            colour_ea[colour] += 1

        
        if action[0] == "PASS":
            rew += 0
            re = 0
            suc_bo = current_board

        piece_difference = self.cal_pdiff(current_board, suc_bo, colour)
        danger_piece = self.cal_dpiei(current_board, suc_bo ,colour)

        utility = [
                    re,
                    piece_difference,
                    danger_piece
                ]

        utility += self.player_es(colour_ea, False)

        utility += self.cal_heuristic(suc_bo, colour, colour_ea)
        
        rew += self.check_heuristic_rew(colour_ea, suc_bo, colour, re)

        ev = self.hard_code_eva_function(piece_difference, re, danger_piece)
        
        self.logger.add_log(suc_bo, action=action, rew=rew, d_heur=re, utility=utility, ev=ev, turns=turn_count)

        return action

    def heuristic(self, players, colour, player_exit):
        heuri = 0

        tmp_h = []
        for p in players:
            tmp_h.append(self.cost[colour][p])

        tmp_h.sort()
        if player_exit == -1:
            return sum(tmp_h)
        if len(players) + player_exit >= 4:
            heuri = sum(tmp_h[:4 - (player_exit)])
        else:
            heuri = sum(tmp_h)
            heuri =heuri + (4 - (len(players) + player_exit)) *10

        return heuri

    def get_next_curbo(self, current_board, action, colour):

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
        e_c = [
            "red",
            "green",
            "blue"
        ]

        

        

        heuris = [self.heuristic([x for x in suc_bo.keys() if suc_bo[x] == c],c,colour_exit[c]) for c in self.arrange]

        return heuris

    def cal_pdiff(self, cur_state, next_state, colour):
        c_or = [k for k in cur_state.keys() if cur_state[k] != "empty" and cur_state[k] == colour]
        n_r = [k for k in next_state.keys() if next_state[k] != "empty" and next_state[k] == colour]

        c_ors = len(c_or)
        n_s = len(n_r)
        return n_s - c_ors

    def cal_dpiei(self,cur_state, next_state,colour):
        nxt_pl = [k for k in next_state.keys() if next_state[k] == colour]
        nxt_ot = [k for k in next_state.keys() if next_state[k] != "empty" and next_state[k] != colour]
        

        tmp_current_board = {x: "empty" for x in utils.CELLS}
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

    def hard_code_eva_function(self, pieces_difference : int, reduced_heuristic : float, danger_pieces : int) -> float:
        """
        1. # possible safety movement (*1)
        2. reduced heuristic to dest (positive means increased, negative means decreased) *(-2)
        3. # of piece in danger (could be taken by opponent by one JUMP action) *(-5)
        """
        # print(pieces_difference, reduced_heuristic, danger_pieces)
        return (3) *pieces_difference + (-5)*reduced_heuristic + danger_pieces * (-10)

    def check_heuristic_rew(self, colour_exit, suc_bo, colour, d_heur):
        n_r = [k for k in suc_bo.keys() if suc_bo[k] != "empty" and suc_bo[k] == colour]
        exited = colour_exit[colour]

        count = exited + len(n_r)

        if d_heur > 0:
            return utils.D_HEURISTIC
        elif d_heur == 0:
            return utils.D_HEURISTIC_HORIZONTAL

        return 0


    def get_board(self, current_board, colour, heurii):

        jrex = {'green': 1, 'red': 2, 'blue': 3, 'empty': 0}

        nb = {x: jrex[current_board[x]] for x in current_board.keys()}
        the_br = [e[1] for e in sorted(nb.items(), key=lambda u: utils.CELLS.index(u[0]))]
        the_br.append(jrex[colour])
        the_br.append(heurii)

        return the_br

    def cost_from_goal(self, goal: tuple, tmp_current_board: dict, colour) -> None:
        """
        Receive a goal coordinate and block list then calculate a pre
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

                    if s[1] not in self.cost[colour]:
                        self.cost[colour][s[1]] = h
                    elif self.cost[colour][s[1]] > h:
                        self.cost[colour][s[1]] = h

        return

