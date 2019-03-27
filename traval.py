import math
from heapq import *
import node

class traval():

    def __init__(self, root:node) -> None:
        self.frontier = []
        heappush(self.frontier, root)
        self.flimit = 9999999
        

    def traval(self, root:node, ) -> None:
        # the game has finished
        if (len(root.state["players"]) == 0) or (len(root.possibleNext) == 0):
            return None
        
        



    def can_builder(self, n:node) -> tuple:
        return (n.f, n)