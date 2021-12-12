import math

class Game:
    def __init__(self, player1_type, player2_type):
        self.board = Board()
        self.white_player = Player("w", self.board, player1_type)
        self.black_player = Player("b", self.board, player2_type)
        self.curr_turn = 1
        self.furthest_turn = 1

    def get_turn(self):
        return self._curr_turn

class Board:
    def __init__(self):
        self.slots = []

        for i in range(5):
            row = []
            for j in range(5):
                row.append(Slot(i, j))
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
        self.row = row + 1
        self.col = col + 1
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
    def __init__(self, color, board, player_type):
        self.color = color
        self.player_type = player_type

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

# board = Board()  
# print(board)
