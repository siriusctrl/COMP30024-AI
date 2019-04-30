import VanGame.__init__ as v
import VanGame.strategy as s
import VanGame.player as p

import HardCode.strategy as sp

BLUE_MAPPING = {
    (0, -3): (-3, 3),
    (1, -3): (-3, 2),
    (2, -3): (-3, 1),
    (3, -3): (-3, 0),
    (-1, -2): (-2, 3),
    (0, -2): (-2, 2),

}

RED_TO_BLUE = {
    -3: (0, 3),
    -2: (-1, 3),
    -1: (-2, 3),
    0: (-3, 3),
    1: (-3, 2),
    2: (-3, 1),
    3: (-3, 0)
}

BLUE_MAPPING = {k: (k[1], range(RED_TO_BLUE[k[1]][0], RED_TO_BLUE[k[1][1]]).index(k[0])) for k in CELLS}

def to_blue_main(red_main_board):


v.test()

play = p.Player("blue")
sb = s.Strategy(play.goal)
'''sb.get_possible_moves(play.current_board, play.colour, play.colour_p, play.goal)'''
sb.get_board(play.current_board, play.colour)

st = sp.Strategy(play.goal)


'''mv = st.get_possible_moves(play.current_board, play.colour, play.colour_p, play.goal)
print("cao" + str(mv))'''