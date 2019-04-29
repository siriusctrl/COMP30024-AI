import VanGame.utils as utils
import random
import math, copy

import VanGame.logger as logger

import VanGame.keras_model as ker_m
import queue


class Strategy:

    def __init__(self, goals, colour):
        self.cost = {}

        self.colour = colour

        self.goals = goals

        tmp_current_board = {x: "empty" for x in utils.CELLS}

        for g in self.goals:
            self.cost_from_goal(g, tmp_current_board)
        # utils.print_board(self.cost)

        self.logger = logger.Logger(self.colour)

        self.mdl = ker_m.dnn()
    

    def get_possible_moves(self, current_board, colour, colour_p, goal):

        ps = colour_p[colour]

        action = tuple()

        for a in ps:
            if a in goal:
                action = ("EXIT", a)

        suc_bo = current_board
        re = 0
        rew = 0
        
        if(len(action) == 0):
            all_ms = []
            for p in ps:
                all_ms = all_ms + utils.find_next(p, current_board)


            
            acs = []

            all_pre = []

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
                    d_heurii = self.cal_rheu(current_board, next_bor, colour)

                    # board in num representation used in predicting
                    next_n = self.get_board(next_bor, colour, d_heurii)

                    # add the estimate utility value
                    all_pre.append(self.mdl.predict(next_n))

                    # add the next board to be chosen later
                    all_suc.append(next_bor)

                    # add the heuristic
                    all_heu.append(d_heurii)

                    # return all_ms[math.floor(random.random() * len(all_ms))]
                
                # get the right action chosen in this status
                ie = utils.chose(all_pre)
                action = acs[ie]
            else:
                action = ("PASS", None)
            
            # get the current successor state and dheuri
            if (ie != -1):
                suc_bo = all_suc[ie]
                re = all_heu[ie]
        
        if action[0] == "EXIT":
            rew = 125
            re = 1
        
        self.logger.add_log(suc_bo, action=action, rew=rew, d_heur=re)

        return action

        pass

    def heuristic(self, players):
        heuri = 0
        for p in players:
            heuri =heuri + self.cost[p]

        return heuri
        pass


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


    def cal_rheu(self, cur_state, next_state, colour):
        cur_pl = [x for x in cur_state.keys() if cur_state[x] == colour]
        nxt_pl = [x for x in next_state.keys() if next_state[x] == colour]
        

        cur_heuri = self.heuristic(cur_pl)
        nxt_heuri = self.heuristic(nxt_pl)

        return nxt_heuri - cur_heuri
    
    def get_board(self, current_board, colour, heurii):

        jrex = {'green': 1, 'red': 2, 'blue': 3, 'empty': 0}

        nb = {x: jrex[current_board[x]] for x in current_board.keys()}
        the_br = [e[1] for e in sorted(nb.items(), key=lambda u: utils.CELLS.index(u[0]))]
        the_br.append(jrex[colour])
        the_br.append(heurii)

        return the_br

    def cost_from_goal(self, goal: tuple, tmp_current_board: dict) -> None:
        """
        Receive a goal coordinate and block list then calculate a pre
        """

        q = queue.Queue()

        # (cost_from_goal, ((MOVE_counter, JUMP_counter), coordinates))
        q.put((0, ((0, 0), goal)))

        cost = {goal: 0}

        self.cost[goal] = 1

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

                    if s[1] not in self.cost:
                        self.cost[s[1]] = h
                    elif self.cost[s[1]] > h:
                        self.cost[s[1]] = h

        return

