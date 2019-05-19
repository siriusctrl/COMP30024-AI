import HardCode3.config as config
import HardCode3.compatNode as cnode
import HardCode3.maxn as maxn

# 2 utility:
#  pieces less than 4 then up eating utility (include exit pieces)
#  more or equal to 4 then prevent to be eaten
class Strategy:

    def __init__(self, colour):

        self.colour = colour
        self.turn = 0

    def get_possible_moves(self, current_board, colour, colour_exit, turn):
        
        self.turn = turn

        node = cnode.CompatNode(current_board, colour, colour_exit, turn=self.turn)

        maxnn = maxn.MaxN(node)
        max_e = maxnn.chose()
    
        return max_e.action

