# CENG 3511 Artificial Intelligence Midterm Project: Connect Four AI

![Python Version](https://img.shields.io/badge/python-3.x-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

This repository contains the source code for a Connect Four game with an integrated Artificial Intelligence opponent, submitted for the CENG 3511 AI course. The AI agent uses the **Minimax algorithm** optimized with **Alpha-Beta Pruning** to play strategically against a human player.

## 1. Project Overview

The primary goal of this project was to design and implement an AI agent capable of playing a turn-based, two-player, zero-sum game. Connect Four was chosen as the game environment due to its clear rules and defined strategic depth, making it a perfect candidate for classic search algorithms.

This project fulfills **Option 3: AI Opponent for a Turn-Based Game** from the project guidelines. The AI acts as the second player (Player 2), analyzing the game state and making optimal decisions to win, or at worst, draw the game.

## 2. Features

* **Standard 6x7 Game Board:** Implements the classic 6-row, 7-column Connect Four grid.
* **Two-Player Gameplay:** Allows a human player (Player 1) to compete against an AI (Player 2).
* **Intelligent AI Opponent:** The AI uses the Minimax algorithm to find the best possible move.
* **Optimized Performance:** **Alpha-Beta Pruning** is implemented to significantly reduce the search space, allowing the AI to look several moves ahead without significant computational delay.
* **Strategic Heuristic Evaluation:** The AI uses a robust `score_position` function to evaluate non-terminal game states, prioritizing wins, blocks, and strategic board control.

## 3. Technologies Used

* **Python 3:** The core programming language used for all game logic and AI implementation.
* **NumPy:** Used for efficient creation, manipulation, and copying of the 6x7 game board (as a 2D array). This is significantly more performant than using nested Python lists for board copies.
* **Math:** Used for `math.inf` (infinity) to initialize the `alpha` and `beta` variables in the Minimax algorithm.
* **Random:** Used to `random.choice` from a list of valid moves if multiple moves result in the same (best) heuristic score. This adds variability to the AI's gameplay.

## 4. Setup and Installation

To run this project on your local machine, follow these steps.

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git)
    cd YOUR_REPOSITORY
    ```

2.  **Install Dependencies:**
    The project relies only on `numpy`. You can install it using pip:
    ```bash
    pip install numpy
    ```

3.  **Run the Game:**
    Execute the Python script from your terminal:
    ```bash
    python connect_four_ai.py
    ```
    *(Note: Replace `connect_four_ai.py` with the actual name of your Python file.)*

## 5. How to Play

1.  Run the script as instructed above. The empty 6x7 game board will be printed to the console.
2.  The game follows standard Connect Four rules. You are **Player 1** (represented by `1`). The AI is **Player 2** (represented by `2`).
3.  When prompted (`Oyuncu, 0-6 arasında bir sütun seçin:`), enter the column number (0 through 6) where you want to drop your piece.
4.  The board will update and display your move.
5.  The AI will then calculate its best move and place its piece on the board. The console will announce the AI's chosen column.
6.  The game continues until one player achieves four pieces in a row (horizontally, vertically, or diagonally) or the board is full (a draw).
7.  A message will announce the winner (e.g., "🎉 Oyuncu kazandı!" or "🤖 AI kazandı!").

## 6. AI Design and Logic

The AI's decision-making process is built on the Minimax algorithm, a classic AI search algorithm for two-player games.

### 6.1. Minimax Algorithm
The core is a recursive, depth-first search (DFS) algorithm. It simulates all possible game outcomes up to a certain **depth** (number of moves).
* **Maximizing Player (AI):** Aims to find the move that leads to the highest possible score, assuming the opponent plays optimally.
* **Minimizing Player (Human):** Aims to find the move that leads to the lowest possible score for the AI.

### 6.2. Alpha-Beta Pruning Optimization
A standard Minimax algorithm for Connect Four is computationally infeasible as it would explore too many game states. **Alpha-Beta Pruning** is an optimization that "prunes" (cuts off) branches of the game tree that don't need to be searched. It stops evaluating a move as soon as it finds a move that is provably worse than a move it has already examined. This allows the AI to search deeper into the game tree (e.g., `depth=4`) in the same amount of time.

### 6.3. Terminal Node and Depth Evaluation
The recursion stops under two conditions:

1.  **Terminal Node:** The game is over (a player has won or the board is full).
    * **AI Win:** Returns a massive positive score (`1000000000000`).
    * **Player Win:** Returns a massive negative score (`-1000000000000`).
    * **Draw:** Returns a score of `0`.

2.  **Depth Limit Reached:** The algorithm has searched `depth` moves into the future. At this point, it cannot determine a definite win/loss, so it must **evaluate the "goodness"** of the current board using a heuristic function.

### 6.4. Heuristic Evaluation (`score_position`)
This function is the "brain" of the AI. It assigns a numerical score to any non-terminal board state. It does this by:

1.  **Prioritizing the Center Column:** A piece in the center column (`column_count // 2`) has more potential winning lines. The AI gets a small bonus (`+3`) for each of its pieces in this column.
2.  **Window-Based Scoring (`evaluate_window`):** The function scans the entire board (horizontally, vertically, and both diagonals) using a 4-piece "window." It scores each window:
    * **Offensive Scoring:**
        * `+100` for 4-in-a-row (A guaranteed win, this is the highest heuristic score).
        * `+5` for 3-in-a-row with an empty slot (A strong threat).
        * `+2` for 2-in-a-row with two empty slots.
    * **Defensive Scoring:**
        * `-4` for 3-in-a-row *for the opponent* with an empty slot. This score is negative, meaning the AI sees this as a "bad" board state and will be highly motivated to block it.

The AI sums all these scores to get a single value representing how good the current board is.

## 7. Testing and Performance

Since this is an algorithmic AI (not ML/RL), it does not require "training." Its performance is deterministic based on its algorithm and heuristic.

* **Test Method:** Testing was conducted via "actual gameplay" simulations (playing against the AI) to evaluate its behavior.
* **Observed Behavior:**
    * **Defense:** The AI successfully identifies and blocks the human player's 3-in-a-row threats.
    * **Offense:** The AI actively creates its own 3-in-a-row and 2-in-a-row threats.
* **Depth Analysis:** The search depth is set to `depth=4`. This was found to be the "sweet spot":
    * It's deep enough for the AI to see immediate threats and simple 2-move-ahead traps.
    * It's shallow enough to return a move almost instantly, providing a good user experience.
    * A higher depth (e.g., 6 or 8) would make the AI much stronger but would also significantly increase the computation time for each move.

## 8. Project Challenges and Future Work

* **Heuristic Tuning:** The most significant challenge was balancing the heuristic scores in the `evaluate_window` function. Determining the right values (e.g., `+5` for a 3-piece threat vs. `-4` for blocking an opponent's 3-piece threat) was a process of trial and error to make the AI play in a "smart" and balanced way.
* **Performance vs. Depth:** Finding the right `depth` was a key trade-off between AI intelligence and game performance. `depth=4` was chosen for this project, but `depth=5` is also viable, albeit slightly slower.
* **Debugging Recursion:** Debugging the Minimax algorithm was complex. It required careful state tracking and printing board states at different recursion levels to identify bugs in the logic.

**Future Work:**
* **Pygame UI:** The current game is console-based. [cite_start]A future improvement would be to integrate this logic with `Pygame` [cite: 21, 27] for a full graphical user interface.
* **Variable Depth:** The AI could be improved by using an iterative deepening approach or a variable depth search that searches deeper in critical (win/loss) situations.
