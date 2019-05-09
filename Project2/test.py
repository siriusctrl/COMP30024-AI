import VanGame.__init__ as v
import VanGame.strategy as s
import VanGame.player as p

import HardCode.strategy as sp



def cal_py(py, pa):

    thr = pa[0], -(pa[0]+pa[1]), pa[1]
    din = []
    for pj in py:
        pjt = pj[0], -(pj[0]+pj[1]), pj[1]

        dn = (abs(thr[0] - pjt[0]) + abs(thr[1] - pjt[1]) + abs(thr[2] - pjt[2]))/2

        din.append((pj, dn))
    
    return din
    
    
ji = cal_py([(-3, 0), (-3, 1), (-3, 2), (-2, 3)],
            (-3, 0))

print(ji)

v.test()

play = p.Player("blue")
sb = s.Strategy(play.goal)
'''sb.get_possible_moves(play.current_board, play.colour, play.colour_p, play.goal)'''
sb.get_board(play.current_board, play.colour)

st = sp.Strategy(play.goal)


'''mv = st.get_possible_moves(play.current_board, play.colour, play.colour_p, play.goal)
print("cao" + str(mv))'''