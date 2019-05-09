import HardCode3.utils as utils
import HardCode3.config as config
import HardCode3.logger as logger

import HardCode3.compatNode as cnode
import copy
import queue
import HardCode3.maxn as maxn

# 2 utility:
#  pieces less than 4 then up eating utility (include exit pieces)
#  more or equal to 4 then prevent to be eaten
class Strategy:

    def __init__(self, goals, colour):
        self.cost = config.COST

        self.colour = colour

        self.goals = goals

        self.arrange = config.MAIN[self.colour]

        

        
        self.turn = 0

        self.logger = logger.Logger(self.colour)



    def get_possible_moves(self, current_board, colour, colour_p, goal, colour_e):
        self.turn += 1

        node = cnode.CompatNode(current_board, colour, colour_e, turn=self.turn)

        # succesrs = node.expand()

        maxnn = maxn.MaxN(node)
        max_e = maxnn.chose()
        


        '''for succr in succesrs:

            print(succr.get_full_utilities())
            if succr.action[0] in ("EXIT", None):
                max_e = succr'''
                


        re = max_e.cald[1]
        utility = max_e.cald[2]
        ev = max_e.cald[3]
        rew = max_e.cald[0]

        self.logger.add_log(max_e.current_board, action=max_e.action, rew=rew, d_heur=re, utility=utility, ev=ev, turns=max_e.turn)
        
        return max_e.action

