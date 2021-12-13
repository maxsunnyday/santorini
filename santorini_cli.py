from santorini_game import *
import sys

class OwnerError(Exception):
    pass

class SantoriniCLI:
    """Display board and prompt a move"""
    def __init__(self, player1="human", player2="human", undo="off", display_score="off"):
        self.game = Game()
        self._player1_type = player1
        self._player2_type = player2
        self.display_score = display_score
        self.undo = undo
            
    def run(self):
        while True:
            print(self.game.board)
            # check if game is over

            # fetch current turn number
            curr_turn = self.game.get_turn()
            # if odd, white moves. if even, blue moves.
            if (curr_turn % 2) != 0:
                # get current move_score if display score is on
                if self.display_score == "on":
                    player = self.game.white_player
                    score = f", ({player.height_score(player.workers[0].slot, player.workers[1].slot)}, {player.center_score(player.workers[0].slot, player.workers[1].slot)}, {player.distance_score(player.workers[0].slot, player.workers[1].slot, self.game.blue_player)})"
                else:
                    score = ""
                print(f"Turn: {curr_turn}, white (AB){score}")
                self.white_turn()
            else:
                # get current move_score if display score is on
                if self.display_score == "on":
                    player = self.game.blue_player
                    score = f", ({player.height_score(player.workers[0].slot, player.workers[1].slot)}, {player.center_score(player.workers[0].slot, player.workers[1].slot)}, {player.distance_score(player.workers[0].slot, player.workers[1].slot, self.game.white_player)})"
                else:
                    score = ""
                print(f"Turn: {curr_turn}, blue (YZ){score}")
                self.blue_turn()
            
            self.game.curr_turn += 1

    def white_turn(self):
        if self.game.white_player.find_possible_moves(self.game.board):
            print("white has won")
            sys.exit(0)
        elif self.game.blue_player.find_possible_moves(self.game.board):
            print("blue has won")
            sys.exit(0)
        elif len(self.game.white_player.possible_moves) == 0:
            print("blue has won")
            sys.exit(0)

        # check if player is human
        if self._player1_type == "random":
            move = random.choice(self.game.white_player.possible_moves)
            self.game.move(move[0], move[1])
            self.game.build(move[0], move[2])
            print(f"{move[0]},{move[1]},{move[2]}")

        elif self._player1_type == "heuristic":
            move = self.game.white_player.heuristic(self.game.board, self.game.blue_player)
            self.game.move(move[0], move[1])
            self.game.build(move[0], move[2])
            print(f"{move[0]},{move[1]},{move[2]}")
        else:
            # self._player1_type == "human":
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
        if self.game.white_player.find_possible_moves(self.game.board):
            print("white has won")
            sys.exit(0)
        elif self.game.blue_player.find_possible_moves(self.game.board):
            print("blue has won")
            sys.exit(0)
        elif len(self.game.blue_player.possible_moves) == 0:
            print("white has won")
            sys.exit(0)

        # check if player is human
        if self._player2_type == "random":
            move = random.choice(self.game.blue_player.possible_moves)
            self.game.move(move[0], move[1])
            self.game.build(move[0], move[2])
            print(f"{move[0]},{move[1]},{move[2]}")
        elif self._player2_type == "heuristic":
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
        
if __name__ == "__main__":
    if len(sys.argv) <= 1:
        thing = SantoriniCLI()
    elif len(sys.argv) == 2:
        thing = SantoriniCLI(sys.argv[1])
    elif len(sys.argv) == 3:
        thing = SantoriniCLI(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 4:
        thing = SantoriniCLI(sys.argv[1], sys.argv[2], sys.argv[3])
    elif len(sys.argv) == 5:
        thing = SantoriniCLI(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        print("too many command-line arguments")
    
    thing.run()