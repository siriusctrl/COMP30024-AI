import math
import utils
import functools


@functools.total_ordering
class Node:

    def __init__(self, preNode:'node'=None, state: "dict"={}, fromLastAction="", g=0) -> None:
        self.nearSix = [
            [0, -1],
            [1, -1],
            [1, 0],
            [0, 1],
            [-1, 1],
            [-1, 0]
        ]

        self.fromLastAction = fromLastAction
        self.preNode = preNode
        self.successors = []
        self.g = g
        self.state = state
        # self.heuristic({"players": [[-3, 3], [5,5]], "goals": [[-3, 3]]})
        self.f = self.g + self.heuristic(self.state)
        # actions
        # TODO: finish the build of the tree

    def pieceValid(self, piece: tuple) -> bool:
        max_coor = 3
        min_coor = -3

        return piece[0] >= min_coor and piece[1] >= min_coor and piece[0] <= max_coor and piece[1] <= max_coor

    def __lt__(self, other):
        return self.f < other.f
    
    def __eq__(self, other):
        return self.f == other.f and self.g == other.g and self.state == other.state

    def heuristic(self, state):
        Heuri = []
        for pc in state["players"]:
            tmpHeuri = []
            #print(str(pc))
            for go in state["goals"]:
                
                if pc[1] > go[1]:
                    checkNear = [0, 1]
                elif pc[1] < go[1]:
                    checkNear = [3, 4]
                else:
                    tmpHeuri.append(abs(go[0] - pc[0]))
                    continue
                
                for i in checkNear:
                    moveCoor = self.nearSix[i]
                    dX = abs(go[0] - pc[0])
                    dY = abs(go[1] - pc[1])



                    moveToX = [x * dX for x in moveCoor]
                    #print(moveToX)
                    newCoor = [pc[0] + moveToX[0], pc[1] + moveToX[1]]
                    if go[0] == newCoor[0]:
                        tmpHeuri.append(abs(dX + abs(go[1] - newCoor[1])))

                    #print("goal: " + str(go) + str(dX + abs(go[1] - newCoor[1])))

                    moveToY = [x * dY for x in moveCoor]
                    #print(moveToY)
                    newCoor = [pc[0] + moveToY[0], pc[1] + moveToY[1]]
                    if go[1] == newCoor[1]:
                        tmpHeuri.append(dY + abs(go[0] - newCoor[0]))
                    #print("goal: " + str(go) + str(dY + abs(go[0] - newCoor[0])))
                    
            minDist = min(tmpHeuri)

            # not adding one

            if minDist % 2 == 0:
                Heuri.append(minDist / 2 + 1)
            else:
                Heuri.append((minDist-1)/2 +2)  
            # print(Heuri)
        return sum(Heuri)

    def _newNode(self, oldCoor: tuple, newCoor: tuple=None, fromLastAction=""):
        newState = {}
        newState["players"] = self.state["players"] + []
        newState["players"].remove(oldCoor)
        if newCoor:
            newState["players"].append(newCoor)
        newState["goals"] = self.state["goals"]
        newState["blocks"] = self.state["blocks"]

        newNode = Node(self, newState, g=(self.g + 1), fromLastAction=fromLastAction)
        # newNode.g = self.g + 1

        self.successors.append(newNode)
        return newNode

    def expand(self) -> None:
        """
        this method are tring to find all the possible movement for
        all the avaliable pieces on the board as next possible
        states based on the current position of pieces, and trate
        them like the child of this node.
        """
        # TODO: also need to consider when pieces can exit the board
        nearSix = [
            [0, -1],
            [1, -1],
            [1, 0],
            [0, 1],
            [-1, 1],
            [-1, 0]
        ]

        further = [
            [0, -2],
            [2, -2],
            [2, 0],
            [0, 2],
            [-2, 2],
            [-2, 0]
        ]

        # allMoves = dict()
        allMoveNodes = []
        numOfAllPossible = 6

        for piece in range(len(self.state["players"])):

            tmpPiece = tuple(self.state["players"][piece] + ())
            # tmpCanMovePieces = []

            if tmpPiece in self.state["goals"]:
                theNew = self._newNode(tmpPiece, fromLastAction="EXIT from " + str(tmpPiece) + ".")
                # theNew.fromLastAction = str(tmpPiece) + " EXIT from " + str(tmpPiece)
                allMoveNodes.append(theNew)
                continue

            for i in range(numOfAllPossible):
                checkingCoordin = (tmpPiece[0] + nearSix[i][0], tmpPiece[1] + nearSix[i][1])
                if (not (checkingCoordin in self.state["blocks"] or checkingCoordin in self.state["players"])) and self.pieceValid(checkingCoordin):
                    # tmpCanMovePieces.append(checkingCoordin)
                    theNew = self._newNode(tmpPiece, checkingCoordin, fromLastAction= "MOVE from " + str(tmpPiece) + " to " + str(checkingCoordin) + ".")
                    # theNew.fromLastAction = str(tmpPiece) + " MOVE to " + str(checkingCoordin)
                    allMoveNodes.append(theNew)
                else:
                    furtherCoordin = (tmpPiece[0] + further[i][0], tmpPiece[1] + further[i][1])
                    if (not (furtherCoordin in self.state["blocks"] or furtherCoordin in self.state["players"])) and self.pieceValid(furtherCoordin):
                        # tmpCanMovePieces.append(furtherCoordin)

                        theNew = self._newNode(tmpPiece, furtherCoordin, fromLastAction="JUMP from " + str(tmpPiece) + " to " + str(furtherCoordin) + ".")
                        # theNew.formLastAction = str(tmpPiece) + " JUMP to " + str(furtherCoordin)
                        allMoveNodes.append(theNew)

            # allMoves[tmpPiece] = tmpCanMovePieces

        # return allMoves
        return allMoveNodes

    
    def goal_test(self):
        """
        determine if the current state is the goal state
        """
        #TODO: implement this here
        return self.state["players"] == []


    def __str__(self):
        stateBoard = {

        }
        for p in self.state["players"]:
            stateBoard[p] = "*p*"

        for l in self.state["goals"]:
            if l in stateBoard:
                stateBoard[l] = stateBoard[l]+ "*a*"
            else:
                stateBoard[l] = "*a*"
        
        for o in self.state["blocks"]:
            if o in stateBoard:
                stateBoard[o] = stateBoard[o] + "*o*"
            else:
                stateBoard[o] = "*o*"
        utils.print_board(stateBoard, message=self.fromLastAction + str(self.heuristic(self.state)), debug=True)
        # return utils.print_board(stateBoard, debug=True)
        return self.fromLastAction

    __repr__ = __str__

if __name__ == "__main__":
    thatShitNode = Node(state={
        "players": [(0, 2), (2, 1)],
        "goals": [(3, 0), (2, 1), (1, 2), (0, 3)],
        "blocks": [(2, -1)]
    })

    print(thatShitNode.expand())
