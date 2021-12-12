import math

class Game:
    def __init__(self):
        self.board = Board()
        self.white_player = Player("w", self.board)
        self.black_player = Player("b", self.board)
        self._curr_turn = 1
        self.furthest_turn = 1
        self.directions = {
            "s": [1, 0],
            "se": [1, 1],
            "e": [0, 1],
            "ne": [-1, 1],
            "n": [-1, 0],
            "nw": [-1, -1],
            "w": [0, -1],
            "sw": [1, -1]
        }

    def get_turn(self):
        return self._curr_turn

    def move(self, worker_letter, direction_str):
        if worker_letter == "A":
            worker = self.white_player.workers[0]
        elif worker_letter == "B":
            worker = self.white_player.workers[1]
        elif worker_letter == "Y":
            worker = self.white_player.workers[1]
        else:
            player = self.black_player

        

    def build(self, worker, direction):
        pass

class Board:
    def __init__(self):
        self.slots = []

        for i in range(5):
            row = []
            for j in range(5):
                row.append(Slot(i + 1, j + 1))
            self.slots.append(row)

    def __repr__(self):
        return_string = ""
        board_separator = "+--+--+--+--+--+"
        new_line = "\n"
        return_string += board_separator

        for row in self.slots:
            return_string += new_line
            
            for s in row:
                return_string += "|"
                return_string += s.__repr__()

            return_string += "|\n"
            return_string += board_separator
        
        return return_string


class Slot:
    def __init__(self, row, col, worker = 0):
        self.row = row
        self.col = col
        self.level = 0
        self.worker = worker

    def __repr__(self):
        if self.worker == 0:
            return f"{self.level} "
        else:
            return f"{self.level}{self.worker}"

class Worker:
    def __init__(self, letter, slot):
        self.name = letter
        self.slot = slot

    def __repr__(self):
        return self.name

class Player:
    def __init__(self, color, board):
        self.color = color

        if color == "w":
            self.workers = []
            w1 = Worker("A", board.slots[3][1])
            self.workers.append(w1)
            board.slots[3][1].worker = w1
            w2 = Worker("B", board.slots[1][3])
            self.workers.append(w2)
            board.slots[1][3].worker = w2
        else:
            self.workers = []
            w1 = Worker("Y", board.slots[1][1])
            self.workers.append(w1)
            board.slots[1][1].worker = w1
            w2 = Worker("Z", board.slots[3][3])
            self.workers.append(w2)
            board.slots[3][3].worker = w2

game = Game()  
print(game.board)
