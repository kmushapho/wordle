import subprocess
import sys
import os
import json
import pkg_resources
import requests
    

def check_and_install_pip():
    """Checks if pip is installed on the user's machine. 
    If not, it installs pip for the user."""

    try:
        # check if pip is installed
        subprocess.check_call([sys.executable, "-m", "pip", "--version"])
        # if pip already installed tell the user
        print("\033[32m\npip is already installed on this device.\033[0m")
    
    except subprocess.CalledProcessError:
        # tell user if pip not already installed
        print("\033[31m\nPip is not installed. Installing pip.....\033[0m")

        # first update sudo apt
        subprocess.check_call(["sudo", "apt", "update"])
        # install pip
        subprocess.check_call(["sudo", "apt", "install", "-y", "python3-pip"])
    
    except:
        # tell user to install pip manually
        print("\033[31m\nFailed to install pip using apt. Please install pip manually\033[0m")

        # exit the program
        sys.exit(1)


def install_packages():
    """Checks each package listed in requirements.txt to see if it's installed on the user's machine. 
    If any package is missing, it installs the required package."""

    try:
        with open("requirements.txt", "r") as file:
            packages = file.readlines()

        # remove any whitespaces from the packages
        packages = [i.strip() for i in packages]

        for package in packages:

            try:
                # check if package is already installed
                pkg_resources.get_distribution(package)
                print(f"\033[32m\n{package} is already installed on this device.\033[0m")

            except pkg_resources.DistributionNotFound:
                # if its not found, install it
                print(f"\033[31m\n{package} not found. Installing....\033[0m")



                try:
                    # run pip install using the subprocess modules to install all requiremets
                    subprocess.check_call([sys.executable, "pip", "install", "requiments.txt"])
                    print("\033[32m\nAll packages were installed successfully\033[0m")


                except subprocess.CalledProcessError:
                    print(f"\033[31m\nAn error occurred while installing the {package}. Please try installing it manually.\033[0m")

    except FileNotFoundError:
        print("\033[31mrequirements.txt not found\033[0m")


def get_game_words():
    print("\033[34m\nPlease wait while the game words are being downloaded.\033[0m")

    # set up datamuse url
    url = "https://random-word-api.herokuapp.com/word"

    filtered_words = []

    while len(filtered_words) < 10:
        response = requests.get(url)
        if response.status_code == 200:
            word = response.json()[0]
            filtered_words.append(word)
        
        else:
            print(f"\033[31mError fetching word. Status code: {response.status_code}\033[0m")
            break
    
    print("\033[32m\nWords download complete\033[0m")


    return filtered_words


def new_user():
    """Checks if the user is new. If so, creates a JSON file and installs the necessary game packages."""
    if not os.path.exists('config.json'):
        # install all the required packages
        check_and_install_pip()
        install_packages()

        # get the words that will be used in the game
        words_list = get_game_words()
        words_list = [word for word in words_list if 5 <= len(word) <= 12]

        # create a json file for new user
        with open('config.json', 'w') as file:
            json.dump({"words_list": words_list}, file)

    else:
        print("Welcome back!")


new_user()
