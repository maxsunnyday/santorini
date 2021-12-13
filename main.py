from santorini_cli import *

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