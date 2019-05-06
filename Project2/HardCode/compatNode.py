import HardCode.config as config
import HardCode.utils as utils
import copy

class CompatNode:

    def __init__(self, next_board, colour, last_colour_e, parent_n=None, action=("None", None)):
        self.current_board = next_board
        self.parent_n = parent_n
        self.colour = colour

        self.last_colour_e = last_colour_e
        self.colour_e = copy.deepcopy(last_colour_e)
        if(action[0] == "EXIT"):
            self.colour_e[colour] += 1
        self.last_action = action

        self.colour_p = [x for x in self.current_board.keys() if self.current_board[x] == self.colour]

        if parent_n != None:
            self.cald = self.cal_all(parent_n.current_board, self.current_board, self.colour, self.colour_e, self.colour_p, self.last_action[0]=="EXIT")
        else:
            self.cald = []
    


    def cal_all(self, current_board, next_bor, colour, colour_e, colour_p, exit_this=False):

        rew = 0

        d_heurii = self.cal_rheu(current_board, next_bor, colour, -1)
        
        colour_ea = colour_e
        if exit_this:
            rew += config.EXIT_RW
        else:
            pass
        uti = self.get_utility(current_board, next_bor, colour, d_heurii, colour_e)


        piece_difference = self.cal_pdiff(current_board, next_bor, colour)
        danger_piece = self.cal_dpiei(current_board, next_bor,colour)

        ev = self.hard_code_eva_function(piece_difference, d_heurii, danger_piece, colour_p[colour], colour_e[colour])

        rew += self.check_heuristic_rew(colour_e, next_bor, colour, d_heurii)

        return (rew, d_heurii, uti, ev)


    def hard_code_eva_function(self, pieces_difference : int, reduced_heuristic : float, danger_pieces : int, players, player_exit) -> float:
        """
        1. # possible safety movement (*1)
        2. reduced heuristic to dest (positive means increased, negative means decreased) *(-2)
        3. # of piece in danger (could be taken by opponent by one JUMP action) *(-5)
        """
        t = len(players) + player_exit
        if t < 4:
            return (20) *pieces_difference + (-2)*reduced_heuristic + danger_pieces * (-10)
        else:
            return (5) *pieces_difference + (-8)*reduced_heuristic + danger_pieces * (-20)


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
        heuri = 0

        tmp_h = []
        for p in players:
            tmp_h.append(self.cost[colour][p])

        tmp_h.sort()
        if player_exit == -1:
            return sum(tmp_h)
        if len(players) + player_exit >= 4:
            heuri = sum(tmp_h[:4 - (player_exit)])
        else:
            heuri = sum(tmp_h)
            heuri =heuri + (4 - (len(players) + player_exit)) *10

        return heuri

    def cal_rheu(self, cur_state, next_state, colour, player_exit):
        cur_pl = [x for x in cur_state.keys() if cur_state[x] == colour]
        nxt_pl = [x for x in next_state.keys() if next_state[x] == colour]
        

        cur_heuri = self.heuristic(cur_pl, colour, player_exit)
        nxt_heuri = self.heuristic(nxt_pl, colour, player_exit)

        return nxt_heuri - cur_heuri

    def player_es(self, colour_e, exit_this):
        # only red here wait for more colours
        rest_ps = [colour_e[k] for k in self.arrange]

        if exit_this:
            rest_ps[0] = rest_ps[0] + 1

        return rest_ps


    def cal_heuristic(self, suc_bo, colour, colour_exit):
        e_c = [
            "red",
            "green",
            "blue"
        ]

        heuris = [self.heuristic([x for x in suc_bo.keys() if suc_bo[x] == c],c,colour_exit[c]) for c in self.arrange]

        return heuris

    def cal_pdiff(self, cur_state, next_state, colour):
        c_or = [k for k in cur_state.keys() if cur_state[k] != "empty" and cur_state[k] == colour]
        n_r = [k for k in next_state.keys() if next_state[k] != "empty" and next_state[k] == colour]

        c_ors = len(c_or)
        n_s = len(n_r)
        return n_s - c_ors

    def cal_dpiei(self,cur_state, next_state,colour):
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


    def check_heuristic_rew(self, colour_exit, suc_bo, colour, d_heur):
        n_r = [k for k in suc_bo.keys() if suc_bo[k] != "empty" and suc_bo[k] == colour]
        exited = colour_exit[colour]

        count = exited + len(n_r)

        if d_heur > 0:
            return config.D_HEURISTIC
        elif d_heur == 0:
            return config.D_HEURISTIC_HORIZONTAL

        return 0