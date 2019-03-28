import math
from heapq import heappush,heappop
from node import Node

class Traval():

    def __init__(self, root):
        self.root = root
        self.infi = 999
        self.base = []
        self.frontier = []
        self.fa = "Failure"
        
        for s in root.expand():
            heappush(self.base, (s.f, s))


    def RBFS(self, node:Node, flimit:float) -> Node:
        
        successors = node.successors

        # there is no path for base node
        if len(successors) == 0:
            return self.fa, self.infi

        for s in successors:
            heappush(self.frontier, (s.f, s))

        while True:
            
            # no way towards the goal state through this offspring
            if len(self.frontier) == 0:
                return self.fa, self.infi

            currentNode = heappop(self.frontier)

            # already find the goal
            if currentNode.goal_test():
                return currentNode, currentNode.f
            
            if (currentNode.f <= flimit):
                successors = currentNode.expand()

                # NOTICE: len(successors) might = 0
                for s in successors:
                    heappush(self.frontier, (s.f, s))
                
            else:
                return self.fa, currentNode.f
        

    def find(self):
        flimit = self.infi - 1

        # expand all the base node before calculating the cost
        for b in self.base:
            b[1].expand()

        while True:
            #(NodeCost, NodeObject)
            best = heappop(self.base)

            # if best base be assigned a infi cost value
            if best[0] >= flimit:
                return "No path, cheack your search logic"

            # the cost of the second best one
            alternativeCost= self.base[0][0]

            # new frontier
            # TODO: we can try to a hash table to store part of the frontier in order to save times
            self.frontier = []
            
            result, cost = self.RBFS(best, min(flimit, alternativeCost))

            if result != self.fa:
                return result
            
            # update the flimit for the base node
            heappush(self.base, (cost, best[1]))

    