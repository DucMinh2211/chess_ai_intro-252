import chess
import math
import random
from model.evaluation import evaluate, evaluate_move

# ===================== MCTS =====================

C = 1.4
ROLLOUT_DEPTH = 100

class Node:
    def __init__(self, board, parent=None):
        self.board = board
        self.parent = parent
        self.children = []
        self.visits = 0
        self.value = 0


def uct(node):
    if node.visits == 0:
        return float('inf')

    exploit = node.value / node.visits
    explore = C * math.sqrt(math.log(node.parent.visits) / node.visits)

    heuristic = evaluate(node.board) * 0.01

    return exploit + explore + heuristic


def select(node):
    while node.children:
        node = max(node.children, key=uct)
    return node


def expand(node):
    moves = list(node.board.legal_moves)
    for move in moves:
        b = node.board.copy()
        b.push(move)
        node.children.append(Node(b, node))
    return random.choice(node.children) if node.children else node


def heuristic_move(board):
    moves = list(board.legal_moves)
    if not moves: return None

    # Pick the best move according to evaluate_move (captures/promotions)
    best_move = max(moves, key=lambda m: evaluate_move(board, m))
    
    # If the best move is not a capture/promotion, pick randomly to maintain some exploration
    if evaluate_move(board, best_move) == 0:
        return random.choice(moves)
        
    return best_move


def simulate(board):
    depth = 0

    while not board.is_game_over():
        if depth >= ROLLOUT_DEPTH:
            return evaluate(board)

        move = heuristic_move(board)
        board.push(move)
        depth += 1

    if board.is_checkmate():
        return -99999 if board.turn else 99999

    return 0


def backpropagate(node, result):
    while node:
        node.visits += 1
        node.value += result
        node = node.parent


def mcts(board, iterations=1000):
    root = Node(board)

    for _ in range(iterations):
        node = select(root)
        node = expand(node)
        result = simulate(node.board.copy())
        backpropagate(node, result)

    if not root.children:
        return None

    best = max(root.children, key=lambda n: n.visits)
    return best.board.peek()
