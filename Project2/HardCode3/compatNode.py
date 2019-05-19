import HardCode3.config as config
import HardCode3.utils as utils
import copy
from collections import defaultdict as dd


class CompatNode:

    def __init__(self, next_board, colour, last_colour_exit, parent_n=None, 
                                                action=("None", None), turn=0):
        '''
            initialize CompatNode

            We use a node to represent a state, no matter the state is an 
            actual state of current game or the imagine state in the tree
            of maxN.

            args:
                next_board:         this nodes' board

                colour:             the player's colour in this node

                last_colour_exit:   a dict of players' colour and their 
                                    number of exit pieces

                parent_n:           parent node

                action:             last action from last state to 
                                    this state

                turn:               game's total turn so far
        '''
        
        self.turn = turn
        self.current_board = next_board
        self.parent_n = parent_n
        self.colour = colour

        # the heuristic maps of all colours
        self.cost = config.COST

        # do not prefer visited path, unless it is the only choice
        self.visited = dd(lambda: 0)

        self.win = 0

        # exit status of all players, a dict of players: count of exits
        self.colour_exit = copy.deepcopy(last_colour_exit)

        # goals
        self.goal = config.GOALS

        # if last action is an exit then modify self colour's count of exit
        if action[0] == "EXIT":
            self.colour_exit[colour] += 1

        # last action leads to this state
        self.action = action

        # player's pieces on the board
        self.colour_players = {
            "red": [],
            "green": [],
            "blue": []
        }

        # different colour's pieces
        for clr in self.colour_players.keys():
            self.colour_players[clr] = [x for x in self.current_board.keys() 
                                            if self.current_board[x] == clr]

        if parent_n is not None:

            # calculate all player's utility value for this state
            self.calculateds = {}

            for c in ["red", "green", "blue"]:

                if c == self.colour:
                    self.calculateds[c] = utils.calculate_related(
                                                parent_n.current_board,
                                                self.current_board,
                                                self.colour,
                                                self.colour_exit,
                                                self.colour_players,
                                                self.action,
                                                self.turn,
                                                self.action[0] == "EXIT",
                                                0)
                else:
                    self.calculateds[c] = utils.calculate_related(
                                                parent_n.current_board,
                                                self.current_board,
                                                c,
                                                self.colour_exit,
                                                self.colour_players,
                                                ("None", None),
                                                self.turn,
                                                False,
                                                0)

            # accumulate utility value from parent to this state
            for c in ["red", "green", "blue"]:
                if parent_n.calculated:
                    self.calculateds[c][3] += parent_n.calculateds[c][3]

            # get self colour's utility value
            self.calculated = self.calculateds[self.colour]
            
        else:

            self.calculated = []
            self.calculateds = {
                "red": [],
                "green": [],
                "blue": []
            }


    def expand(self, colour=""):
        '''
            expand successors from this state

            args:
                colour:     next successor's player's colour
                            used when consider other player's move in MaxN
        '''

        if colour == "":
            colour = self.colour

        nxt_turn = self.turn + 1

        # players
        ps = self.colour_players[colour]

        # the action
        action = tuple()

        # all successors
        all_state_players = []

        # checking exit
        for a in ps:
            if a in self.goal[colour]:
                action = ("EXIT", a)

                # next board
                next_bor = utils.get_next_curbo(self.current_board, action, 
                                                                        colour)

                next_node = CompatNode(next_bor, colour, self.colour_exit, 
                                                        self, action, nxt_turn)
                all_state_players.append(next_node)

        
        # all next actions
        all_ms = []
        for p in ps:
            all_ms = all_ms + utils.find_next(p, self.current_board)

        if len(all_ms):

            for ms in all_ms:
                m_action = tuple()

                if ms[2] == 1:
                    m_action = ("MOVE", (ms[0], ms[1]))
                elif ms[2] == 2:
                    m_action = ("JUMP", (ms[0], ms[1]))

                # get next board from the this action
                next_bor = utils.get_next_curbo(self.current_board, 
                                                        m_action, colour)

                next_node = CompatNode(next_bor, colour, self.colour_exit, 
                                                        self, m_action, nxt_turn)

                all_state_players.append(next_node)
        
        else:
            
            if len(all_state_players) == 0:
                action = ("PASS", None)

                # next board
                next_bor = utils.get_next_curbo(self.current_board, action, 
                                                                        colour)

                next_node = CompatNode(next_bor, colour, self.colour_exit, 
                                                        self, action, nxt_turn)

                all_state_players.append(next_node)


        return all_state_players

