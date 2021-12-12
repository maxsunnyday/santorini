from santorini_game import *
class OwnerError(Exception):
    pass
class SantoriniCLI:
    """Display board and prompt a move"""
    def __init__(self, player1="human", player2="human"):
        self.game = Game('human', 'human')
        self._player1_type = player1
        self._player2_type = player2
            
    def run(self):
        while True:
            print(self.game.board)
            # fetch current turn number
            curr_turn = self.game.get_turn()
            # if odd, white moves. if even, blue moves.
            if (curr_turn % 2) != 0:
                print("Turn: {}, white (AB)".format(curr_turn))
                self.white_turn()
            else:
                print("Turn: {}, blue (XY)".format(curr_turn))
                self.blue_turn()
            

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
        # check if player is human
        if self._player1_type == "human":
            # ask for piece selection
            while True:
                try:
                    worker_input = input("Select a worker to move\n")
                    if worker_input == "Z" or "Y":
                        raise OwnerError
                    elif worker_input != "A" or worker_input != "B":
                        raise ValueError
                    else:
                        # input is good. Player selected either A or B.
                        break
                except OwnerError:
                    print("That is not your worker")
                except ValueError:
                    print("Not a valid worker")
            # ask for desired move
            while True:
                try:
                    move = input("Select a direction to move (n, ne, e, se, s, sw, w, nw)\n")
                    break
                except ValueError:
                    print("Please try again with a valid date in the format YYYY-MM-DD.")

        
        
if __name__ == "__main__":
    SantoriniCLI().run()