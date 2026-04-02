import math
import chess
import random
from model.evaluation import evaluate, evaluate_move

# ===================== MCTS =====================

C = 1.4

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

    exploit = math.tanh(node.value / (node.visits * 1000))

    explore = C * math.sqrt(math.log(node.parent.visits + 1) / node.visits)
    return exploit + explore


def select(node):
    while node.children:
        unvisited = [c for c in node.children if c.visits == 0]
        if unvisited:
            return random.choice(unvisited)
        node = max(node.children, key=uct)
    return node


def expand(node):
    if node.children:
        return node  
    
    moves = list(node.board.legal_moves)
    if not moves:
        return node
    
    for move in moves:
        b = node.board.copy()
        b.push(move)
        node.children.append(Node(b, node))
    
    return random.choice(node.children)

def random_move(board):
    moves = list(board.legal_moves)
    if not moves: return None
    rmove = random.choice(moves)
    return rmove


def simulate(board, rollout_depth: int):
    mover = not board.turn

    depth = 0
    while not board.is_game_over() and depth < rollout_depth:
        move = random_move(board)
        if move is None:
            break
        board.push(move)
        depth += 1

    raw = evaluate(board)  # White-positive
    raw = max(-2000, min(2000, raw))
    return raw if mover == chess.WHITE else -raw


def backpropagate(node, result):
    while node:
        node.visits += 1
        node.value += result
        result = - result
        node = node.parent


def mcts(board, iterations=10000, rollout_depth=30):
    root = Node(board)

    print(f"MCTS starting: {iterations} iterations, rollout depth {rollout_depth}")

    for i in range(iterations):
        if i % 1000 == 0 and i > 0:
            print(f"  Iteration {i}/{iterations}...")

        node = select(root)
        node = expand(node)
        result = simulate(node.board.copy(), rollout_depth)
        backpropagate(node, result)

    if not root.children:
        print("MCTS: No legal moves found!")
        return None

    sorted_children = sorted(root.children, key=lambda n: n.visits, reverse=True)

    print("\nMCTS Results:")
    for child in sorted_children[:5]:
        move = child.board.peek()
        avg_val = child.value / child.visits if child.visits > 0 else 0
        print(f"  Move {move}: {child.visits} visits, avg value: {avg_val:.2f}")

    best = max(root.children, key=lambda n: n.value / n.visits if n.visits > 0 else float('-inf'))
    print(f"\nBest move: {best.board.peek()} with {best.visits} visits\n")
    return best.board.peek()
