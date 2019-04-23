import HardCode.utils as utils
import random
import math

import queue


class Strategy:

    def __init__(self, goals):
        self.cost = {}

        self.goals = goals

        tmp_current_board = {x: "empty" for x in utils.CELLS}

        for g in self.goals:
            self.cost_from_goal(g, tmp_current_board)
        utils.print_board(self.cost)

        print(self.cost)



    def get_possible_moves(self, current_board, colour, colour_p, goal):

        ps = colour_p[colour]

        ot = [y for x in colour_p.keys() for y in colour_p[x] if x != colour]


        for a in ps:
            if a in goal:
                return "EXIT", a

        all_ms = []
        for p in ps:
            all_ms = all_ms + utils.find_next(p, current_board)

        if len(all_ms):
            all_state_players = []
            for i in all_ms:
                tmp_state_play = []
                tmp_p = ps.copy()

                tmp_o=ot.copy()

                tmp_p.remove(i[0])
                tmp_p.append(i[1])

                if i[2] == 2:
                    if i[3] in tmp_o:
                        tmp_p.append(i[3])
                        tmp_o.remove(i[3])
                
                tmp_state_play.append(tmp_p)
                tmp_state_play.append(tmp_o)

                all_state_players.append(tmp_state_play)
            print(all_state_players)
            # print(all_state_players, ev)
            ev = []

            for p in all_state_players:
                cn = [ps, ot]
                pdiff = self.cal_pdiff(cn, p)
                rheu = self.cal_rheu(cn, p)
                dpiei = self.cal_dpiei(cn, p)

            
                ev.append(self.hard_code_eva_function(pdiff, rheu, dpiei))
            
            print(ev)

            max_e = max(ev)
            max_ein = ev.index(max_e)



            
            print(all_ms)

            cm = all_ms[max_ein]
            if cm[2] == 1:
                return "MOVE", (cm[0], cm[1])
            elif cm[2] == 2:
                return "JUMP", (cm[0], cm[1])
            # return all_ms[math.floor(random.random() * len(all_ms))]
        else:
            return "PASS", None

        pass


    def heuristic(self, players):
        heuri = 0
        for p in players:
            heuri =heuri + self.cost[p]

        return heuri
        pass

    def cal_pdiff(self, cur_state, next_state):
        return len(next_state[1]) - len(cur_state[1])
    
    def cal_rheu(self, cur_state, next_state):
        cur_pl = cur_state[0]
        nxt_pl = next_state[0]

        cur_heuri = self.heuristic(cur_pl)
        nxt_heuri = self.heuristic(nxt_pl)

        return nxt_heuri - cur_heuri

    def cal_dpiei(self,cur_state, next_state):
        nxt_pl = next_state[0]
        nxt_ot = next_state[1]

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


    def hard_code_eva_function(self, pieces_difference : int, reduced_heuristic : float, danger_pieces : int) -> float:
        """
        1. # possible safety movement (*1)
        2. reduced heuristic to dest (positive means increased, negative means decreased) *(-2)
        3. # of piece in danger (could be taken by opponent by one JUMP action) *(-5)
        """
        return (3) *pieces_difference + (-5)*reduced_heuristic + danger_pieces * (-10)

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
