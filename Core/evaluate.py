
import requests
import os
from colorama import Fore

class Evaluator():
    def __init__(
            self,
            headers:dict,
            body:str,
            session:requests.session = requests.session(),
            fingerprints_folder:str = os.path.join("Fingerprints"),
            timeout:int = 5
        ):

        self.session : requests.Session = session
        self.headers : dict = headers
        self.body : str = body
        self.fingerprints_folder:str = fingerprints_folder

        self.timeout = timeout

    def analyze(self,url:str,stack:list):
        # A litle skiddish but it will do the job
        if "Cloudflare" in stack:
            print(f"{Fore.LIGHTYELLOW_EX}Cloudflare is a WAF and may block attacks...{Fore.WHITE}")

        if "Flask" in stack:
            print(f"{Fore.GREEN}Flask detected, using standard version check...{Fore.WHITE}")
            if (self.headers.get("server") == None) or not ("Werkzeug" in self.headers.get("server")):
                print(f"{Fore.LIGHTYELLOW_EX}The server header is not correct...{Fore.WHITE}")
            else:
                server_header = self.headers.get("server").split(" ")

                for item in server_header:
                    print(f"The target is using {Fore.CYAN}{item.split("/")[0]}{Fore.WHITE}" + 
                          f" version {Fore.CYAN}{item.split("/")[1]}{Fore.WHITE}"
                        )

            

