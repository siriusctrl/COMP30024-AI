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

        self.goal = config.GOALS[self.colour]

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
            self.cald = self.cal_all(parent_n.current_board, self.current_board, self.colour, self.colour_e, self.colour_p, self.action, self.action[0]=="EXIT")
        else:
            self.cald = []
    


    def cal_all(self, current_board, next_bor, colour, colour_e, colour_p, action, exit_this=False):

        rew = 0

        d_heurii = self.cal_rheu(current_board, next_bor, colour, -1)
        
        if exit_this:
            rew += config.EXIT_RW
        else:
            pass
        uti = self.get_utility(current_board, next_bor, colour, d_heurii, colour_e)

        piece_difference = self.cal_pdiff(current_board, next_bor, colour)
        danger_piece = self.cal_dpiei(current_board, next_bor,colour)

        ev = self.hard_code_eva_function(piece_difference, d_heurii, danger_piece, colour_p[colour], colour_e[colour], action)
        rew += self.check_heuristic_rew(colour_e, next_bor, colour, d_heurii)

        return (rew, d_heurii, uti, ev)


    def get_utility(self, current_board, suc_bo, colour, re, colour_ea):
        piece_difference = self.cal_pdiff(current_board, suc_bo, colour)
        danger_piece = self.cal_dpiei(current_board, suc_bo ,colour)

        utility = [
                    re,
                    piece_difference,
                    danger_piece
                ]

        utility += self.player_es(colour_ea, False)

        utility += self.cal_heuristic(suc_bo, colour, colour_ea)

        return utility
    

    def heuristic(self, players, colour, player_exit):
        h = 0

        tmp_h = []
        for p in players:
            tmp_h.append(config.COST[colour][p])

        tmp_h.sort()
        if player_exit == -1:
            return sum(tmp_h)
        if len(players) + player_exit >= 4:
            h = sum(tmp_h[:4 - player_exit])
        else:
            h = sum(tmp_h)
            h += (4 - (len(players) + player_exit)) * 10

        return h


    @staticmethod
    def get_next_curbo(current_board, action, colour):

        t_cur = copy.deepcopy(current_board)

        if action[0] in ("MOVE", "JUMP"):
            t_cur[action[1][0]] = "empty"
            t_cur[action[1][1]] = colour
            if action[0] in ("JUMP", ):
                fr = action[1][0]
                to = action[1][1]
                sk = (fr[0] + (to[0] - fr[0]) / 2, fr[1] + (to[1] - fr[1]) / 2)

                # well I dont freaking know what im thinking about
                if t_cur[sk] != "empty" and t_cur[sk] != colour:
                    t_cur[sk] = colour

        elif action[0] in ("EXIT",):
            t_cur[action[1]] = "empty"

        return t_cur


    def player_es(self, colour_e, exit_this):
        # only red here wait for more colours
        rest_ps = [colour_e[k] for k in self.arrange]

        if exit_this:
            rest_ps[0] = rest_ps[0] + 1

        return rest_ps


    def cal_heuristic(self, suc_bo, colour, colour_exit):

        heuris = [self.heuristic([x for x in suc_bo.keys() if suc_bo[x] == c],c,colour_exit[c]) for c in self.arrange]
        return heuris


    '''
        calculation of variables used in eval func
    '''

    @staticmethod
    def cal_pdiff(cur_state, next_state, colour):
        c_or = [k for k in cur_state.keys() if cur_state[k] != "empty" and cur_state[k] == colour]
        n_r = [k for k in next_state.keys() if next_state[k] != "empty" and next_state[k] == colour]

        c_ors = len(c_or)
        n_s = len(n_r)
        return n_s - c_ors


    @staticmethod
    def cal_dpiei(cur_state, next_state, colour):
        nxt_pl = [k for k in next_state.keys() if next_state[k] == colour]
        nxt_ot = [k for k in next_state.keys() if next_state[k] != "empty" and next_state[k] != colour]

        tmp_current_board = {x: "empty" for x in config.CELLS}
        for p in nxt_pl:
            tmp_current_board[p] = "n"
        for p in nxt_ot:
            tmp_current_board[p] = "n"

        dengr = set({})
        
        for p in nxt_ot:
            p_nxt = utils.find_next(p, tmp_current_board)
            for d in p_nxt:
                if d[2] == 2:
                    if d[3] in nxt_pl:
                        dengr.add(d[3])
        
        return len(dengr)

    
    def cal_rheu(self, cur_state, next_state, colour, player_exit):
        cur_pl = [x for x in cur_state.keys() if cur_state[x] == colour]
        nxt_pl = [x for x in next_state.keys() if next_state[x] == colour]

        cur_heuri = self.heuristic(cur_pl, colour, player_exit)
        nxt_heuri = self.heuristic(nxt_pl, colour, player_exit)

        return nxt_heuri - cur_heuri


    '''
        eval func
    '''

    @staticmethod
    def hard_code_eva_function(pieces_difference: int, reduced_heuristic: float, danger_pieces: int, players, player_exit, action) -> float:
        """
        1. # possible safety movement (*1)
        2. reduced heuristic to dest (positive means increased, negative means decreased) *(-2)
        3. # of piece in danger (could be taken by opponent by one JUMP action) *(-5)
        """
        # print(pieces_difference, reduced_heuristic, danger_pieces)
        t = len(players) + player_exit

        res = 0

        if action[0] == "EXIT":
            res += 10

        if t < 4:
            res += 30 * pieces_difference + (-2) * reduced_heuristic + (danger_pieces - max(0, pieces_difference)) * (-10)
        elif t == 4:
            res += 5 * pieces_difference + (-2) * reduced_heuristic + (danger_pieces - max(0, pieces_difference)) * (-20)
        else:
            res += 5 * pieces_difference + (-2) * reduced_heuristic + (danger_pieces - max(0, pieces_difference)) * (-2)

        return res
    
    def expand(self):

        nxt_turn = self.turn +1

        ps = self.colour_p[self.colour]

        action = tuple()

        all_state_players = []

        for a in ps:
            if a in self.goal:
                action = ("EXIT", a)
                next_bor = self.get_next_curbo(self.current_board, action, self.colour)
                
                next_node = CompatNode(next_bor, self.colour, self.colour_e, self, action, nxt_turn)
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
                    
                    next_bor = self.get_next_curbo(self.current_board, m_action, self.colour)

                    next_node = CompatNode(next_bor, self.colour, self.colour_e, self, m_action, nxt_turn)

                    all_state_players.append(next_node)

                    # delta heuristic
            else:
                action = ("PASS", None)
                next_bor = self.get_next_curbo(self.current_board, action, self.colour)
                
                next_node = CompatNode(next_bor, self.colour, self.colour_e, self, action, nxt_turn)
                all_state_players.append(next_node)
        
        return all_state_players


    '''
        heuristic reward cal
    '''


    @staticmethod
    def check_heuristic_rew(colour_exit, suc_bo, colour, d_heur):
        n_r = [k for k in suc_bo.keys() if suc_bo[k] != "empty" and suc_bo[k] == colour]
        exited = colour_exit[colour]

        count = exited + len(n_r)

        if d_heur > 0:
            return config.D_HEURISTIC
        elif d_heur == 0:
            return config.D_HEURISTIC_HORIZONTAL

        return 0