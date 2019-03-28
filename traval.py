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
            self.base.append([s.f, s])
        
        self.base = self.nodeSort(self.base)


    def RBFS(self, node:Node, flimit:float) -> Node:
        
        successors = node.successors

        # there is no path for base node
        if len(successors) == 0:
            return self.fa, self.infi

        for s in successors:
            self.frontier.append((s.f, s))

        while True:
            self.frontier = self.nodeSort(self.frontier)

            # no way towards the goal state through this offspring
            if len(self.frontier) == 0:
                return self.fa, self.infi

            currentNode = self.frontier[0][1]
            # remove the current node from the frontier
            self.frontier = self.frontier[1:]

            # already find the goal
            if currentNode.goal_test():
                return currentNode, currentNode.f
            
            if (currentNode.f <= flimit):
                successors = currentNode.expand()

                # NOTICE: len(successors) might = 0
                for s in successors:
                    self.frontier.append((s.f, s))
            else:
                return self.fa, currentNode.f
        

    def find(self):
        flimit = self.infi - 1

        # expand all the base node before calculating the cost
        for b in self.base:
            b[1].expand()

        while True:

            self.base = self.nodeSort(self.base)
            print([(i[0], i[1].fromLastAction) for i in self.base])
            
            #[NodeCost, NodeObject]
            best = self.base[0]

            # if best base be assigned a infi cost value
            if best[0] >= flimit:
                return "No path, cheack your search logic"

            # the cost of the second best one
            alternativeCost= self.base[1][0]

            # TODO: we can try to use a hash table to store part of the frontier in order to save times
            # new frontier for switching between different branch
            self.frontier = []
            
            result, cost = self.RBFS(best[1], min(flimit, alternativeCost))

            if result != self.fa:
                return result
            
            # update the flimit for the base node
            self.base[0][0] = cost


    def nodeSort(self, nodes:[Node]) -> [Node]:
        return sorted(nodes, key=lambda x:x[0])