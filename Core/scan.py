
# Fingerprint Detector #

import json
import requests
import os
from colorama import Fore

class Scanner():
    def __init__(
            self,session:requests.session = requests.session(),
            fingerprints_folder:str = os.path.join("Fingerprints")
        ):

        self.session : requests.Session = session
        self.fingerprints_folder:str = fingerprints_folder

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
        initial_reqest = self.session.get(url)
        
        for header in self.head_fingerprints:
            header : str

            split_header = header.split(":")

            if not initial_reqest.headers.get(split_header[0]):
                continue

            if split_header[1] in initial_reqest.headers.get(split_header[0]):
                print(f"The source is probably using {Fore.CYAN}'{self.head_fingerprints[header]}'{Fore.WHITE}"
                    + f" - based on {Fore.CYAN}'{split_header[0]}:{initial_reqest.headers.get(split_header[0])}'{Fore.WHITE} header."
                )

        for body_fingerprint in self.body_fingerprints:
            body_fingerprint: str

            if body_fingerprint in initial_reqest.content.decode():
                print(f"The source is probably using {Fore.CYAN}'{self.body_fingerprints[body_fingerprint]}'{Fore.WHITE},"+ 
                      f" - a fingerprint seemingly appears in the response body {Fore.CYAN}'{body_fingerprint}'{Fore.WHITE}")

            