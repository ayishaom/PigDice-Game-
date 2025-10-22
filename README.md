# PigDice Game

This project is an object-oriented Python application that implements a terminal-based game called **PigDice Game**. The goal of the project is to practice object-oriented programming, create a proper Python development environment and apply unit testing and automated documentation tools, including UML diagram generation.

The game allows one or two players to play against the computer. Players can select or change their names, view the rules and play full rounds of the game. A persistent high-score list tracks player statistics across sessions. The computer has configurable intelligence settings to provide a challenging opponent. The game also includes a cheat mode for testing purposes.

This project is developed as part of an assignment to practice clean, modular, and testable code in Python. It emphasizes:

- Object-oriented programming with classes like `Game`, `Dice`, `DiceHand`, `Histogram`, `Intelligence`, `HighScore`, `Player`, `Menu`, and `Main`.
- Comprehensive unit testing with one test file per class, aiming for over 90% code coverage.
- Automated UML diagram generation to document the application structure.
- Proper Python development practices, including virtual environments, dependency management and code style using linters (`pylint` and `flake8`).

The project also includes detailed instructions for installing dependencies, running the game, running tests and generating documentation, all of which are described below in this README.

---

## Table of Contents
- [Features](#features)
- [Game Rules](#game-rules)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Run the Game](#run-the-game)
- [Testing and Coverage](#testing-and-coverage)
- [Code Quality](#code-quality)
- [Auto-Generated Documentation](#auto-generated-documentation)
- [UML Diagrams](#uml-diagrams)
- [High Scores and Data](#high-scores-and-data)
- [Team Members](#team-members)
- [License](#license)

---

## Features
- Player vs Computer (AI) and Player vs Player modes
- Adjustable AI difficulty levels (easy, medium, hard)
- Persistent high-score tracking stored in `scores.json`
- Cheat option (+50 points) for testing
- Input validation and error handling
- Readable terminal interface with simple menus
- Unit-tested codebase with 90%+ coverage

---

## Game Rules
- Each player rolls one die per turn.
- Rolling a 1 ends the turn with 0 points for that round.
- Rolling 2–6 adds to the player’s turn total.
- Players can choose to “hold” to save their turn points.
- The first to reach 100 points wins.
- Cheat mode adds +50 points instantly for testing purposes.

---

## Project Structure
```
project-root/
├─ src/
│  ├─ __init__.py       # Makes src a package
│  ├─ dice.py           # Dice logic (roll, sides)
│  ├─ diceHand.py       # Manages multiple dice
│  ├─ player.py         # Player info and scores
│  ├─ score.py          # Persistent score storage
│  ├─ intelligence.py   # AI logic for computer opponent
│  ├─ game.py           # Game loop and logic
│  ├─ menu.py           # Menu display and input handling
│  ├─ histogram.py      # Score histogram display
│  ├─ main.py           # Program entry point
│  └─ scores.json       # Persistent data
├─ tests/               # One test file per class
├─ doc/api/             # Auto-generated documentation
├─ doc/uml/             # UML diagrams
├─ requirements.txt
├─ README.md
└─ LICENSE.md
```

---

## Installation

Before starting, make sure you have Git and **Python 3.11 or higher** installed on your computer.

You can use Git Bash terminal.

Follow these steps to set up the project on your system:

### 1. Clone the repository from GitHub
Open your terminal, navigate to the folder where you want to install the project and run:
```bash
git clone https://github.com/<your-username>/<your-repository-name>.git
```

Then move into the project folder:
```bash
cd <your-repository-name>
```

### 2. Create and activate a virtual environment
Create a virtual environment to keep project dependencies separate:
```bash
python -m venv .venv
```

Activate the environment:
```bash
source .venv/Scripts/activate
```

### 3. Install dependencies
Install all project dependencies using the provided `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 4. Verify installation
Check that everything is installed correctly:
```bash
python --version
pytest --version
pylint --version
```

You should see version numbers confirming successful installation.

---

## Run the Game
After installation, start the game using:
```bash
python src/main.py
```

### Main Menu Options
1. Play against computer  
2. Play two-player game  
3. View high scores  
4. View rules  
5. Quit

---

## Testing and Coverage
This project uses **pytest** for unit testing.

### 1. Installation
Install pytest and coverage tools:
```bash
pip install pytest pytest-cov coverage
```

### 2. Running Tests
To run all tests:
```bash
pytest -q
```

For detailed output:
```bash
pytest -vv
```

### Checking Test Coverage
Generate a coverage report (shows missing lines and HTML report):
```bash
pytest --cov=src --cov-report=term-missing --cov-report=html
```

Open the file `htmlcov/index.html` in a browser to view the coverage report.

Our goal was to achieve over 90% test coverage.  
Each class has its own test file and at least 10 test cases with 20+ assertions, as required by the assignment.

---

## Code Quality
This project uses **Flake8**, **Pylint**, and **Black** to ensure that the code follows Python’s style and quality guidelines.  
These tools help identify and correct issues such as unused imports, inconsistent naming, missing docstrings and code formatting problems.

### 1. Installation
To install the linters, run the following commands in your terminal (inside your virtual environment):
```bash
pip install flake8 flake8-docstrings flake8-polyfill pylint black
```

### 2. Running Flake8
Flake8 checks for general code style issues and docstring formatting.
```bash
flake8 src tests
```

### 3. Running Pylint
Pylint performs a deeper analysis of code quality.
```bash
pylint src
```

We used the Pylint output to improve our code readability and structure, aiming for a score above 8.0/10 for each module.

### 4. Formatting Code with Black
Black automatically formats Python code according to the PEP 8 style guide.

Run Black:
```bash
black src tests
```

(Optional) You can check the formatting without changing files:
```bash
black --check src tests
```

If everything’s good, it will show:
```
All done! ✨ 🍰 ✨
```

These commands ensure a unified project style before linting.

---

## Auto-Generated Documentation
1. To install pdoc:
```bash
pip install pdoc
```

2. Open a terminal and go to the root folder of the project:
```bash
cd /path/to/project
```

3. Set Python path to ensure that Python can find source modules:
```bash
export PYTHONPATH="$(realpath src)"
```

4. (Optional) Clean old documentation:
```bash
rm -rf doc/api
```

5. To automatically generate HTML documentation for all modules:
```bash
pdoc --output-dir doc/api $(find src -name "*.py" -exec basename {} .py \;)
```

6. To view documentation in a web browser:
```
explorer.exe "$(cygpath -w doc/api/index.html)"
```

---

## UML Diagrams
This project includes UML diagrams generated from the Python code.  
They are stored in the `doc/uml` directory.

### Included Diagrams
- Class Diagram: Shows classes, attributes, methods, and relationships.
- Package Diagram: Shows package structure and dependencies.

### Regenerating UML Diagrams
To regenerate UML diagrams from the Python code, follow these steps:

> **Note:** Make sure **Graphviz** is installed and added to your system PATH.  
> If you haven’t installed it yet, **see step 3 below** for detailed installation instructions.  
> Without Graphviz, `pyreverse` will not be able to generate the UML diagram images.


1. Activate the virtual environment:
```bash
source .venv/Scripts/activate
```

2. Install required packages (if not installed):
```bash
pip install pylint graphviz
```

3. #### Install the Graphviz system tool (Windows)
   i. Download the **Graphviz installer** from the official website:  
      👉 [https://graphviz.org/download/](https://graphviz.org/download/)

   ii. Run the installer and make sure to **check** the box:  
      > “Add Graphviz to the system PATH for current user”
   
   iii. After installation, **close and reopen your terminal** so the PATH updates.
   
   iv. Verify that Graphviz was installed correctly:
      ```bash
      dot -V
      ```
      You should see something like this:
      ```
      dot - graphviz version 14.0.2 (2024-…)
   ```
4. Generate UML diagrams:
```bash
pyreverse -o png -p PigDiceGame src/
```

5. Move the diagrams to the documentation folder:
```bash
mv classes_PigDiceGame.png packages_PigDiceGame.png doc/uml/
```

After completing these steps, the `doc/uml` directory will contain your updated class and package diagrams.

---

## High Scores and Data
High scores and player statistics are stored in `src/scores.json` using the following structure:
```json
{
  "PlayerName": {
    "games": [
      { "date": "YYYY-MM-DD", "points": 120 }
    ],
    "total_points": 120
  }
}
```

When a player is renamed, their history is preserved by merging records under the new name.

---

## Team Members

- **Anastasia Klimson**  
  GitHub: [https://github.com/aklimson](https://github.com/aklimson)

- **Ayisha Omer**  
  GitHub: [https://github.com/ayishaom](https://github.com/ayishaom)

- **Lungowe Akushanga**  
  GitHub: [https://github.com/LungoweA](https://github.com/LungoweA)

---

## License
This project is licensed under the MIT License.  
See `LICENSE.md` for details.
