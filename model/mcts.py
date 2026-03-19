import math
import random
import time
import chess

class MCTSNode:
    def __init__(self, board, parent=None, move=None):
        self.board = board
        self.parent = parent
        self.move = move
        self.children = []
        self.wins = 0
        self.visits = 0
        self.untried_moves = list(board.legal_moves)

    def select_child(self):
        # * UCB1 formula
        return max(self.children, key=lambda c: c.wins / c.visits + math.sqrt(2 * math.log(self.visits) / c.visits))

    def expand(self):
        move = self.untried_moves.pop()
        next_board = self.board.copy()
        next_board.push(move)
        child_node = MCTSNode(next_board, parent=self, move=move)
        self.children.append(child_node)
        return child_node

    def update(self, result):
        self.visits += 1
        self.wins += result

def mcts_search(board, iterations=1000):
    root = MCTSNode(board.copy())

    for _ in range(iterations):
        node = root
        
        # * 1. Selection
        while not node.untried_moves and node.children:
            node = node.select_child()

        # * 2. Expansion
        if node.untried_moves:
            node = node.expand()

        # * 3. Simulation (Rollout)
        temp_board = node.board.copy()
        while not temp_board.is_game_over():
            moves = list(temp_board.legal_moves)
            temp_board.push(random.choice(moves))
        
        # * Determine result (1 for win, 0.5 for draw, 0 for loss)
        result = temp_board.result()
        if result == '1-0':
            score = 1 if board.turn == chess.WHITE else 0
        elif result == '0-1':
            score = 1 if board.turn == chess.BLACK else 0
        else:
            score = 0.5

        # * 4. Backpropagation
        while node is not None:
            # * Score depends on whose turn it was to move to reach this node
            # * In MCTS, we usually reward the move if it leads to a win for the current player
            node.update(score if node.board.turn != board.turn else 1 - score)
            node = node.parent

    # * Select the move with the most visits
    return max(root.children, key=lambda c: c.visits).move
