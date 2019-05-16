import HardCode3.config as config
import HardCode3.utils as utils
import copy
from collections import defaultdict as dd


class CompatNode:

    def __init__(self, next_board, colour, last_colour_exit, player_nums, parent_n=None, action=("None", None), turn=0):
        self.turn = turn
        self.current_board = next_board
        self.parent_n = parent_n
        self.colour = colour
        self.cost = config.COST
        self.arrange = config.MAIN[self.colour]
        # do not prefer visited path, unless it is the only choice
        self.visited = dd(lambda: 0)

        self.player_nums = player_nums

        self.win = 0

        self.last_colour_exit = last_colour_exit
        self.colour_exit = copy.deepcopy(last_colour_exit)

        self.goal = config.GOALS

        if action[0] == "EXIT":
            self.colour_exit[colour] += 1
        self.action = action

        self.colour_players = {
            "red": [],
            "green": [],
            "blue": []
        }

        for clr in self.colour_players.keys():
            self.colour_players[clr] = [x for x in self.current_board.keys() if self.current_board[x] == clr]

        if parent_n is not None:
            self.calculateds = {}

            for c in ["red", "green", "blue"]:

                if c == self.colour:
                    self.calculateds[c] = utils.calculate_related(parent_n.current_board,
                                                  self.current_board,
                                                  self.colour,
                                                  self.colour_exit,
                                                  self.colour_players,
                                                  self.action,
                                                  self.arrange,
                                                  self.turn,
                                                  self.action[0] == "EXIT",
                                                  self.player_nums,
                                                  0)
                else:
                    self.calculateds[c] = utils.calculate_related(parent_n.current_board,
                                                  self.current_board,
                                                  c,
                                                  self.colour_exit,
                                                  self.colour_players,
                                                  ("None", None),
                                                  config.MAIN[c],
                                                  self.turn,
                                                  False,
                                                  self.player_nums,
                                                  0)

            for c in ["red", "green", "blue"]:
                if parent_n.calculated:
                    self.calculateds[c][3] += parent_n.calculateds[c][3]

            self.calculated = self.calculateds[self.colour]
            
        else:

            self.calculated = []
            self.calculateds = {
                "red": [],
                "green": [],
                "blue": []
            }


    def expand(self, colour=""):

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
                next_bor = utils.get_next_curbo(self.current_board, action, colour)

                # next players
                new_player_nums = self.next_player_nums(self.player_nums, action)

                next_node = CompatNode(next_bor, colour, self.colour_exit, new_player_nums, self, action, nxt_turn)
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
                next_bor = utils.get_next_curbo(self.current_board, m_action, colour)

                # next
                new_player_nums = self.next_player_nums(self.player_nums, m_action)

                next_node = CompatNode(next_bor, colour, self.colour_exit, new_player_nums, self, m_action, nxt_turn)

                all_state_players.append(next_node)
        
        else:

            action = ("PASS", None)

            # next board
            next_bor = utils.get_next_curbo(self.current_board, action, colour)

            # next
            new_player_nums = self.next_player_nums(self.player_nums, action)

            next_node = CompatNode(next_bor, colour, self.colour_exit, new_player_nums, self, action, nxt_turn)

            all_state_players.append(next_node)

        return all_state_players


    def next_player_nums(self, player_nums, action):
        next_player_num = copy.deepcopy(player_nums)
        return next_player_num

