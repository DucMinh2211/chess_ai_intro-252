import math
import random
import chess

from model.alpha_beta import negamax
from model.evaluation import evaluate_move
from model.evaluation_mcts import evaluate as rollout_eval

AB_DEPTH      = 3
Q_DEPTH       = 2
TOP_K         = 8
GAMMA         = 12
C             = 1.4
ROLLOUT_DEPTH = 5


def sigmoid_normalize(centipawns: float) -> float:
    return 1.0 / (1.0 + math.exp(-centipawns / 400.0))


def normalize_rollout(raw: float) -> float:
    return (raw + 1.0) / 2.0


def ab_screen_moves(board: chess.Board, top_k: int = TOP_K):
    moves = list(board.legal_moves)
    moves.sort(key=lambda m: evaluate_move(board, m), reverse=True)

    alpha = -float('inf')
    beta  =  float('inf')
    scored = []

    for move in moves:
        board.push(move)
        value = -negamax(board, AB_DEPTH - 1, -beta, -alpha, Q_DEPTH)
        board.pop()

        scored.append((move, value))
        alpha = max(alpha, value)

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:top_k]


class Node:
    def __init__(self, board: chess.Board, parent=None,
                 virtual_visits: float = 0.0, virtual_wins: float = 0.0):
        self.board    = board
        self.parent   = parent
        self.children: list["Node"] = []
        self.visits   = virtual_visits
        self.value    = virtual_wins


def uct(node: Node) -> float:
    if node.visits == 0:
        return float('inf')
    exploit = node.value / node.visits
    explore = C * math.sqrt(math.log(node.parent.visits + 1) / node.visits)
    return exploit + explore


def select(node: Node) -> Node:
    while node.children:
        unvisited = [c for c in node.children if c.visits == 0]
        if unvisited:
            return random.choice(unvisited)
        node = max(node.children, key=uct)
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
        node.children.append(Node(b, parent=node))

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
    scored = [(m, evaluate_move(board, m)) for m in moves]
    scored.sort(key=lambda x: x[1], reverse=True)
    top = scored[:top_k]
    return random.choice(top)[0] if top[0][1] > 0 else random.choice(moves)


def simulate(board: chess.Board, rollout_depth: int = ROLLOUT_DEPTH) -> float:
    mover_is_white = not board.turn

    total_pieces = len(board.piece_map())
    is_endgame   = total_pieces <= 12
    epsilon      = 0.15 if is_endgame else 0.35
    depth        = 0

    while not board.is_game_over() and depth < rollout_depth:
        move = greedy_move(board, top_k=3 if is_endgame else 5, epsilon=epsilon)
        if move is None:
            break
        board.push(move)
        depth += 1

    result = normalize_rollout(rollout_eval(board))

    if result > 0.95 or result < 0.05:
        speed  = (rollout_depth - depth + 1) / (rollout_depth + 1)
        factor = 0.95 + 0.05 * speed
        result = result * factor if result > 0.5 else 1.0 - (1.0 - result) * factor

    return result if mover_is_white else (1.0 - result)


def backpropagate(node: Node, result: float):
    while node:
        node.visits += 1
        node.value  += result
        result       = 1.0 - result
        node         = node.parent


def build_seeded_root(board: chess.Board,
                      ab_candidates: list[tuple[chess.Move, float]]) -> Node:
    root = Node(board)

    for move, ab_score_mover_pov in ab_candidates:
        b = board.copy()
        b.push(move)

        win_prob = sigmoid_normalize(ab_score_mover_pov)

        child = Node(
            b, parent=root,
            virtual_visits = float(GAMMA),
            virtual_wins   = float(GAMMA) * win_prob,
        )
        root.children.append(child)

    root.visits = sum(c.visits for c in root.children)
    root.value  = sum(c.value  for c in root.children)

    return root


def ab_mcts_best_move(board: chess.Board,
                      iterations: int = 8000,
                      top_k: int = TOP_K) -> chess.Move | None:
    print(
        f"\n{'='*60}\n"
        f"AB-MCTS | AB depth={AB_DEPTH} q_depth={Q_DEPTH} "
        f"top_k={top_k} | γ={GAMMA} C={C} | iters={iterations}\n"
        f"{'='*60}"
    )

    print("\n[Phase 1] Alpha-Beta screening all legal moves...")
    ab_candidates = ab_screen_moves(board, top_k=top_k)

    if not ab_candidates:
        print("No legal moves available.")
        return None

    print(f"  Retained top {len(ab_candidates)} candidates:")
    for i, (move, score) in enumerate(ab_candidates):
        prob = sigmoid_normalize(score)
        print(f"  {i+1:2d}. {move}  AB={score:+.0f} cp  →  prior={prob:.3f}")

    print(f"\n[Phase 2] MCTS expanding {len(ab_candidates)} branches "
          f"({iterations} iterations)...")

    root = build_seeded_root(board, ab_candidates)

    for i in range(iterations):
        if i % 1000 == 0 and i > 0:
            print(f"  Iteration {i}/{iterations}...")

        node   = select(root)
        node   = expand(node)
        result = simulate(node.board.copy())
        backpropagate(node, result)

    if not root.children:
        return None

    sorted_children = sorted(root.children, key=lambda n: n.visits, reverse=True)

    print("\nAB-MCTS Final Rankings (by visits):")
    for child in sorted_children[:min(5, len(sorted_children))]:
        move    = child.board.peek()
        avg_val = child.value / child.visits if child.visits > 0 else 0.0
        ab_s    = next((s for m, s in ab_candidates if m == move), None)
        ab_str  = f"AB={ab_s:+.0f}" if ab_s is not None else ""
        print(f"  {move}: {child.visits:.0f} visits  "
              f"avg={avg_val:.3f}  {ab_str}")

    best    = max(root.children, key=lambda n: n.visits)
    avg_val = best.value / best.visits if best.visits > 0 else 0.0
    move    = best.board.peek()
    print(f"\n>>> Best move: {move} | {best.visits:.0f} visits | "
          f"avg value: {avg_val:.3f}\n{'='*60}\n")
    return move