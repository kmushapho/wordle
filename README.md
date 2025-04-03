# wordle

Welcome to Wordle Unlimited Dupe, a Python-based game inspired by the popular Wordle game but with unlimited play! This project allows you to play a variety of Wordle modes, including random mode, levels, and specific word lengths. The game is built using Python, with external dependencies for spellchecking and rendering the game interface using Pygame.

Features
Random Mode: Play with randomly selected words.

Levels Mode: Play through levels with increasing difficulty.

Custom Word Length: Choose the length of the word to guess (between 5 and 10 characters).

Spellchecking: Built-in spellcheck for valid words.

Pygame Interface: A simple yet fun interface for playing the game.

Requirements
Before you can run the game, you'll need Python installed on your computer. The game also uses two external packages:

Pygame: For the graphical user interface.

Spellcheck: To verify valid words.

When you first run the game, it will automatically install these dependencies if they are not already installed.

Installation & Setup
Step 1: Clone the repository
First, clone the repository to your local machine:
git clone https://github.com/kmushapho/wordle.git

Cd to the directory:
cd wordle

Step 2: Run the game
Execute the wordle.py script to start the game:

python wordle.py
The first time you run the game, it will automatically install any required packages using pip (if they are not already installed). This includes:

spellcheck

pygame

Additionally, it will create a JSON file that stores game words and saved game level.

Step 3: Playing the Game
Once the game is running, you can choose from several play modes:

Random Mode: The game selects a random word for you to guess.

Levels Mode: Increase the difficulty as you progress through levels.

Specific Word Length: Choose the length of the word, ranging from 5 to 10 characters.

Step 4: JSON File
When the game runs for the first time, a JSON file will be created in the directory to store game data and settings. This file will be used to store your progress and preferences.

How to Play
Type your guess into the input field.

The game will highlight correct letters and show feedback on your guess.

Keep guessing until you find the correct word!

Dependencies
To ensure the game runs smoothly, you will need to have the following Python packages installed:

bash
Copy
pip install spellcheck pygame
If running wordle.py for the first time, the script will handle this installation automatically.

Contributing
Feel free to open issues, submit pull requests, or suggest new features. This project is open for collaboration, and contributions are welcome!
