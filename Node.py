import math

class Node:

    def __init__(self, preNode:Node) -> None:
        self.preNode = preNode
        self.possibleNext = []
        self.coordinates = []
        # TODO: finish the build of the tree
    

    def expand(self) -> None:
        """
        this method are tring to find all the possible movement for
        all the avaliable pieces on the board as next possible
        states based on the current position of pieces, and trate
        them like the child of this node.
        """
        pass
    

    def moveTo(self, c1:list, c2:list) -> Node:
        """
        moveTo the next state of the board, creating a new child
        node to represent.

        * `c1` the current position of the piece you want to move

        * `c2` the position that piece will move to
        """
        pass
    
    

