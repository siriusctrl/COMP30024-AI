import HardCode3.utils as utils
import HardCode3.strategy as strategy
import HardCode3.config as config
import copy


class Player:

    def __init__(self, colour):
        """
        This method is called once at the beginning of the game to initialise
        your player. You should use this opportunity to set up your own internal
        representation of the game state, and any other information about the 
        game state you would like to maintain for the duration of the game.

        The parameter colour will be a string representing the player your 
        program will play as (Red, Green or Blue). The value will be one of the 
        strings "red", "green", or "blue" correspondingly.
        """
        # print(colour)
        self.colour = colour

        # player's goal
        self.goal = config.GOALS[colour]

        # player's starting point
        self.colour_p = {}

        # board in each turn
        self.current_board = {}

        self.colour_exit = {
            "red": 0,
            "blue": 0,
            "green": 0
        }

        self.turn = 0

        self.strategy = strategy.Strategy(self.goal, self.colour)

        # TODO: Set up state representation.

        self.colour_p = copy.deepcopy(config.START)
        for a in config.CELLS:
            self.current_board[a] = "empty"
        for c in config.START.keys():
            for o in config.START[c]:
                self.current_board[o] = c

        # print(self.colour_p)
        # print(self.current_board)
        # print(self.goal)

    def action(self):
        """
        This method is called at the beginning of each of your turns to request
        a choice of action from your program.

        Based on the current state of the game, your player should select and
        return an allowed action to play on this turn. If there are no allowed
        actions, your player must return a pass instead. The action (or pass)
        must be represented based on the above instructions for representing
        actions.
        """
        # TODO: Decide what action to take.
        return self.strategy.get_possible_moves(self.current_board, self.colour, self.colour_p, self.goal, self.colour_exit, self.turn)

    def update(self, colour, action):
        """
        This method is called at the end of every turn (including your player’s 
        turns) to inform your player about the most recent action. You should 
        use this opportunity to maintain your internal representation of the 
        game state and any other information about the game you are storing.

        The parameter colour will be a string representing the player whose turn
        it is (Red, Green or Blue). The value will be one of the strings "red", 
        "green", or "blue" correspondingly.

        The parameter action is a representation of the most recent action (or 
        pass) conforming to the above in- structions for representing actions.

        You may assume that action will always correspond to an allowed action 
        (or pass) for the player colour (your method does not need to validate 
        the action/pass against the game rules).
        """
        # TODO: Update state representation in response to action.
        self.update_board(action, colour)

        self.turn = self.turn + 1

        for n in self.colour_exit.keys():
            if self.colour_exit[n] == 4:
                player_exited = self.colour_exit[self.colour]
                r = - (4 - player_exited) * config.EXIT_RW
                s_wi = "[2zzz]"
                if n == self.colour:
                    r += 0
                    s_wi = "[1win]"
                self.strategy.logger.update_last_log("rew", r)
                self.strategy.logger.export_log(s_wi)
                break

    def update_board(self, action, colour):
        if action[0] in ("MOVE", "JUMP"):
            self.current_board[action[1][0]] = "empty"
            self.current_board[action[1][1]] = colour
            self.colour_p[colour].remove(action[1][0])
            self.colour_p[colour].append(action[1][1])
            if action[0] in ("JUMP", ):
                fr = action[1][0]
                to = action[1][1]
                sk = (fr[0] + (to[0] - fr[0]) / 2, fr[1] + (to[1] - fr[1]) / 2)

                # well I dont freaking know what im thinking about
                if self.current_board[sk] != "empty" and self.current_board[sk] != colour:

                    self.colour_p[self.current_board[sk]].remove(sk)
                    self.colour_p[colour].append(sk)

                    lst = self.current_board[sk]
                    self.current_board[sk] = colour

                    tmp_tbr = self.current_board
                    pl = [m for m in tmp_tbr.keys() if tmp_tbr[m] == self.colour]
                    if lst == self.colour:
                        if(len(pl) >= 4):
                            self.strategy.logger.update_last_log("rew", -config.MORE_RW)
                            '''self.strategy.log[len(self.strategy.log)-1][1]-= config.MORE_RW'''
                        else:
                            self.strategy.logger.update_last_log("rew", -config.LESS_RW)
                            # self.strategy.log[len(self.strategy.log)-1][1] -= utils.LESS_RW
                    elif lst != self.colour and colour == self.colour:
                        if(len(pl) > 4):
                            self.strategy.logger.update_last_log("rew", config.MORE_RW)
                            # self.strategy.log[len(self.strategy.log)-1][1]+=utils.MORE_RW
                        else:
                            self.strategy.logger.update_last_log("rew", config.LESS_RW)
                            # self.strategy.log[len(self.strategy.log)-1][1] += utils.LESS_RW

        elif action[0] in ("EXIT",):
            self.current_board[action[1]] = "empty"
            self.colour_p[colour].remove(action[1])

            if colour not in self.colour_exit.keys():
                self.colour_exit[colour] = 0
            self.colour_exit[colour] += 1

        return

