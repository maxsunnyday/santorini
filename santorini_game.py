import math

class Game:
    def __init__(self):
        self.board = Board()

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
        board_separator = "+--+--+--+--+--+\n"
        return_string += board_separator

        for row in self.slots:
            for s in row:
                return_string += "|"
                return_string += s.__repr__()

            return_string += "|\n"
            return_string += board_separator
        
        return return_string


class Slot:
    def __init__(self, row, col):
        self.row = row + 1
        self.col = col + 1
        self.level = 0
        self.worker = 0

    def __repr__(self):
        if self.worker == 0:
            return f"{self.level} "
        else:
            return f"{self.level}{self.worker}"

class Worker:
    def __init__(self):
        self.position = []

class Player:
    def __init__(self):
        self.workers = []

board = Board()  
print(board)