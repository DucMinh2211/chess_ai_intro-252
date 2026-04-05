import chess

# ===================== EVALUATION CONSTANTS =====================

PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000
}

PAWN_TABLE = [
    0, 0, 0, 0, 0, 0, 0, 0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
    5, 5, 10, 25, 25, 10, 5, 5,
    0, 0, 0, 20, 20, 0, 0, 0,
    5, -5, -10, 0, 0, -10, -5, 5,
    5, 10, 10, -20, -20, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0
]

KNIGHT_TABLE = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50
]

BISHOP_TABLE = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10, 5, 0, 0, 0, 0, 5, -10,
    -20, -10, -10, -10, -10, -10, -10, -20
]

ROOK_TABLE = [
    0, 0, 0, 0, 0, 0, 0, 0,
    5, 10, 10, 10, 10, 10, 10, 5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    0, 0, 0, 5, 5, 0, 0, 0
]

QUEEN_TABLE = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -5, 0, 5, 5, 5, 5, 0, -5,
    0, 0, 5, 5, 5, 5, 0, -5,
    -10, 5, 5, 5, 5, 5, 0, -10,
    -10, 0, 5, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20
]

KING_MID = [
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    20, 20, 0, 0, 0, 0, 20, 20,
    20, 30, 10, 0, 0, 10, 30, 20
]

KING_END = [
    -50, -40, -30, -20, -20, -30, -40, -50,
    -30, -20, -10, 0, 0, -10, -20, -30,
    -30, -10, 20, 30, 30, 20, -10, -30,
    -30, -10, 30, 40, 40, 30, -10, -30,
    -30, -10, 30, 40, 40, 30, -10, -30,
    -30, -10, 20, 30, 30, 20, -10, -30,
    -30, -30, 0, 0, 0, 0, -30, -30,
    -50, -30, -30, -30, -30, -30, -30, -50
]

PST = {
    chess.PAWN: PAWN_TABLE,
    chess.KNIGHT: KNIGHT_TABLE,
    chess.BISHOP: BISHOP_TABLE,
    chess.ROOK: ROOK_TABLE,
    chess.QUEEN: QUEEN_TABLE
}

def is_endgame(board: chess.Board) -> bool:
    """
    Simplified endgame detection.
    """
    white_queens = len(board.pieces(chess.QUEEN, chess.WHITE))
    black_queens = len(board.pieces(chess.QUEEN, chess.BLACK))
    
    if white_queens == 0 and black_queens == 0:
        return True
    
    for color in [chess.WHITE, chess.BLACK]:
        if len(board.pieces(chess.QUEEN, color)) > 0:
            piece_count = (len(board.pieces(chess.KNIGHT, color)) + 
                          len(board.pieces(chess.BISHOP, color)) + 
                          len(board.pieces(chess.ROOK, color)))
            
            if len(board.pieces(chess.ROOK, color)) > 0 or piece_count > 1:
                return False
    
    return True

def is_passed_pawn(board: chess.Board, square: int, color: bool) -> bool:
    """
    Check if a pawn is a passed pawn (no enemy pawns can block its path to promotion).
    """
    file = chess.square_file(square)
    rank = chess.square_rank(square)
    
    # Define files to check (current file and adjacent files)
    files_to_check = [file]
    if file > 0:
        files_to_check.append(file - 1)
    if file < 7:
        files_to_check.append(file + 1)
    
    # For white pawns, check ranks ahead; for black, check ranks behind
    if color == chess.WHITE:
        ranks_to_check = range(rank + 1, 8)
    else:
        ranks_to_check = range(0, rank)
    
    # Check if there are any enemy pawns blocking
    enemy_color = not color
    for f in files_to_check:
        for r in ranks_to_check:
            check_square = chess.square(f, r)
            piece = board.piece_at(check_square)
            if piece and piece.piece_type == chess.PAWN and piece.color == enemy_color:
                return False
    
    return True

def evaluate_promotion_potential(board: chess.Board) -> int:
    """
    Evaluate passed pawns and promotion potential.
    """
    score = 0
    
    for square in board.pieces(chess.PAWN, chess.WHITE):
        rank = chess.square_rank(square)
        if is_passed_pawn(board, square, chess.WHITE):
            # Passed pawn bonus increases as it gets closer to promotion
            distance_to_promotion = 7 - rank
            bonus = 50 + (7 - distance_to_promotion) * 20  # 50 to 190
            score += bonus
        elif rank >= 5:  # Advanced pawn (6th or 7th rank)
            score += 15 * (rank - 4)
    
    for square in board.pieces(chess.PAWN, chess.BLACK):
        rank = chess.square_rank(square)
        if is_passed_pawn(board, square, chess.BLACK):
            distance_to_promotion = rank
            bonus = 50 + (7 - distance_to_promotion) * 20
            score -= bonus
        elif rank <= 2:  # Advanced pawn (2nd or 1st rank)
            score -= 15 * (3 - rank)
    
    return score

def evaluate(board: chess.Board) -> int:
    # Material calculation for draw penalty
    mat_w = sum(len(board.pieces(pt, chess.WHITE)) * PIECE_VALUES[pt] for pt in PIECE_VALUES)
    mat_b = sum(len(board.pieces(pt, chess.BLACK)) * PIECE_VALUES[pt] for pt in PIECE_VALUES)
    diff = mat_w - mat_b

    outcome = board.outcome(claim_draw=True)
    if outcome:
        if outcome.winner is chess.WHITE: return 99999
        if outcome.winner is chess.BLACK: return -99999

        # PHẠT HÒA NẶNG: Nếu đang thắng thế (> 1 quân nhẹ) mà để hòa thì bị trừ điểm cực nặng
        if diff > 200: return -500 # Trắng đang thắng mà để hòa -> Phạt (trả về điểm xấu cho Trắng)
        if diff < -200: return 500 # Đen đang thắng mà để hòa -> Phạt (trả về điểm xấu cho Đen)
        return 0

    score = 0

    endgame = is_endgame(board)
    
    # Add promotion potential evaluation
    score += evaluate_promotion_potential(board)

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if not piece:
            continue

        value = PIECE_VALUES[piece.piece_type]

        if piece.piece_type == chess.KING:
            table = KING_END if endgame else KING_MID
        else:
            table = PST.get(piece.piece_type, [0]*64)

        # Mapping: Tables are written Rank 8 -> Rank 1.
        # For White: Rank 1 (0-7) should map to Table Row 7 (56-63).
        # For Black: Rank 8 (56-63) should map to Table Row 7 (56-63).
        if piece.color == chess.WHITE:
            idx = square ^ 56
        else:
            idx = square

        value += table[idx]
        score += value if piece.color == chess.WHITE else -value

    return score

def evaluate_move(board: chess.Board, move: chess.Move):
    """
    Score a move for move ordering (MVV-LVA).
    Useful for both Alpha-Beta (move ordering) and MCTS (smart rollouts).
    """
    score = 0
    if board.is_capture(move):
        victim = board.piece_at(move.to_square)
        attacker = board.piece_at(move.from_square)
        if victim and attacker:
            # MVV-LVA: Most Valuable Victim - Least Valuable Attacker
            score = 10 * victim.piece_type - attacker.piece_type
    
    # Prioritize promotions
    if move.promotion:
        score += 900
        
    return score
