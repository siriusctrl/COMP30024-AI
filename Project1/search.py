"""
COMP30024 Artificial Intelligence, Semester 1 2019
Solution to Project Part A: Searching

Authors: Xinyao Niu (900721), Maoting Zuo (901116)
Team Name: VanGame
"""

import sys
import json
import utils
import travel


def main():
    if len(sys.argv) >= 2:
        with open(sys.argv[1]) as file:
            data = json.load(file)
    else:
        with open("test.json") as file:
            data = json.load(file)

    root = utils.root_init(data)

    # return the goal state (node) so that we can back trace to get the result
    last = travel.Travel(root).Astar_Q()

    total_steps = 0

    moves = ""

    while last != root:
        total_steps += 1
        moves = last.transition_action + "\n" + moves
        last = last.pre_node

    print("# total steps are:", total_steps)
    print(moves)


# when this module is executed, run the `main` function:
if __name__ == '__main__':
    main()
