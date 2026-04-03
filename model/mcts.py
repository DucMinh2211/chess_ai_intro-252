import math
import chess
import random
from model.evaluation import evaluate_move
from model.evaluation_mcts import evaluate

# ===================== MCTS =====================

C = 1.4

class Node:
    def __init__(self, board, parent=None):
        self.board = board
        self.parent = parent
        self.children = []
        self.visits = 0
        self.value = 0


def uct(node, max_score = 1000):
    if node.visits == 0:
        return float('inf')

    # exploit = math.tanh((node.value / (node.visits * 1000))/max_score)

    # explore = C * math.sqrt(math.log(node.parent.visits + 1) / node.visits)
    exploit = node.value / node.visits
    explore = C * math.sqrt(math.log(node.parent.visits + 1) / node.visits)

    return exploit + explore


def select(node):
    while node.children:
        unvisited = [c for c in node.children if c.visits == 0]
        if unvisited:
            return random.choice(unvisited)
        # node = max(node.children, key=lambda n: uct(n, max_score))
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

def greedy_move(board, top_k=5, epsilon=0.2):
    """
    Greedy move selection dựa trên evaluate_move (MVV-LVA).
    - top_k: chọn ngẫu nhiên trong top K moves tốt nhất (tránh quá deterministic)
    - epsilon: xác suất random hoàn toàn (exploration)
    """
    moves = list(board.legal_moves)
    if not moves:
        return None
    
    # Epsilon-greedy: đôi khi random để tránh bị khai thác
    if random.random() < epsilon:
        return random.choice(moves)
    
    # Ưu tiên tuyệt đối: chiếu hết ngay lập tức
    for move in moves:
        b = board.copy()
        b.push(move)
        if b.is_checkmate():
            return move
    
    # Score tất cả moves bằng evaluate_move
    scored = [(move, evaluate_move(board, move)) for move in moves]
    scored.sort(key=lambda x: x[1], reverse=True)
    
    # Lấy top_k moves tốt nhất, random trong đó
    # Tránh greedy thuần 100% làm rollout bị bias
    top_moves = scored[:top_k]
    
    # Nếu move tốt nhất có score > 0 (có capture/promotion), dùng top_k
    # Nếu tất cả score == 0 (toàn quiet moves), random hoàn toàn
    if top_moves[0][1] > 0:
        return random.choice(top_moves)[0]
    else:
        return random.choice(moves)



def simulate(board, rollout_depth: int):
    mover = not board.turn
    depth = 0
    total_pieces = len(board.piece_map())
    is_endgame = total_pieces <= 12
    epsilon = 0.15 if is_endgame else 0.35

    while not board.is_game_over() and depth < rollout_depth:
        move = greedy_move(board, top_k=3 if is_endgame else 5, epsilon=epsilon)
        if move is None:
            break
        board.push(move)
        depth += 1

    # ✅ Không cần clamp, không cần tanh ở đây nữa
    # evaluate() đã trả [-1, 1] trực tiếp
    result = evaluate(board)

    # ✅ Depth discount: thắng nhanh hơn thì tốt hơn
    # Chỉ áp dụng khi result gần ±1 (đang thắng/thua rõ)
    if abs(result) > 0.9:
        speed = (rollout_depth - depth + 1) / (rollout_depth + 1)
        result = result * (0.95 + 0.05 * speed)

    return result if mover == chess.WHITE else -result


def backpropagate(node, result):
    while node:
        node.visits += 1
        node.value += result
        result = - result
        node = node.parent


def mcts(board, iterations=10000, rollout_depth=30):
    root = Node(board)
    # max_score = 1.0
    print(f"MCTS starting: {iterations} iterations, rollout depth {rollout_depth}")

    for i in range(iterations):
        if i % 1000 == 0 and i > 0:
            print(f"  Iteration {i}/{iterations}...")

        node = select(root)
        node = expand(node)
        result = simulate(node.board.copy(), rollout_depth)
        # max_score = max(max_score, abs(result) + 1)
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

    # best = max(root.children, key=lambda n: math.tanh((n.value / n.visits) / max_score) if n.visits > 0 else float('-inf'))
    best = max(root.children, key=lambda n: n.visits)
    avg = best.value / best.visits if best.visits > 0 else 0
    print(f"\nBest move: {best.board.peek()} with {best.visits} visits\n")
    return best.board.peek()
