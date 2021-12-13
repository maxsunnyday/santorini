from santorini_game import *
import sys
import random

class OwnerError(Exception):
    pass

class SantoriniCLI:
    """Display board and prompt a move"""
    def __init__(self, player1="random", player2="random"):
        self.game = Game()
        self._player1_type = player1
        self._player2_type = player2
            
    def run(self):
        while True:
            print(self.game.board)
            # check if game is over

            # fetch current turn number
            curr_turn = self.game.get_turn()
            # if odd, white moves. if even, blue moves.
            if (curr_turn % 2) != 0:
                print("Turn: {}, white (AB)".format(curr_turn))
                self.white_turn()
            else:
                print("Turn: {}, blue (YZ)".format(curr_turn))
                self.blue_turn()
            
            self.game.curr_turn += 1
            

            # while True:
            #     try:
            #         move = input("Select a direction to move (n, ne, e, se, s, sw, w, nw)\n")
            #         break
            #     except ValueError:
            #         print("Please try again with a valid date in the format YYYY-MM-DD.")

            # while True:
            #     try:
            #         build = input("Select a direction to build (n, ne, e, se, s, sw, w, nw)\n")
            #         break
            #     except ValueError:
            #         print("Please try again with a valid date in the format YYYY-MM-DD.")

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
            pass
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
            pass
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
    thing = SantoriniCLI()
    thing.run()