import random
from copy import deepcopy

class OwnerError(Exception):
    pass

class InvalidMove(Exception):
    pass

class Game:
    def __init__(self, board=0, white=0, blue=0, turn=1):
        # initilize everything unless its passed in as argument
        if board == 0:
            self.board = Board()
        else:
            self.board = board

        if white == 0:
            self.white_player = Player("w", self.board)
        else:
            self.white_player = white

        if blue == 0:
            self.blue_player = Player("b", self.board)
        else:
            self.blue_player = blue
        
        self.curr_turn = turn

    # deep copies everything within game and maintains relationship between slots and workers
    def copy(self):
        white = deepcopy(self.white_player)
        blue = deepcopy(self.blue_player)
        board = deepcopy(self.board)
        turn = deepcopy(self.curr_turn)

        # copies all the individual slots
        for i in range(len(self.board.slots)):
            for j in range(len(self.board.slots[i])):
                board.slots[i][j] = deepcopy(self.board.slots[i][j])
                board.slots[i][j].worker = deepcopy(self.board.slots[i][j].worker)

        # copies workers A and B
        for w in range(len(self.white_player.workers)):
            org_worker = self.white_player.workers[w]
            white.workers[w] = deepcopy(org_worker)
            white.workers[w].slot = board.slots[org_worker.slot.row-1][org_worker.slot.col-1]

        # copies worker Y and Z
        for w in range(len(self.blue_player.workers)):
            org_worker = self.blue_player.workers[w]
            blue.workers[w] = deepcopy(org_worker)
            blue.workers[w].slot = board.slots[org_worker.slot.row-1][org_worker.slot.col-1]

        return Game(board, white, blue, turn)

    def get_turn(self):
        return self.curr_turn

    def move(self, worker_letter, direction_str):
        # determine which worker is moving
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
        # find new slot based on direction
        new_row = org_slot.row + direction[0]
        new_col = org_slot.col + direction[1]
        # invalid if square is outside the board
        if new_row > 5 or new_row < 1 or new_col > 5 or new_col < 1:
            raise InvalidMove
        new_slot = self.board.slots[new_row-1][new_col-1]
        # invalid if slot has a dome or has a worker on it
        if new_slot.worker != 0 or new_slot.level == 4 or new_slot.level > org_slot.level + 1:
            raise InvalidMove
        
        # move worker from org_slot to new_slot
        new_slot.worker = worker
        org_slot.worker = 0
        worker.slot = new_slot

    def build(self, worker_letter, direction_str):
        # determine which worker is building
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
        # find new slot based on direction
        new_row = slot.row + direction[0]
        new_col = slot.col + direction[1]
        # invalid if square is outside the board
        if new_row > 5 or new_row < 1 or new_col > 5 or new_col < 1:
            raise InvalidMove
        build_slot = self.board.slots[new_row-1][new_col-1]
        # invalid if slot has a dome or has a worker on it
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

        # initialize workers
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

        # if either worker is on a level 3 building, the player wins
        if self.workers[0].slot.level == 3 or self.workers[1].slot.level == 3:
            return True

        for w in self.workers:
            # find all possible directions each worker can move in
            for move_d in board.directions:
                move_direction = board.directions[move_d]
                org_slot = w.slot
                new_row = org_slot.row + move_direction[0]
                new_col = org_slot.col + move_direction[1]
                # skip if outside of board
                if new_row > 5 or new_row < 1 or new_col > 5 or new_col < 1:
                    continue
                new_slot = board.slots[new_row-1][new_col-1]
                # skip if slot has worker or is too high up or is a dome
                if new_slot.worker != 0 or new_slot.level == 4 or new_slot.level > org_slot.level + 1:
                    continue
                
                # find all possible directions each worker can build in
                for build_d in board.directions:
                    build_direction = board.directions[build_d]
                    build_row = new_slot.row + build_direction[0]
                    build_col = new_slot.col + build_direction[1]
                    # skip if outside of board
                    if build_row > 5 or build_row < 1 or build_col > 5 or build_col < 1:
                        continue
                    build_slot = board.slots[build_row-1][build_col-1]
                    # skip if worker is on it or has a dome
                    if (build_slot.worker != 0 and build_slot != org_slot) or build_slot.level == 4:
                        continue

                    self.possible_moves.append([w.name, move_d, build_d])

    def height_score(self, s1, s2):
        return s1.level + s2.level

    def center_score(self, s1, s2):
        score = 0

        # middle square is 2 points, inner ring is 1 point, outer ring is 0 points
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
            # assign infinity to move if it results in moving to a level 3 building (win)
            return float("inf")
        else:
            return 3*self.height_score(s1, s2) + 2*self.center_score(s1, s2) + 1*self.distance_score(s1, s2, opp_player)

    def heuristic(self, board, opp_player):
        best_moves = []

        # calculate heuristic for all possible moves
        for m in self.possible_moves:
            # determine which worker is being moved
            if self.workers[0].name == m[0]:
                moved_worker_slot = self.workers[0].slot
                other_worker_slot = self.workers[1].slot
            else:
                moved_worker_slot = self.workers[1].slot
                other_worker_slot = self.workers[0].slot

            move_direction = board.directions[m[1]]
            # find slot based on direction
            new_row = moved_worker_slot.row + move_direction[0]
            new_col = moved_worker_slot.col + move_direction[1]
            new_slot = board.slots[new_row-1][new_col-1]
            move_score = self.move_score(new_slot, other_worker_slot, opp_player)
            
            # clear array and add move if score is greater than the current best move
            if best_moves == [] or move_score > best_moves[0][1]:
                best_moves = []
                best_moves.append((m, move_score))
            elif move_score == best_moves[0][1]:
                # if score is the same as the current best move, add move to array
                best_moves.append((m, move_score))

        # if there are multiple moves with the best score, randomly break ties
        return random.choice(best_moves)[0]
