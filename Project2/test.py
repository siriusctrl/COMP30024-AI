import VanGame.__init__ as v
import VanGame.strategy as s
import VanGame.player as p

v.test()

play = p.Player("blue")
s.get_possible_moves(play.current_board, play.colour, play.colour_p)
