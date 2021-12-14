from santorini_game import *
from copy import deepcopy
import sys

class SantoriniCLI:
    """Display board and prompt a move"""
    def __init__(self, player1="human", player2="human", undo="off", display_score="off"):
        self.game = Game()
        self._player1_type = player1
        self._player2_type = player2
        self._display_score = display_score
        self._undo = undo
        self.game_instances = [self.copy(self.game)]

    # deep copies everything within game and maintains relationship between slots and workers
    def copy(self, game):
        white = deepcopy(game.white_player)
        blue = deepcopy(game.blue_player)
        board = deepcopy(game.board)
        turn = deepcopy(game.curr_turn)

        # copies all the individual slots
        for i in range(len(game.board.slots)):
            for j in range(len(game.board.slots[i])):
                board.slots[i][j] = deepcopy(game.board.slots[i][j])
                board.slots[i][j].worker = deepcopy(game.board.slots[i][j].worker)

        # copies workers A and B
        for w in range(len(game.white_player.workers)):
            org_worker = game.white_player.workers[w]
            white.workers[w] = deepcopy(org_worker)
            white.workers[w].slot = board.slots[org_worker.slot.row-1][org_worker.slot.col-1]

        # copies worker Y and Z
        for w in range(len(game.blue_player.workers)):
            org_worker = game.blue_player.workers[w]
            blue.workers[w] = deepcopy(org_worker)
            blue.workers[w].slot = board.slots[org_worker.slot.row-1][org_worker.slot.col-1]

        return Game(board, white, blue, turn)
            
    def run(self):
        while True:
            print(self.game.board)
            # fetch current turn number
            curr_turn = self.game.get_turn()
            # if odd, white moves. if even, blue moves.
            if (curr_turn % 2) != 0:
                # display current move_score if display score is on
                if self._display_score == "on":
                    player = self.game.white_player
                    score = f", ({player.height_score(player.workers[0].slot, player.workers[1].slot)}, {player.center_score(player.workers[0].slot, player.workers[1].slot)}, {player.distance_score(player.workers[0].slot, player.workers[1].slot, self.game.blue_player)})"
                else:
                    score = ""

                print(f"Turn: {curr_turn}, white (AB){score}")
    
                # undo, redo, next functionality
                if self._undo == "on":
                    reload = 0

                    while True:
                        try:
                            history_input = input("undo, redo, or next\n")
                            if history_input == "undo":
                                if curr_turn > 1:
                                    self.game = self.copy(self.game_instances[curr_turn-2])
                                reload = 1
                                break
                            elif history_input == "redo":
                                if curr_turn < len(self.game_instances):
                                    self.game = self.copy(self.game_instances[curr_turn])
                                reload = 1
                                break
                            elif history_input == "next":
                                while curr_turn < len(self.game_instances):
                                    self.game_instances.pop()
                                self.white_turn()
                                break
                            else:
                                raise ValueError
                        except ValueError:
                            print("Not a valid command")

                    if reload == 1:
                        continue
                else:
                    self.white_turn()
            else:
                # display current move_score if display score is on
                if self._display_score == "on":
                    player = self.game.blue_player
                    score = f", ({player.height_score(player.workers[0].slot, player.workers[1].slot)}, {player.center_score(player.workers[0].slot, player.workers[1].slot)}, {player.distance_score(player.workers[0].slot, player.workers[1].slot, self.game.white_player)})"
                else:
                    score = ""

                print(f"Turn: {curr_turn}, blue (YZ){score}")
                
                # undo, redo, next functionality
                if self._undo == "on":
                    reload = 0

                    while True:
                        try:
                            history_input = input("undo, redo, or next\n")
                            if history_input == "undo":
                                if curr_turn > 1:
                                    self.game = self.copy(self.game_instances[curr_turn-2])
                                reload = 1
                                break
                            elif history_input == "redo":
                                if curr_turn < len(self.game_instances):
                                    self.game = self.copy(self.game_instances[curr_turn])
                                reload = 1
                                break
                            elif history_input == "next":
                                while curr_turn < len(self.game_instances):
                                    self.game_instances.pop()
                                self.blue_turn()
                                break
                            else:
                                raise ValueError
                        except ValueError:
                            print("Not a valid command")

                    if reload == 1:
                        continue
                else:
                    self.blue_turn()

            # end of turn
            self.game.curr_turn += 1
            self.game_instances.append(self.copy(self.game))

    def white_turn(self):
        # check if game is over
        if self.game.white_player.find_possible_moves(self.game.board):
            print("white has won")
            sys.exit(0)
        elif self.game.blue_player.find_possible_moves(self.game.board):
            print("blue has won")
            sys.exit(0)
        elif len(self.game.white_player.possible_moves) == 0:
            print("blue has won")
            sys.exit(0)

        # check if player is human, random, or heuristic
        if self._player1_type == "random":
            # randonly select from possible moves
            move = random.choice(self.game.white_player.possible_moves)
            self.game.move(move[0], move[1])
            self.game.build(move[0], move[2])
            print(f"{move[0]},{move[1]},{move[2]}")

        elif self._player1_type == "heuristic":
            # use heuristic calculation to choose best move
            move = self.game.white_player.heuristic(self.game.board, self.game.blue_player)
            self.game.move(move[0], move[1])
            self.game.build(move[0], move[2])
            print(f"{move[0]},{move[1]},{move[2]}")
        else:
            # ask for piece selection
            worker_input = "0" #just a garbage value to be adjusted later
            while True:
                try:
                    worker_input = input("Select a worker to move\n")
                    if worker_input == "Z" or worker_input == "Y":
                        raise OwnerError
                    elif worker_input not in ["A", "B"]:
                        raise ValueError
                    else:
                        # input is good. Player selected either A or B.
                        break
                except OwnerError:
                    print("That is not your worker")
                except ValueError:
                    print("Not a valid worker")
            # ask for desired move direction
            while True:
                valid_directions = ["n", "ne", "e", "se", "s", "sw", "w", "nw"]
                try:
                    move = input("Select a direction to move (n, ne, e, se, s, sw, w, nw)\n")
                    if move not in valid_directions:
                        raise ValueError
                    # validate move
                    self.game.move(worker_input, move)
                    break
                except ValueError:
                    print("Not a valid direction")
                except InvalidMove:
                    print("Cannot move {}".format(move))
            # now that move is done, build
            while True:
                valid_directions = ["n", "ne", "e", "se", "s", "sw", "w", "nw"]
                try:
                    build = input("Select a direction to build (n, ne, e, se, s, sw, w, nw)\n")
                    if build not in valid_directions:
                        raise ValueError
                    # validate and execute build
                    result = self.game.build(worker_input, build)
                    break
                except ValueError:
                    print("Not a valid direction")
                except InvalidMove:
                    print("Cannot build {}".format(build))
            # move and build are done

    def blue_turn(self):
        # check if game is over
        if self.game.white_player.find_possible_moves(self.game.board):
            print("white has won")
            sys.exit(0)
        elif self.game.blue_player.find_possible_moves(self.game.board):
            print("blue has won")
            sys.exit(0)
        elif len(self.game.blue_player.possible_moves) == 0:
            print("white has won")
            sys.exit(0)

        # check if player is human, random, or heuristic
        if self._player2_type == "random":
            # randonly select from possible moves
            move = random.choice(self.game.blue_player.possible_moves)
            self.game.move(move[0], move[1])
            self.game.build(move[0], move[2])
            print(f"{move[0]},{move[1]},{move[2]}")
        elif self._player2_type == "heuristic":
            # use heuristic calculation to choose best move
            move = self.game.blue_player.heuristic(self.game.board, self.game.white_player)
            self.game.move(move[0], move[1])
            self.game.build(move[0], move[2])
            print(f"{move[0]},{move[1]},{move[2]}")
        else: 
            # ask for piece selection
            worker_input = "0" #just a garbage value to be adjusted later
            while True:
                try:
                    worker_input = input("Select a worker to move\n")
                    if worker_input == "A" or worker_input == "B":
                        raise OwnerError
                    elif worker_input not in ["Y", "Z"]:
                        raise ValueError
                    else:
                        # input is good. Player selected either A or B.
                        break
                except OwnerError:
                    print("That is not your worker")
                except ValueError:
                    print("Not a valid worker")
            # ask for desired move direction
            while True:
                valid_directions = ["n", "ne", "e", "se", "s", "sw", "w", "nw"]
                try:
                    move = input("Select a direction to move (n, ne, e, se, s, sw, w, nw)\n")
                    if move not in valid_directions:
                        raise ValueError
                    # validate move
                    self.game.move(worker_input, move)
                    break
                except ValueError:
                    print("Not a valid direction")
                except InvalidMove:
                    print("Cannot move {}".format(move))
            # now that move is done, build
            while True:
                valid_directions = ["n", "ne", "e", "se", "s", "sw", "w", "nw"]
                try:
                    build = input("Select a direction to build (n, ne, e, se, s, sw, w, nw)\n")
                    if build not in valid_directions:
                        raise ValueError
                    # validate and execute build
                    result = self.game.build(worker_input, build)
                    break
                except ValueError:
                    print("Not a valid direction")
                except InvalidMove:
                    print("Cannot build {}".format(build))
            # move and build are done