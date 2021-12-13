import math
import random

class InvalidMove(Exception):
    pass

class Game:
    def __init__(self):
        self.board = Board()
        self.white_player = Player("w", self.board)
        self.blue_player = Player("b", self.board)
        self.curr_turn = 1
        self.furthest_turn = 1

    def get_turn(self):
        return self.curr_turn

    def move(self, worker_letter, direction_str):
        if worker_letter == "A":
            worker = self.white_player.workers[0]
        elif worker_letter == "B":
            worker = self.white_player.workers[1]
        elif worker_letter == "Y":
            worker = self.blue_player.workers[0]
        else:
            worker = self.blue_player.workers[1]

        direction = self.board.directions[direction_str]
        org_slot = worker.slot
        new_row = org_slot.row + direction[0]
        new_col = org_slot.col + direction[1]
        if new_row > 5 or new_row < 1 or new_col > 5 or new_col < 1:
            raise InvalidMove
        new_slot = self.board.slots[new_row-1][new_col-1]
        if new_slot.worker != 0 or new_slot.level == 4 or new_slot.level > org_slot.level + 1:
            raise InvalidMove
        new_slot.worker = worker
        org_slot.worker = 0
        worker.slot = new_slot

    def build(self, worker_letter, direction_str):
        if worker_letter == "A":
            worker = self.white_player.workers[0]
        elif worker_letter == "B":
            worker = self.white_player.workers[1]
        elif worker_letter == "Y":
            worker = self.blue_player.workers[0]
        else:
            worker = self.blue_player.workers[1]

        direction = self.board.directions[direction_str]
        slot = worker.slot
        new_row = slot.row + direction[0]
        new_col = slot.col + direction[1]
        if new_row > 5 or new_row < 1 or new_col > 5 or new_col < 1:
            raise InvalidMove
        build_slot = self.board.slots[new_row-1][new_col-1]
        if build_slot.worker != 0 or build_slot.level == 4:
            raise InvalidMove
        else:
            build_slot.level += 1

class Board:
    def __init__(self):
        self.slots = []

        for i in range(5):
            row = []
            for j in range(5):
                row.append(Slot(i + 1, j + 1))
            self.slots.append(row)

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
        self.possible_moves = []

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

    def find_possible_moves(self, board):
        self.possible_moves = []

        if self.workers[0].slot.level == 3 or self.workers[1].slot.level == 3:
            return True

        for w in self.workers:
            for move_d in board.directions:
                move_direction = board.directions[move_d]
                org_slot = w.slot
                new_row = org_slot.row + move_direction[0]
                new_col = org_slot.col + move_direction[1]
                if new_row > 5 or new_row < 1 or new_col > 5 or new_col < 1:
                    continue
                new_slot = board.slots[new_row-1][new_col-1]
                if new_slot.worker != 0 or new_slot.level == 4 or new_slot.level > org_slot.level + 1:
                    continue

                for build_d in board.directions:
                    build_direction = board.directions[build_d]
                    build_row = new_slot.row + build_direction[0]
                    build_col = new_slot.col + build_direction[1]
                    if build_row > 5 or build_row < 1 or build_col > 5 or build_col < 1:
                        continue
                    build_slot = board.slots[build_row-1][build_col-1]
                    if build_slot.worker != 0 or build_slot.level == 4:
                        continue

                    self.possible_moves.append([w.name, move_d, build_d])

    def height_score(self, s1, s2):
        return s1.level + s2.level

    def center_score(self, s1, s2):
        score = 0

        if s1.row == 3 and s1.col == 3:
            score += 2
        elif s1.row not in [1,5] and s1.col not in [1,5]:
            score += 1

        if s2.row == 3 and s2.col == 3:
            score += 2
        elif s2.row not in [1,5] and s2.col not in [1,5]:
            score += 1

        return score

    def distance_score(self, s1, s2, opp_player):
        distance = 0

        for w in opp_player.workers:
            distance += min(max(abs(s1.row - w.slot.row), abs(s1.col - w.slot.col)), max(abs(s2.row - w.slot.row), abs(s2.col - w.slot.col)))

        return 8 - distance

    def move_score(self, s1, s2, opp_player):
        if s1.level == 3 or s2.level == 3:
            return float("inf")
        else:
            return 3*self.height_score(s1, s2) + 2*self.center_score(s1, s2) + self.distance_score(s1, s2, opp_player)

    def heuristic(self, board, opp_player):
        ordered_moves = []

        for m in self.possible_moves:
            if self.workers[0].name == m[0]:
                moved_worker_slot = self.workers[0].slot
                other_worker_slot = self.workers[1].slot
            else:
                moved_worker_slot = self.workers[1].slot
                other_worker_slot = self.workers[0].slot

            move_direction = board.directions[m[1]]
            new_row = moved_worker_slot.row + move_direction[0]
            new_col = moved_worker_slot.col + move_direction[1]
            new_slot = board.slots[new_row-1][new_col-1]
            move_score = self.move_score(new_slot, other_worker_slot, opp_player)
            
            if ordered_moves == [] or move_score > ordered_moves[0][1]:
                ordered_moves = []
                ordered_moves.append((m, move_score))
            elif move_score == ordered_moves[0][1]:
                ordered_moves.append((m, move_score))

        return random.choice(ordered_moves)[0]
