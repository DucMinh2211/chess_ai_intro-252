import math
import chess
import random
from model.evaluation_mcts import evaluate, evaluate_move

C     = 1.4
POWER = 3


class Node:
    def __init__(self, board, parent=None):
        self.board        = board
        self.parent       = parent
        self.children     = []
        self.visits       = 0
        self.value        = 0
        self.min_result   = 1.0
        self.proven_value = None


def uct(node: Node) -> float:
    if node.proven_value == float('inf'):
        return float('inf')
    if node.proven_value == float('-inf'):
        return float('-inf')

    if node.visits == 0:
        return float('inf')

    avg       = node.value / node.visits
    power_avg = math.copysign(abs(avg) ** (1.0 / POWER), avg)
    q_value   = 0.5 * (node.min_result + power_avg)

    explore = C * math.sqrt(math.log(node.parent.visits + 1) / node.visits)
    return q_value + explore


def select(node: Node) -> Node:
    while node.children:
        available = [c for c in node.children if c.proven_value != float('-inf')]
        if not available:
            return node

        unvisited = [c for c in available if c.visits == 0]
        if unvisited:
            return random.choice(unvisited)

        node = max(available, key=uct)
    return node


def expand(node: Node) -> Node:
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


def greedy_move(board: chess.Board, top_k: int = 5, epsilon: float = 0.2):
    moves = list(board.legal_moves)
    if not moves:
        return None
    if random.random() < epsilon:
        return random.choice(moves)
    for move in moves:
        b = board.copy()
        b.push(move)
        if b.is_checkmate():
            return move
    scored = [(move, evaluate_move(board, move)) for move in moves]
    scored.sort(key=lambda x: x[1], reverse=True)
    top_moves = scored[:top_k]
    if top_moves[0][1] > 0:
        return random.choice(top_moves)[0]
    return random.choice(moves)


def simulate(board: chess.Board, rollout_depth: int) -> float:
    mover        = not board.turn
    depth        = 0
    total_pieces = len(board.piece_map())
    is_eg        = total_pieces <= 16

    effective_depth = max(rollout_depth, 20) if is_eg else rollout_depth

    epsilon  = 0.15 if is_eg else 0.35

    while not board.is_game_over() and depth < effective_depth:
        move = greedy_move(board, top_k=3 if is_eg else 5, epsilon=epsilon)
        if move is None:
            break
        board.push(move)
        depth += 1

    result = evaluate(board)

    if abs(result) > 0.9:
        speed  = (effective_depth - depth + 1) / (effective_depth + 1)
        result = result * (0.95 + 0.05 * speed)

    return result if mover == chess.WHITE else -result


def _update_proven_value(node: Node):
    if not node.children:
        return

    visited_children = [c for c in node.children
                        if c.visits > 0 or c.proven_value is not None]
    if not visited_children:
        return

    if any(c.proven_value == float('inf') for c in visited_children):
        node.proven_value = float('inf')
        return

    all_explored = len(visited_children) == len(node.children)
    if all_explored and all(c.proven_value == float('-inf') for c in node.children):
        node.proven_value = float('-inf')


def backpropagate(node: Node, result: float):
    while node:
        node.visits += 1
        node.value  += result

        node.min_result = min(node.min_result, result)

        if node.board.is_game_over():
            outcome = node.board.outcome()
            if outcome is not None:
                if outcome.winner is None:
                    node.proven_value = 0.0
                else:
                    node.proven_value = float('-inf')

        _update_proven_value(node)

        result = -result
        node   = node.parent


def mcts(board: chess.Board, iterations: int = 10000, rollout_depth: int = 30):
    root = Node(board)
    print(f"MCTS starting: {iterations} iterations, rollout depth {rollout_depth}")

    for i in range(iterations):
        if i % 1000 == 0 and i > 0:
            print(f"  Iteration {i}/{iterations}...")

        if root.proven_value is not None:
            print(f"  Early exit at iteration {i}: root proven = {root.proven_value}")
            break

        node   = select(root)
        node   = expand(node)
        result = simulate(node.board.copy(), rollout_depth)
        backpropagate(node, result)

    if not root.children:
        print("MCTS: No legal moves found!")
        return None

    sorted_children = sorted(root.children, key=lambda n: n.visits, reverse=True)

    print("\nMCTS Results:")
    for child in sorted_children[:5]:
        move    = child.board.peek()
        avg_val = child.value / child.visits if child.visits > 0 else 0
        proven  = ""
        if child.proven_value == float('inf'):
            proven = " [PROVEN WIN]"
        elif child.proven_value == float('-inf'):
            proven = " [PROVEN LOSS]"
        elif child.proven_value == 0.0:
            proven = " [PROVEN DRAW]"
        print(f"  Move {move}: {child.visits} visits, avg value: {avg_val:.3f}{proven}")

    proven_wins = [c for c in root.children if c.proven_value == float('inf')]
    if proven_wins:
        best = proven_wins[0]
        print(f"\nBest move (PROVEN WIN): {best.board.peek()}\n")
        return best.board.peek()

    candidates = [c for c in root.children if c.proven_value != float('-inf')]
    if not candidates:
        candidates = root.children

    best    = max(candidates, key=lambda n: n.visits)
    avg_val = best.value / best.visits if best.visits > 0 else 0
    print(f"\nBest move: {best.board.peek()} with {best.visits} visits, avg: {avg_val:.3f}\n")
    return best.board.peek()