import VanGame.__init__ as v
import VanGame.strategy as s
import VanGame.player as p

import HardCode.strategy as sp

v.test()

play = p.Player("blue")
sb = s.Strategy(play.goal)
'''sb.get_possible_moves(play.current_board, play.colour, play.colour_p, play.goal)'''
sb.get_board(play.current_board, play.colour)

st = sp.Strategy(play.goal)


'''mv = st.get_possible_moves(play.current_board, play.colour, play.colour_p, play.goal)
print("cao" + str(mv))'''