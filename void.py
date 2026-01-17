from colorama import Fore
import sys

from Core import scan
from Core import evaluate

def help():
    print("Usage:")
    print(f"python void.py {Fore.LIGHTBLACK_EX}<url>{Fore.WHITE}")
    print("--timeout <int> -> Set the number of seconds the software will wait for a response (defualt is 5)")

def main():
    if len(sys.argv) < 2:
        help()
        return
    
    if sys.argv[1] == "help":
        help()
        return
    
    url = sys.argv[1]
    
    Scanner = scan.Scanner()
    
    if "--timeout" in sys.argv:
        Scanner.timeout = int(
        sys.argv[
            sys.argv.index("--timeout") + 1
        ]
    )
    
    print("Running initial scan on given url...")

    inital_scan = Scanner.scan(url)

    stack = inital_scan[0]

    print("Evaluating the response with another request...")
    Evaluator = evaluate.Evaluator(
        inital_scan[1],
        inital_scan[2],
        session=Scanner.session
    )

    Evaluator.analyze(
        url,
        stack
    )


if __name__ == "__main__":
    main()