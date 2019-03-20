import math

class Node:

    def __init__(self, preNode) -> None:
        self.preNode = preNode
        self.possibleNext = []
        self.coordinates = []
        self.g = 0
        # actions
        # TODO: finish the build of the tree

    def pieceValid(piece: tuple) -> bool:
        max_coor = 3
        min_coor = -3

        return piece[0] >= min_coor and piece[1] >= min_coor and piece[0] <= max_coor and piece[1] <= max_coor
    

    def expand(self, chessBoard: list, blocks: list) -> None:
        """
        this method are tring to find all the possible movement for
        all the avaliable pieces on the board as next possible
        states based on the current position of pieces, and trate
        them like the child of this node.
        """

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
        pass
    