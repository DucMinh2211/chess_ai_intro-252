import chess
import math
import random
from model.evaluation import evaluate

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

    captures = [m for m in moves if board.is_capture(m)]
    if captures:
        return random.choice(captures)

    checks = []
    for m in moves:
        board.push(m)
        if board.is_check():
            checks.append(m)
        board.pop()

    if checks:
        return random.choice(checks)

    return random.choice(moves)


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
