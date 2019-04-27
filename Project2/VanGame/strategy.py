import VanGame.utils as utils
import random
import math, copy

import VanGame.keras_model as ker_m


class Strategy:

    def __init__(self, goals):
        self.cost = {}

        self.goals = goals

        tmp_current_board = {x: "empty" for x in utils.CELLS}

        self.log = []

        self.mdl = ker_m.dnn()
    

    def get_possible_moves(self, current_board, colour, colour_p, goal):

        ps = colour_p[colour]

        action = tuple()

        for a in ps:
            if a in goal:
                action = ("EXIT", a)
        
        if(len(action) == 0):
            all_ms = []
            for p in ps:
                all_ms = all_ms + utils.find_next(p, current_board)

            print("all" + str(all_ms))

            
            acs = []

            all_pre = []

            if len(all_ms):
                for ms in all_ms:
                    if ms[2] == 1:
                        m_action = ("MOVE", (ms[0], ms[1]))
                    elif ms[2] == 2:
                        m_action = ("JUMP", (ms[0], ms[1]))
                    acs.append(m_action)
                    
                    next_bor = self.get_next_curbo(current_board, m_action, colour)

                    next_n = self.get_board(next_bor, colour)

                    all_pre.append(self.mdl.predict(next_n))

                    # return all_ms[math.floor(random.random() * len(all_ms))]
                
                ie = utils.chose(all_pre)
                action = acs[ie]
            else:
                action = ("PASS", None)
            

        self.add_log(current_board, colour, action=action)

        return action

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

    
    def get_board(self, current_board, colour):

        jrex = {'green': 1, 'red': 2, 'blue': 3, 'empty': 0}

        nb = {x: jrex[current_board[x]] for x in current_board.keys()}
        print(nb)
        the_br = [e[1] for e in sorted(nb.items(), key=lambda u: utils.CELLS.index(u[0]))]
        the_br.append(jrex[colour])

        return the_br


    
    def add_log(self, current_board, colour, action=("NONE", None), utility=0, rew=0):


        nxt_b = copy.deepcopy(current_board)

        if action[0] in ("MOVE", "JUMP"):
            nxt_b[action[1][0]] = "empty"
            nxt_b[action[1][1]] = colour
            if action[0] in ("JUMP", ):
                fr = action[1][0]
                to = action[1][1]
                sk = (fr[0] + (to[0] - fr[0]) / 2, fr[1] + (to[1] - fr[1]) / 2)

                # well I dont freaking know what im thinking about
                if nxt_b[sk] != "empty" and nxt_b[sk] != colour:
                    nxt_b[sk] = colour

        elif action[0] in ("EXIT",):
            nxt_b[action[1]] = "empty"

        new = {str(m): nxt_b[m] for m in nxt_b.keys()}
        # new = {}

        
        
        self.log.append(
            [
            new, rew, utility, action[0]
        ])
