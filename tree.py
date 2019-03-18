import math

class tree:

    def __init__(self, pre:tree) -> None:
        self.pre = pre
        self.next = None
        # TODO: finish the build of the tree