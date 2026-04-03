import chess
import math

# ============ Constants ============
PIECE_VALUES = {
    chess.PAWN:   100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK:   500,
    chess.QUEEN:  900,
    chess.KING:   0
}

EVAL_SCALE = 300  # ~3 pawns = tanh(1.0) ≈ 0.76, đủ gradient cho endgame

def material_score(board: chess.Board) -> int:
    """Raw centipawn score, white-positive"""
    score = 0
    for piece_type, value in PIECE_VALUES.items():
        score += len(board.pieces(piece_type, chess.WHITE)) * value
        score -= len(board.pieces(piece_type, chess.BLACK)) * value
    return score

def mobility_score(board: chess.Board) -> int:
    """Số legal moves của mỗi bên — quan trọng ở endgame"""
    # Đếm moves của White
    board.turn = chess.WHITE
    white_moves = board.legal_moves.count()
    
    # Đếm moves của Black  
    board.turn = chess.BLACK
    black_moves = board.legal_moves.count()
    
    return (white_moves - black_moves) * 5  # 5cp mỗi move

def king_safety_endgame(board: chess.Board) -> int:
    """
    Endgame: king nên tiến về trung tâm
    Dùng distance từ king đến center để score
    """
    total_pieces = len(board.piece_map())
    if total_pieces > 14:
        return 0  # Chỉ áp dụng endgame
    
    center = chess.E4  # Tham chiếu trung tâm
    
    wk = board.king(chess.WHITE)
    bk = board.king(chess.BLACK)
    
    if wk is None or bk is None:
        return 0
    
    # Manhattan distance đến trung tâm
    def dist_to_center(sq):
        r, f = chess.square_rank(sq), chess.square_file(sq)
        return abs(r - 3.5) + abs(f - 3.5)
    
    # White king gần trung tâm = tốt cho White
    # Black king gần trung tâm = tốt cho Black
    score = (dist_to_center(bk) - dist_to_center(wk)) * 10
    return score

def evaluate(board: chess.Board) -> float:
    """
    Trả về float trong [-1.0, 1.0] — đồng bộ với MCTS.
    
    Xử lý terminal states đặc biệt:
    - Checkmate: ±1.0 (không phải ±20000)
    - Stalemate/Draw: 0.0
    - Đang chơi: tanh(raw / EVAL_SCALE)
    """
    # ✅ Terminal states — trả giá trị tuyệt đối, không qua tanh
    if board.is_checkmate():
        # Bên vừa đi tạo checkmate → bên đang turn là bên thua
        return -1.0 if board.turn == chess.WHITE else 1.0

    if board.is_stalemate() or board.is_insufficient_material():
        return 0.0

    if board.is_seventyfive_moves() or board.is_fivefold_repetition():
        return 0.0

    # ✅ Material — thành phần chính
    raw = material_score(board)

    # ✅ Mobility — phân biệt được moves khi vật chất bằng nhau
    raw += mobility_score(board)

    # ✅ King activity — quan trọng ở endgame
    raw += king_safety_endgame(board)

    # ✅ Normalize về [-1, 1] với gradient rõ ở range thực tế
    # EVAL_SCALE = 300: chênh 3 pawns → tanh(1.0) = 0.76
    # Checkmate thực sự đã được handle ở trên → không bao giờ saturate ở đây
    return math.tanh(raw / EVAL_SCALE)
