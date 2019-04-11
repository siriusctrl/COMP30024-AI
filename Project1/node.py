import utils
import functools


@functools.total_ordering
class Node:
    """
        Node class

        for using search tree and contains state and the action from last move.
        the cost g and f (g + heuristic) are stored as well!

        built for project pA of COMP30024
        Authors: Xinyao Niu (900721), Maoting Zuo (901116)
        Team Name: VanGame
    """

    def __init__(self, pre_node: 'node' = None, state: dict = {},
                 transition_action: str = "", g=0, jumping: bool = False, direc: int = 9) -> None:
        """
            constructor
            * pre_node -- parent node on the tree (None by default)
            * state -- current state (empty by default)
            * transition_action -- output string for this node, will be used in backtrace
            * g -- cost so far to achieve this state
            * jumping -- does this state achieved by action JUMP
            * direc -- which direction does the previous state relative to this state (None by default, should in 1-6)
        """

        # string of the action that how state are transfer from last node to this node
        self.transition_action = transition_action
        self.pre_node = pre_node
        self.g = g
        self.state = state

        # if the state is reached by jump
        self.jumping = jumping

        # last move or jump's direction
        self.direc = direc

        # calculate heuristic when initializing the node
        self.f = self.g + self.heuristic(self.state)

    def __lt__(self, other):
        """
            function override for using comparision operators.
        """
        return self.f < other.f

    def __eq__(self, other):
        """
            function override for using comparision operators.
        """

        return self.f == other.f and self.g == other.g and self.state == other.state

    def heuristic(self, state):
        """
            heuristic function
        """

        # sum of all move/2 + jump from the position of
        # each piece to their closest goal
        # (proof of admissible refer to the report)
        h = 0

        for p in state["players"]:

            min_distance_from_goal = utils.COST[p]

            # get a int of heuristic
            if min_distance_from_goal[0] % 2 == 0:
                h = h + (min_distance_from_goal[0] / 2 + min_distance_from_goal[1] + 1)
            else:
                h = h + ((min_distance_from_goal[0] - 1) / 2 + min_distance_from_goal[1] + 2)

        return h

    def _newNode(self, old_coord: tuple, new_coord: tuple = None, transition_action="", jumping=False, direc=9):
        """
            private (well..)function for generating new nodes
        """

        new_state = {"players": self.state["players"].copy()}

        # remove old position
        # if taken EXIT action, then remove it without appending new position
        new_state["players"].remove(old_coord)

        # Only append when all the piece has valid position in the next state
        if new_coord:
            new_state["players"].add(new_coord)

        new_state["goals"] = self.state["goals"]
        new_state["blocks"] = self.state["blocks"]

        new_node = Node(self, new_state, g=(self.g + 1),
                        transition_action=transition_action, jumping=jumping, direc=direc)

        return new_node

    def expand(self) -> list:
        """
            this method are trying to find all the possible movement
            (except its parent node state) for all the available pieces on the
            board as next possible states based on the current position 
            of pieces, and regard them as the child of this node. Notice
            that we assume moving back and forth does not give us a 
            optimal solution.
        """

        # delta x and y from any position to its neighbourhood (move)
        move = [
            [0, -1],
            [1, -1],
            [1, 0],
            [0, 1],
            [-1, 1],
            [-1, 0]
        ]

        # delta x and y from any position to its possible move (jump)
        jump = [
            [0, -2],
            [2, -2],
            [2, 0],
            [0, 2],
            [-2, 2],
            [-2, 0]
        ]

        successors = []
        max_directions = 6

        for piece in self.state["players"]:

            # same position but different tuple
            tmpPiece = piece + ()

            # if piece is on the goal then exit
            if tmpPiece in self.state["goals"]:
                s = self._newNode(tmpPiece,
                                  transition_action="EXIT from " + str(tmpPiece) + ".")
                successors.append(s)
                continue

            # check position of next possible moves
            # one direction at a time, check both move and jump
            for i in range(max_directions):

                # by move
                # 1 step position in this direction
                check_move = (tmpPiece[0] + move[i][0],
                              tmpPiece[1] + move[i][1])

                # not going back
                if abs(i - self.direc) == 3:
                    continue

                if (not (check_move in self.state["blocks"] or
                         check_move in self.state["players"])) \
                        and utils.piece_validation(check_move):

                    # if can reach this direction one step by move
                    # create new node
                    s = self._newNode(tmpPiece, check_move,
                                      transition_action="MOVE from " + str(tmpPiece)
                                                        +
                                                        " to " + str(check_move) + ".",
                                      jumping=False, direc=i)
                    successors.append(s)
                else:
                    # by jump (if 1 step move in this direction can not 
                    # be reached)
                    # 2 step position in this direction
                    check_jump = (tmpPiece[0] + jump[i][0],
                                  tmpPiece[1] + jump[i][1])

                    if (not (check_jump in self.state["blocks"] or
                             check_jump in self.state["players"])) and \
                            utils.piece_validation(check_jump):
                        # if can reach this direction one step by jump
                        # create new node
                        s = self._newNode(tmpPiece, check_jump,
                                          transition_action="JUMP from " + str(tmpPiece)
                                                            + " to " + str(check_jump) + ".",
                                          jumping=True, direc=i)
                        successors.append(s)

        return successors

    def goal_test(self):
        """
            determine if the current state is the goal state
        """
        return len(self.state["players"]) == 0

    def __str__(self):
        """
            to string, will be invoked when printing the node
        """

        state_board = {}

        for p in self.state["players"]:
            state_board[p] = "*p*"

        for l in self.state["goals"]:
            if l in state_board:
                state_board[l] = state_board[l] + "*g*"
            else:
                state_board[l] = "*g*"

        for o in self.state["blocks"]:
            if o in state_board:
                state_board[o] = state_board[o] + "*b*"
            else:
                state_board[o] = "*b*"

        utils.print_board(state_board, message=self.transition_action + str(self.heuristic(self.state)), debug=True)

        return self.transition_action

    # make sure that when print a list, the __str__ will also be invoked
    # only for debug purpose
    __repr__ = __str__


if __name__ == "__main__":
    thatShitNode = Node(state={
        "players": [(0, 2), (2, 1)],
        "goals": [(3, 0), (2, 1), (1, 2), (0, 3)],
        "blocks": [(2, -1)]
    })

    print(thatShitNode.expand())
