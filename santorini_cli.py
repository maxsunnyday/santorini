from santorini_game import *

class SantoriniCLI:
    """Display board and display move prompt"""
    def __init__(self):
        self.board = Game()
        self.white_player = Player()
        self.black_player = Player()
            
    def display_menu(self):
        print("--------------------------------")
        self.current_account()
        print("""Enter command
1: open account
2: summary
3: select account
4: list transactions
5: add transaction
6: interest and fees
7: save
8: load
9: quit""")
    
    def run(self):
        """Display the starting options and respond to choices."""
        while True:
            self.display_menu()
            choice = input(">")
            action = self.choices.get(choice)
            if action:
                action()
            else:
                print("{0} is not a valid choice".format(choice))

    def print_account(self, account):
        balance = '${0:.2f}'.format(account.amount)
        print(f"Currently selected account: {account.type.capitalize()}#{str(account.id).zfill(9)},\tbalance: {balance}")


    def current_account(self):
        if not self.current:
            print("Currently selected account: None")
        else:
            self.print_account(self.current)


    def open_account(self):
        type = input("Type of account? (checking/savings)\n>")
        deposit = input("Initial deposit amount?\n>")

        if type == "checking":
            self.bank.new_account(deposit, type)
        elif type == "savings":
            self.bank.new_account(deposit, type)

                
    def summary(self):
        for account in self.bank.accounts:
            balance = '${0:.2f}'.format(account.amount)
            print(f"{account.type.capitalize()}#{str(account.id).zfill(9)},\tbalance: {balance}")
            
    def select_account(self):
        account_number = input("Enter account number\n>")
        account = self.bank.search_account(int(account_number))
        self.current = account
        

    def list_transactions(self):
        self.current.sort_transactions()
        for t in self.current.transactions:
            balance = '${0:.2f}'.format(t.amount)
            print(f"{t.date}, {balance}")
    
    def add_transaction(self):
        amount = input("Amount?\n>")
        date = input("Date? (YYYY-MM-DD)\n>")
        if self.current.type == "savings":
            self.current.add_transaction(amount, date, 1)
        elif self.current.type == "checking":
            self.current.add_transaction(amount, date, 2)
        
    def interest(self):
        for acc in self.bank.accounts:
            acc.add_interest()

    def save(self):
        self.bank.number_of_accounts = self.bank.account_number
        with open("saved_bank.pickle", "wb") as file: 
            pickle.dump(self.bank, file)

    def load(self):
        with open("saved_bank.pickle", "rb") as file: 
            self.bank = pickle.load(file)
            Bank.account_number += self.bank.number_of_accounts
    
    def quit(self):
        sys.exit(0)
        
if __name__ == "__main__":
    BankCLI().run()