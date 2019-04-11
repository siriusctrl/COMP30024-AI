from heapq import heappush, heappop


class Travel:
    """
    this class define the strategies that we are going to explore the search tree
    """

    def __init__(self, root):
        self.root = root
        self.infi = 999  # maximum possible movement if there is really a solution
        self.fa = "Failure"

    def Astar_Q(self) -> 'node':
        """
        A* search using the Priority Queue to maintance the frontier
        """

        # frontier list
        front = []
        # a dictionary to store seen states, if there is a duplication, only 
        # the one with better g will be kept
        visited = {}
        # Only for debugging purpose, to see how many nodes are pruned
        removed = 0
        explored = 0

        for s in self.root.expand():
            heappush(front, s)
            visited[tuple(sorted(s.state["players"]))] = s

        while True:
            current_node = heappop(front)

            if current_node.goal_test():
                print("# total removed duplicate nodes =", removed)
                print("# current PQ size =", len(front))
                print("# explored node =", explored)
                return current_node

            if current_node.f > self.infi:
                return None

            successors = current_node.expand()
            explored += 1

            for s in successors:
                state = tuple(sorted(s.state["players"]))
                if state in visited:
                    # only record better node
                    if visited[state].g > s.g:
                        heappush(front, s)
                        visited[state] = s
                    else:
                        # discard the worse one to reduce space and time complexity
                        removed += 1
                else:
                    heappush(front, s)
                    visited[state] = s
