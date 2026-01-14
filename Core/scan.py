
# Fingerprint Detector #

import json
import requests
import os
from colorama import Fore

class Scanner():
    def __init__(
            self,session:requests.session = requests.session(),
            fingerprints_folder:str = os.path.join("Fingerprints"),
            timeout:int = 5
        ):

        self.session : requests.Session = session
        self.fingerprints_folder:str = fingerprints_folder

        self.timeout = timeout

        main_file = open(
            os.path.join(
                self.fingerprints_folder,
                "fingerprints.json"
            )
        )

        # The fingerprint file is split into two sections.
        # - Head:
        #   - Fingerprints that appear in request headers.
        # - Body
        #   - Fingerprints that appear in request body.

        self.fingerprints = json.load(main_file)

        self.head_fingerprints = self.fingerprints["head"]
        self.body_fingerprints = self.fingerprints["body"]

    def scan(self,url):

        try:
            initial_reqest = self.session.get(
                url,
                timeout=self.timeout
            )
        except requests.exceptions.ConnectTimeout:
            print(f"{Fore.RED}Connection timed out.{Fore.WHITE}")
            return
        except Exception as error:
            print(f"{Fore.RED}Error occured, cannon connect to host:{str(error)}{Fore.WHITE}")
            return
        
        # Print out indicative headers that may appear
        indicative_headers = ["server","X-Powered-By"]

        for header in indicative_headers:
            if initial_reqest.headers.get(header) is None:
                continue

            print(
                f"The source contains the indicative header {Fore.CYAN}{header}{Fore.WHITE} that may often show a product.\n" +
                f"The indicative header {Fore.CYAN}{header}{Fore.WHITE} is {Fore.CYAN}{header}:{initial_reqest.headers.get(header)}{Fore.WHITE}\n" +
                f"{Fore.YELLOW}However those headers have the possibility to be modified to cover internal services{Fore.WHITE}\n"
            )


        
        # Go for each fingerprint in the fingerprints file to see if it appears.
        
        for header in self.head_fingerprints:
            header : str

            split_header = header.split(":")

            if not initial_reqest.headers.get(split_header[0]):
                continue

            if split_header[1].capitalize() in initial_reqest.headers.get(split_header[0]).capitalize():
                print(f"The source is probably using {Fore.CYAN}'{self.head_fingerprints[header]}'{Fore.WHITE}"
                    + f" - based on {Fore.CYAN}'{split_header[0]}:{initial_reqest.headers.get(split_header[0])}'{Fore.WHITE} header."
                )

        for body_fingerprint in self.body_fingerprints:
            body_fingerprint: str

            if body_fingerprint.capitalize() in initial_reqest.content.decode().capitalize():
                print(f"The source is probably using {Fore.CYAN}'{self.body_fingerprints[body_fingerprint]}'{Fore.WHITE},"+ 
                      f" - a fingerprint seemingly appears in the response body {Fore.CYAN}'{body_fingerprint}'{Fore.WHITE}")

            