import HardCode.utils as utils
import random
import math

import queue


# 2 utility:
#  pieces less than 4 then up eating utility (include exit pieces)
#  more or equal to 4 then prevent to be eaten
class Strategy:

    def __init__(self, goals):
        self.cost = {}

        self.goals = goals

        tmp_current_board = {x: "empty" for x in utils.CELLS}

        for g in self.goals:
            self.cost_from_goal(g, tmp_current_board)
        #utils.print_board(self.cost)

        self.log = []

        

        # print(self.cost)



    def get_possible_moves(self, current_board, colour, colour_p, goal, colour_e):

        ps = colour_p[colour]

        ot = [y for x in colour_p.keys() for y in colour_p[x] if x != colour]


        for a in ps:
            if a in goal:
                next_board = current_board.copy()
                next_board[a] = "empty"

                self.log.append(
                    (next_board, 0, 
                    

            
                self.hard_code_eva_function(
                    self.cal_pdiff(current_board, next_board, colour), 
                    self.cal_rheu(current_board, next_board, colour, colour_e[colour]), 
                    self.cal_dpiei(current_board, next_board, colour),
                    colour_p[colour],
                    colour_e[colour]), "EXIT",
                ))

                return "EXIT", a

        all_ms = []
        for p in ps:
            all_ms = all_ms + utils.find_next(p, current_board)

        if len(all_ms):
            all_state_players = []
            for i in all_ms:
                '''tmp_p = ps.copy()

                tmp_o=ot.copy()'''

                ur_b = current_board.copy()

                ur_b[i[0]]="empty"
                ur_b[i[1]]=colour

                '''tmp_p.remove(i[0])
                tmp_p.append(i[1])'''

                if i[2] == 2:
                    if ur_b[i[3]]!="empty":
                        ur_b[i[3]]=colour
                
                all_state_players.append(ur_b)
            # print(all_state_players)
            # print(all_state_players, ev)
            ev = []

            for p in all_state_players:
                cn = current_board
                pdiff = self.cal_pdiff(cn, p, colour)
                rheu = self.cal_rheu(cn, p, colour, colour_e[colour])
                dpiei = self.cal_dpiei(cn, p, colour)

            
                ev.append(self.hard_code_eva_function(pdiff, rheu, dpiei, colour_p[colour], colour_e[colour]))
            
            # print(ev)

            max_e = max(ev)
            max_ein = ev.index(max_e)

            
            # print(all_ms)

            cm = all_ms[max_ein]



            if cm[2] == 1:
                self.log.append(
                    (all_state_players[max_ein], 0, ev[max_ein], "MOVE")
                )
                return "MOVE", (cm[0], cm[1])
                
            elif cm[2] == 2:
                self.log.append(
                    (all_state_players[max_ein], 0, ev[max_ein], "JUMP")
                )
                return "JUMP", (cm[0], cm[1])
            # return all_ms[math.floor(random.random() * len(all_ms))]
        else:
            self.log.append(
                (current_board.copy(), 0, 0, "PASS")
            )
            return "PASS", None

        pass


    def heuristic(self, players, colour, player_exit):
        heuri = 0

        tmp_h = []
        for p in players:
            tmp_h.append(self.cost[p])

        tmp_h.sort()
        if player_exit == -1:
            return sum(tmp_h)
        if len(players) + player_exit >= 4:
            heuri = sum(tmp_h[:4 - (player_exit)])
        else:
            heuri = sum(tmp_h)
            heuri =heuri + (4 - (len(players) + player_exit)) *10

        return heuri

    def cal_pdiff(self, cur_state, next_state, colour):
        c_or = [k for k in cur_state.keys() if cur_state[k] != "empty" and cur_state[k] != colour]
        n_r = [k for k in next_state.keys() if next_state[k] != "empty" and next_state[k] != colour]

        c_ors = len(c_or)
        n_s = len(n_r)
        return c_ors - n_s
    
    def cal_rheu(self, cur_state, next_state, colour, player_exit):
        cur_pl = [x for x in cur_state.keys() if cur_state[x] == colour]
        nxt_pl = [x for x in next_state.keys() if next_state[x] == colour]
        

        cur_heuri = self.heuristic(cur_pl, colour, player_exit)
        nxt_heuri = self.heuristic(nxt_pl, colour, player_exit)

        return nxt_heuri - cur_heuri

    def cal_dpiei(self,cur_state, next_state,colour):
        nxt_pl = [k for k in next_state.keys() if next_state[k] == colour]
        nxt_ot = [k for k in next_state.keys() if next_state[k] != "empty" and next_state[k] != colour]
        

        tmp_current_board = {x: "empty" for x in utils.CELLS}
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

    def cost_from_goal(self, goal: tuple, tmp_current_board: dict) -> None:
        """
        Receive a goal coordinate and block list then calculate a pre
        """

        q = queue.Queue()

        # (cost_from_goal, ((MOVE_counter, JUMP_counter), coordinates))
        q.put((0, ((0, 0), goal)))

        cost = {goal: 0}

        self.cost[goal] = 1

        while not q.empty():

            current = q.get()

            successors = utils.find_next(current[1][1], tmp_current_board)
            child_cost = current[0] + 1

            for s in successors:
                if s[1] not in cost:
                    # since we are using BFS to findNext the coordinates
                    # better solution will be always expanded first

                    # s[1] indicates if the next move s is achieved by move (1) or jump (2)
                    # used in calculating heuristic g
                    # which separately consider jump and moves since jump does not need to /2
                    # to reach a admissible heuristic
                    # toSuc = (MOVE_counter, JUMP_counter) <- counting both moves and jumps
                    if s[2] == 1:
                        s_counter = (current[1][0][0] + 1, current[1][0][1])
                    elif s[2] == 2:
                        s_counter = (current[1][0][0], current[1][0][1] + 1)

                    q.put((child_cost, (s_counter, s[1])))
                    cost[s[1]] = child_cost

                    # if the cost less then update the closest cost
                    h = s_counter[0] + 1

                    '''if s_counter[0] % 2 == 0:
                        h = h + (s_counter[0] / 2 + s_counter[1] + 1)
                    else:
                        h = h + ((s_counter[0] - 1) / 2 + s_counter[1] + 2)'''

                    if s[1] not in self.cost:
                        self.cost[s[1]] = h
                    elif self.cost[s[1]] > h:
                        self.cost[s[1]] = h

        return
