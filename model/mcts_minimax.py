import math
import chess
import random
from model.evaluation import evaluate_move
from model.evaluation_mcts import evaluate

# ===================== MCTS-IP-M-k =====================
# Cải tiến từ MCTS cơ bản bằng cách nhúng Minimax vào giai đoạn Expansion
# để tạo Informed Prior, giúp MCTS ổn định hơn ở cuối ván.

# ── Hyperparameters ──────────────────────────────────────────────────────────
C             = 1.4   # Hằng số khám phá trong UCB1
GAMMA         = 5     # Trọng số prior: càng cao → tin Minimax nhiều hơn rollout
MINIMAX_DEPTH = 2     # Độ sâu Minimax khi tính prior (depth 1-2 là hợp lý về tốc độ)
K_BEST        = 5     # Giữ lại tối đa k nhánh tốt nhất tại mỗi tầng Minimax
# ─────────────────────────────────────────────────────────────────────────────


# ── Chuẩn hóa đánh giá ───────────────────────────────────────────────────────

def normalize_eval(raw: float) -> float:
    """
    Chuyển evaluate() từ [-1, 1] → [0, 1].
    1.0 = trắng thắng chắc, 0.0 = đen thắng chắc, 0.5 = cân bằng.
    """
    return (raw + 1.0) / 2.0


# ── Node ─────────────────────────────────────────────────────────────────────

class Node:
    """
    visits và value được khởi tạo với virtual counts từ Informed Prior.
    Khi γ=0 thì tương đương MCTS gốc.
    """
    def __init__(self, board, parent=None, virtual_visits: float = 0.0, virtual_wins: float = 0.0):
        self.board    = board
        self.parent   = parent
        self.children = []
        self.visits   = virtual_visits   # v  (bắt đầu từ γ thay vì 0)
        self.value    = virtual_wins     # w  (bắt đầu từ γ×h thay vì 0)


# ── UCT ──────────────────────────────────────────────────────────────────────

def uct(node: Node) -> float:
    """
    UCB1 chuẩn. Vì visits khởi đầu từ γ (không phải 0),
    node mới sẽ không còn bị coi là "chưa khám phá hoàn toàn"
    mà được ưu tiên theo đúng chất lượng prior của nó.
    """
    if node.visits == 0:
        return float('inf')
    exploit = node.value / node.visits
    explore = C * math.sqrt(math.log(node.parent.visits + 1) / node.visits)
    return exploit + explore


# ── Selection ────────────────────────────────────────────────────────────────

def select(node: Node) -> Node:
    """Đi xuống cây theo UCT cho đến node lá."""
    while node.children:
        # Với Informed Prior, không còn cần ưu tiên "unvisited" đặc biệt nữa
        # vì mọi node đều có virtual visits từ prior.
        # Tuy nhiên giữ lại để tương thích với trường hợp γ=0.
        unvisited = [c for c in node.children if c.visits == 0]
        if unvisited:
            return random.choice(unvisited)
        node = max(node.children, key=uct)
    return node


# ── Minimax-k-best (thành phần "M-k") ────────────────────────────────────────

def minimax_k_best(board: chess.Board, depth: int,
                   alpha: float, beta: float, maximizing: bool) -> float:
    """
    Minimax giới hạn độ sâu với:
      - α-β pruning  → cắt nhánh không cần thiết
      - k-best pruning → chỉ xét k nước đi tốt nhất tại mỗi tầng
      - Move ordering → sắp xếp theo static eval trước khi cắt

    Trả về giá trị h ∈ [0, 1] theo góc nhìn tuyệt đối của TRẮNG.
    (1 = trắng thắng, 0 = đen thắng)
    """
    if depth == 0 or board.is_game_over():
        return normalize_eval(evaluate(board))

    moves = list(board.legal_moves)
    if not moves:
        return normalize_eval(evaluate(board))

    # ── Bước 1: Đánh giá tĩnh tất cả nước đi để sắp xếp ──
    scored_moves = []
    for move in moves:
        b = board.copy()
        b.push(move)
        h = normalize_eval(evaluate(b))
        scored_moves.append((move, h))

    # ── Bước 2: Sắp xếp + k-best pruning ──
    # maximizing: ưu tiên h cao; minimizing: ưu tiên h thấp
    scored_moves.sort(key=lambda x: x[1], reverse=maximizing)
    top_k_moves = [m for m, _ in scored_moves[:K_BEST]]

    # ── Bước 3: Minimax đệ quy trên k nước đi đã lọc ──
    if maximizing:
        best = 0.0
        for move in top_k_moves:
            b = board.copy()
            b.push(move)
            val = minimax_k_best(b, depth - 1, alpha, beta, False)
            best  = max(best, val)
            alpha = max(alpha, best)
            if beta <= alpha:
                break   # α-β cut
        return best
    else:
        best = 1.0
        for move in top_k_moves:
            b = board.copy()
            b.push(move)
            val = minimax_k_best(b, depth - 1, alpha, beta, True)
            best = min(best, val)
            beta = min(beta, best)
            if beta <= alpha:
                break   # α-β cut
        return best


# ── Expansion với Informed Prior (thành phần "IP") ───────────────────────────

def expand(node: Node) -> Node:
    """
    Khi tạo node con mới, chạy Minimax-k-best để tính prior h,
    rồi khởi tạo:
        visits = γ      (virtual visits)
        value  = γ × h  (virtual wins — tính theo góc nhìn của người vừa đi)
    Điều này khiến UCT phân biệt được ngay các nước đi tốt/xấu
    ngay từ lần đầu tiên node được tạo ra, thay vì cần hàng trăm rollout.
    """
    if node.children:
        return node

    moves = list(node.board.legal_moves)
    if not moves:
        return node

    mover_is_white = (node.board.turn == chess.WHITE)

    for move in moves:
        b = node.board.copy()
        b.push(move)

        # Chạy Minimax từ trạng thái con.
        # b.turn là người sẽ đi tiếp (đối thủ của người vừa đi move).
        # maximizing=True nếu đến lượt TRẮNG tại b.
        h_white_pov = minimax_k_best(
            b,
            MINIMAX_DEPTH,
            alpha=0.0, beta=1.0,
            maximizing=(b.turn == chess.WHITE)
        )

        # Chuyển h về góc nhìn của người VỪA ĐI (mover):
        #   Nếu TRẮNG vừa đi → h_for_mover = h_white_pov
        #   Nếu ĐEN vừa đi   → h_for_mover = 1 - h_white_pov
        h_for_mover = h_white_pov if mover_is_white else (1.0 - h_white_pov)

        child = Node(
            b, node,
            virtual_visits = float(GAMMA),
            virtual_wins   = float(GAMMA) * h_for_mover,
        )
        node.children.append(child)

    return random.choice(node.children)


# ── Rollout helpers (giữ nguyên logic gốc, chỉ chuẩn hóa output) ─────────────

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
    """
    Rollout từ node lá. Trả về kết quả trong [0, 1]
    theo góc nhìn của người VỪA ĐI đến node này.
    """
    mover_is_white = not board.turn   # người vừa đi = không phải người đang đến lượt

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

    result = normalize_eval(evaluate(board))   # [0, 1], góc nhìn TRẮNG

    # Depth discount: ưu tiên kết thúc nhanh khi đang thắng/thua rõ ràng
    if result > 0.95 or result < 0.05:
        speed  = (rollout_depth - depth + 1) / (rollout_depth + 1)
        factor = 0.95 + 0.05 * speed
        result = result * factor if result > 0.5 else 1.0 - (1.0 - result) * factor

    # Đổi về góc nhìn của mover
    return result if mover_is_white else (1.0 - result)


# ── Backpropagation ───────────────────────────────────────────────────────────

def backpropagate(node: Node, result: float):
    """
    result ∈ [0, 1] theo góc nhìn của người vừa đi đến node này.
    Mỗi tầng lên thì đổi góc nhìn (1 - result).
    """
    while node:
        node.visits += 1
        node.value  += result
        result       = 1.0 - result   # đổi góc nhìn cho tầng cha
        node         = node.parent


# ── Vòng lặp MCTS chính ──────────────────────────────────────────────────────

def mcts(board: chess.Board, iterations: int = 10000, rollout_depth: int = 30) -> chess.Move | None:
    root = Node(board)
    print(
        f"MCTS-IP-M-k | iterations={iterations} | rollout_depth={rollout_depth} | "
        f"minimax_depth={MINIMAX_DEPTH} | k={K_BEST} | γ={GAMMA}"
    )

    for i in range(iterations):
        if i % 1000 == 0 and i > 0:
            print(f"  Iteration {i}/{iterations}...")

        node   = select(root)
        node   = expand(node)                          # ← Informed Prior ở đây
        result = simulate(node.board.copy(), rollout_depth)
        backpropagate(node, result)

    if not root.children:
        print("MCTS: No legal moves found!")
        return None

    sorted_children = sorted(root.children, key=lambda n: n.visits, reverse=True)

    print("\nMCTS-IP-M-k Results:")
    for child in sorted_children[:5]:
        move    = child.board.peek()
        avg_val = child.value / child.visits if child.visits > 0 else 0.0
        print(f"  Move {move}: {child.visits:.0f} visits, avg value: {avg_val:.3f}")

    best    = max(root.children, key=lambda n: n.visits)
    avg_val = best.value / best.visits if best.visits > 0 else 0.0
    print(f"\nBest move: {best.board.peek()} | {best.visits:.0f} visits | avg value: {avg_val:.3f}\n")
    return best.board.peek()