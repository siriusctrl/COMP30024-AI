import math

class Node:

    def __init__(self, preNode:'node'=None) -> None:
        self.nearSix = [
            [0, -1],
            [1, -1],
            [1, 0],
            [0, 1],
            [-1, 1],
            [-1, 0]
        ]

        self.preNode = preNode
        self.successors = []
        self.coordinates = []
        self.g = 0
        self.state = {"players": [], "goals": []}
        self.heuristic({"players": [[-3, 3], [5,5]], "goals": [[-3, 3]]})
        # actions
        # TODO: finish the build of the tree

    def pieceValid(self, piece: tuple) -> bool:
        max_coor = 3
        min_coor = -3

        return piece[0] >= min_coor and piece[1] >= min_coor and piece[0] <= max_coor and piece[1] <= max_coor

    def heuristic(self, state):
        Heuri = []
        for pc in state["players"]:
            tmpHeuri = []
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
                    newCoor = [pc[0] + moveToX[0], pc[1] + moveToX[1]]
                    tmpHeuri.append(dX + abs(go[1] - newCoor[1]))

                    moveToY = [x * dY for x in moveCoor]
                    newCoor = [pc[0] + moveToY[0], pc[1] + moveToY[1]]
                    tmpHeuri.append(dY + abs(go[0] - newCoor[0]))

                
            Heuri.append(min(tmpHeuri))
            print(Heuri)
        return max(Heuri)

    def expand(self, chessBoard: list, blocks: list) -> None:
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

        allMoves = dict()
        numOfAllPossible = 6

        for piece in self.coordinates:

            tmpPiece = tuple(piece + [])
            tmpCanMovePieces = []
            for i in range(numOfAllPossible):
                checkingCoordin = (tmpPiece[0] + nearSix[i][0], tmpPiece[1] + nearSix[i][1])
                if (not (checkingCoordin in blocks)) and self.pieceValid(checkingCoordin):
                    tmpCanMovePieces.append(checkingCoordin)
                else:
                    furtherCoordin = (tmpPiece[0] + further[i][0], tmpPiece[1] + further[i][1])
                    if (not (furtherCoordin in blocks)) and self.pieceValid(furtherCoordin):
                        tmpCanMovePieces.append(furtherCoordin)
            allMoves[tmpPiece] = tmpCanMovePieces
        
        return allMoves
    

    def moveTo(self, c1:list, c2:list):
        """
        moveTo the next state of the board, creating a new child
        node to represent.

        * `c1` the current position of the piece you want to move

        * `c2` the position that piece will move to
        """
        # TODO: Does not need it for now
        pass
    
    def goal_test(self):
        """
        determine whether the current state is the goal state
        """
        #TODO: implement this here
        pass

if __name__ == "__main__":
    thatShitNode = Node()