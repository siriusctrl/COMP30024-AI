"""
COMP30024 Artificial Intelligence, Semester 1 2019
Solution to Project Part A: Searching

Authors: Xinyao Niu (900721), Maoting Zuo (901116)
Team Name: VanGame
"""

import sys
import json
import utils
import traval

def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)
    #print(data)
    # TODO: Search for and output winning sequence of moves
    root = utils.initialNode(data)
    #print(utils.initialNode(data))
    last = traval.Traval(root)
    print(last)

# when this module is executed, run the `main` function:
if __name__ == '__main__':
    main()
