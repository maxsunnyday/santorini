from santorini_game import *

class SantoriniCLI:
    """Display board and prompt a move"""
    def __init__(self):
        self.game = Game()
        self.white_player = Player()
        self.black_player = Player()
            
    def run(self):
            while True:
                try:
                    amount = input("Amount?\n>")
                    break
                except InvalidOperation:
                    print("Please try again with a valid dollar amount.")

            while True:
                try:
                    date = input("Date? (YYYY-MM-DD)\n>")
                    date = datetime.strptime(date, "%Y-%m-%d").date()
                    break
                except ValueError:
                    print("Please try again with a valid date in the format YYYY-MM-DD.")

            while True:
                try:
                    date = input("Date? (YYYY-MM-DD)\n>")
                    date = datetime.strptime(date, "%Y-%m-%d").date()
                    break
                except ValueError:
                    print("Please try again with a valid date in the format YYYY-MM-DD.")
        
if __name__ == "__main__":
    SantoriniCLI().run()