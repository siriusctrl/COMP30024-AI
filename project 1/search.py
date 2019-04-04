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
    with open(sys.argv[1]) as file:
        data = json.load(file)

    root = utils.initialRoot(data)
    print(root)

    #return the last node of the 
    last = travel.Travel(root).Astar_Q()

    totalSteps = 0

    results = ""

    while last != root:
        totalSteps += 1
        results = last.fromLastAction + "\n" + results
        last = last.preNode
    
    print("# total steps are:", totalSteps)
    print(results)

# when this module is executed, run the `main` function:
if __name__ == '__main__':
    main()
