from santorini_game import *

class SantoriniCLI:
    """Display board and prompt a move"""
    def __init__(self):
        self.game = Game('human', 'human')
            
    def run(self):
        while True:
            print(self.game.board)
            # fetch current turn number
            curr_turn = self.game.get_turn()
            # if odd, white moves. if even, blue moves.
            if (curr_turn % 2) != 0:
                print("Turn: {}, white (AB)".format(curr_turn))
                white_turn()
            else:
                print("Turn: {}, blue (AB)".format(curr_turn))
                blue_turn()
            

            while True:
                try:
                    move = input("Select a direction to move (n, ne, e, se, s, sw, w, nw)\n")
                    break
                except ValueError:
                    print("Please try again with a valid date in the format YYYY-MM-DD.")

            while True:
                try:
                    build = input("Select a direction to build (n, ne, e, se, s, sw, w, nw)\n")
                    break
                except ValueError:
                    print("Please try again with a valid date in the format YYYY-MM-DD.")

    def white_turn():
                while True:
                    try:
                        worker_input = input("Select a worker to move\n")
                        if worker_input not "A"
                        break
                    except ValueError:
                        print("Please try again with a valid date in the format YYYY-MM-DD.")
        
if __name__ == "__main__":
    SantoriniCLI().run()