import subprocess
import sys
import os
import json
import pkg_resources
from spellchecker import SpellChecker
import time
import random
    

def check_and_install_pip():
    """Checks if pip is installed on the user's machine. 
    If not, it installs pip for the user."""

    try:
        subprocess.check_call([sys.executable, "-m", "pip", "--version"])
        print("\033[32m\npip is already installed on this device.\033[0m")
    
    except subprocess.CalledProcessError:
        print("\033[31m\nPip is not installed. Installing pip.....\033[0m")

        subprocess.check_call(["sudo", "apt", "update"])
        subprocess.check_call(["sudo", "apt", "install", "-y", "python3-pip"])
    
    except:
        print("\033[31m\nFailed to install pip using apt. Please install pip manually\033[0m")

        sys.exit(1)


def install_packages():
    """Checks each package listed in requirements.txt to see if it's installed on the user's machine. 
    If any package is missing, it installs the required package."""

    try:
        with open("requirements.txt", "r") as file:
            packages = file.readlines()

        packages = [i.strip() for i in packages]

        for package in packages:

            try:
                pkg_resources.get_distribution(package)
                print(f"\033[32m\n{package} is already installed on this device.\033[0m")

            except pkg_resources.DistributionNotFound:
                print(f"\033[31m\n{package} not found. Installing....\033[0m")



                try:
                    subprocess.check_call([sys.executable, "pip", "install", package])
                    print("\033[32m\nAll packages were installed successfully\033[0m")


                except subprocess.CalledProcessError:
                    print(f"\033[31m\nAn error occurred while installing the {package}. Please try installing it manually.\033[0m")

    except FileNotFoundError:
        print("\033[31mrequirements.txt not found\033[0m")


def get_game_words():
    print("\033[34m\nPlease wait while the game words are being downloaded.\033[0m")

    all_words = list(SpellChecker())

    filtered_words = []
    word_len = 5
    count = 0

    while len(filtered_words) < 120:
        word = random.choice(all_words)
        if all(char.isalpha() for char in word):
            if len(word) == word_len:
                filtered_words.append(word)
                count += 1
            
            if count == 20:
                count = 0
                word_len += 1
        

    time.sleep(5)
    print("\033[32m\nWords download complete\033[0m")


    return filtered_words


def new_user():
    """Checks if the user is new. If so, creates a JSON file and installs the necessary game packages."""
    if not os.path.exists('config.json'):
        check_and_install_pip()
        install_packages()

        words_list = get_game_words()
        words_list = [word for word in words_list if 5 <= len(word) <= 12]

        with open('config.json', 'w') as file:
            json.dump({"words_list": words_list, "game_level" : 1}, file)

    else:
        print("Welcome back!")


new_user()
