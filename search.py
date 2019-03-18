"""
COMP30024 Artificial Intelligence, Semester 1 2019
Solution to Project Part A: Searching

Authors: Xinyao Niu (900721), Maoting Zuo (901116)
Team Name: VanGame
"""

import sys
import json
import utils

def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)
    print(data)
    utils.print_board(data, message="this is a test", debug=True)
    # TODO: Search for and output winning sequence of moves
    # ...


# when this module is executed, run the `main` function:
if __name__ == '__main__':
    main()
