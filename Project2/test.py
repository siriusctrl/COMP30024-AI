import VanGame.__init__ as v
import VanGame.strategy as s
import VanGame.player as p

import HardCode.strategy as sp

v.test()

play = p.Player("blue")
s.get_possible_moves(play.current_board, play.colour, play.colour_p, play.goal)

st = sp.Strategy(play.goal)

mv = st.get_possible_moves(play.current_board, play.colour, play.colour_p, play.goal)
print("cao" + str(mv))