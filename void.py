from colorama import Fore
import sys

from Core import scan

def help():
    print("Usage:")
    print(f"python void.py {Fore.LIGHTBLACK_EX}<url>{Fore.WHITE}")

def main():
    if len(sys.argv) < 2:
        help()
        return
    
    if sys.argv[1] == "help":
        help()
        return
    
    print("Running initial scan on given url...")
    Scanner = scan.Scanner()
    Scanner.scan(sys.argv[1])


if __name__ == "__main__":
    main()