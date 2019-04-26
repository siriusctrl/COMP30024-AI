import VanGame.utils as utils
import random
import math, copy


class Strategy:

    def __init__(self, goals):
        self.cost = {}

        self.goals = goals

        tmp_current_board = {x: "empty" for x in utils.CELLS}

        self.log = []

        print(self.cost)
    

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
            
            print(all_ms)

            if len(all_ms):
                cm = all_ms[math.floor(random.random() * len(all_ms))]
                if cm[2] == 1:
                    action = ("MOVE", (cm[0], cm[1]))
                elif cm[2] == 2:
                    action = ("JUMP", (cm[0], cm[1]))
                # return all_ms[math.floor(random.random() * len(all_ms))]
            else:
                action = ("PASS", None)
            

        self.add_log(current_board, colour, action=action)

        return action

        pass

    
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
