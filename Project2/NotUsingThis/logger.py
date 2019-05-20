import datetime
import json, time
import os.path

EXPFOPATH = "./rec"

class Logger:

    def __init__(self, colour):
        self.log = []
        self.colour = colour

    def add_log(self, nxt_board, *args, **kwargs):
        '''
        log keys:
            colour,
            board,
            action,
            utility,
            rew,
            d_heur
        '''
        kwargs["colour"] = self.colour

        new = {str(m): nxt_board[m] for m in nxt_board.keys()}
        kwargs["board"] = new

        keys = [
            ["action", ("NONE", None)], 
            ["utility", []],
            ["rew", 0],
            ["d_heur", 0],
            ["ev", 0],
            ["turns", 0]
        ]

        for [key, value] in keys:
            if not (key in kwargs):
                kwargs[key] = value

        self.log.append(
            kwargs
        )

    def update_last_log(self, index, delta):
        self.log[len(self.log)-1][index]+= delta

    def get_last_log(self, index):
        return self.log[len(self.log)-1][index]


    def export_log(self, status):
        with open(os.path.join(EXPFOPATH, status + str(time.mktime(datetime.datetime.now().timetuple() )) + "cao" + self.colour + "jiba" + ".txt"), "w+") as e:
            e.write(json.dumps(self.log))
        