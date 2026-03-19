# Chess AI Intro

A modern Chess game implementation in Python featuring multiple AI algorithms, including **Alpha-Beta Pruning** and **Monte Carlo Tree Search (MCTS)**. This project uses the `eel` library for a web-based GUI and `python-chess` for game logic.

## 🚀 Features

- **Multiple AI Opponents**:
  - **Alpha-Beta Bot**: Uses Minimax with Alpha-Beta pruning and Piece-Square Tables (PST) for evaluation.
  - **MCTS Bot**: Implements Monte Carlo Tree Search with UCB1 for selection.
  - **Random Bot**: A baseline bot that makes random legal moves.
- **Modern Web GUI**: Interactive board built with HTML, CSS, and JavaScript, powered by `eel`.
- **Legal Move Visualization**: Highlights valid moves for the selected piece.
- **Game Status Detection**: Automatically detects checkmate, stalemate, and various draw conditions.
- **Customizable AI Depth**: Adjust the search depth for Alpha-Beta or iterations for MCTS.

## 🛠️ Tech Stack

- **Backend**: Python 3.x
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Libraries**:
  - [python-chess](https://github.com/niklasf/python-chess): For move generation and game state management.
  - [Eel](https://github.com/python-eel/Eel): For hosting a local web-based UI.

## 📦 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/chess-ai-intro-252.git
   cd chess-ai-intro-252
   ```

2. **Install dependencies**:
   It is recommended to use a virtual environment.
   ```bash
   pip install -r requirements.txt
   ```

## 🎮 How to Run

Launch the application by running the `main.py` script:

```bash
python main.py
```

This will open a window with the Chess UI. Select your opponent type and start playing!

## 🧠 Algorithm Details

### 1. Alpha-Beta Pruning
An optimized version of the Minimax algorithm that reduces the number of nodes evaluated by "pruning" branches that cannot influence the final decision.
- **Heuristic Evaluation**: Combines material value (Pawn=100, Knight=320, etc.) with **Piece-Square Tables (PST)** to reward better positioning (e.g., Knights in the center).
- **Endgame Transition**: Adjusts King evaluation strategy during the endgame.

### 2. Monte Carlo Tree Search (MCTS)
A probabilistic search algorithm that builds a search tree through random simulations.
- **Selection**: Uses the **UCB1** (Upper Confidence Bound) formula to balance exploration vs. exploitation.
- **Expansion**: Adds new nodes to the tree.
- **Simulation (Rollout)**: Plays a random game from the current state to the end.
- **Backpropagation**: Updates the win rates and visit counts of parent nodes.

## 📂 Project Structure

```text
├── main.py              # Entry point & Eel bridge
├── model/               # AI Algorithm implementations
│   ├── alpha_beta.py    # Alpha-Beta Pruning & Heuristics
│   └── mcts.py          # Monte Carlo Tree Search
├── UI/                  # Frontend assets
│   ├── index.html       # UI Layout
│   ├── style.css        # Styling
│   ├── app.js           # Game logic & Eel calls
│   └── assets/          # Images and icons
├── doc.md               # Technical documentation (Vietnamese)
└── requirements.txt     # Python dependencies
```

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
*Developed as part of a Chess AI introductory project.*
