### Code Structure

---

- node.py

  - The basic unit of our tree. Each node contains their own state (position of pieces), and can decide whether the game end or not. Most of the node can be expanded, unless they reach the final state.

- search.py

  - The main entry of the project

- travel.py

  - Decide how we are going to expand the tree

- utils.py

  - Contains some constants variable and general method could be used for many files in order to save the memory and repeatedly creating the same thing again and again.


### Game As a Search Problem

---

We regard this game as a search problem from the following perspective

- State
  - Each node contains a state, different node contains different state.
  - How board looks like described a state, every times the board changed, we regard it as a new state.
- Actions
  - There are three possible actions, MOVE, JUMP, EXIT.
- Goal tests
  - If there are no player pieces on board, we say that we reached the final state.
- Action cost
  - Each action cost 1

### Algorithms

---

- 



### Test cases

---

- 