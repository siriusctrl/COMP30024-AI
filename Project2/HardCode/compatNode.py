import HardCode.config as config
import HardCode.utils as utils
import copy

class CompatNode:

    def __init__(self, next_board, colour, last_colour_e, parent_n=None, action=("None", None), turn=0):
        self.turn = turn
        self.current_board = next_board
        self.parent_n = parent_n
        self.colour = colour
        self.cost = config.COST
        self.arrange = config.MAIN[self.colour]

        self.last_colour_e = last_colour_e
        self.colour_e = copy.deepcopy(last_colour_e)

        self.goal = config.GOALS

        if(action[0] == "EXIT"):
            self.colour_e[colour] += 1
        self.action = action

        self.colour_p = {
            "red": [],
            "green": [],
            "blue": []
        }
        

        for clr in self.colour_p.keys():
            self.colour_p[clr] = [x for x in self.current_board.keys() if self.current_board[x] == clr]

        if parent_n != None:
            self.cald = utils.cal_all(parent_n.current_board,
                                      self.current_board,
                                      self.colour,
                                      self.colour_e,
                                      self.colour_p,
                                      self.action,
                                      self.arrange,
                                      self.action[0] == "EXIT")
        else:
            self.cald = []
    
    
    def expand(self, colour =""):

        if colour == "":
            colour = self.colour

        nxt_turn = self.turn +1

        ps = self.colour_p[colour]

        action = tuple()

        all_state_players = []

        for a in ps:
            if a in self.goal[colour]:
                action = ("EXIT", a)
                next_bor =utils.get_next_curbo(self.current_board, action, colour)
                
                next_node = CompatNode(next_bor, colour, self.colour_e, self, action, nxt_turn)
                all_state_players.append(next_node)


        if 2:
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
                    
                    next_bor =utils.get_next_curbo(self.current_board, m_action, colour)

                    next_node = CompatNode(next_bor, colour, self.colour_e, self, m_action, nxt_turn)

                    all_state_players.append(next_node)

                    # delta heuristic
            else:
                action = ("PASS", None)
                next_bor =utils.get_next_curbo(self.current_board, action, colour)
                
                next_node = CompatNode(next_bor, colour, self.colour_e, self, action, nxt_turn)
                all_state_players.append(next_node)
        
        return all_state_players
