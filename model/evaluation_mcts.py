import chess
import math

PIECE_VALS: dict[int, int] = {
    chess.PAWN:   100,
    chess.KNIGHT: 280,
    chess.BISHOP: 320,
    chess.ROOK:   479,
    chess.QUEEN:  929,
    chess.KING:   60_000,
}

PST: dict[int, tuple] = {
    chess.PAWN: (
           0,   0,   0,   0,   0,   0,   0,   0,
          78,  83,  86,  73, 102,  82,  85,  90,
           7,  29,  21,  44,  40,  31,  44,   7,
         -17,  16,  -2,  15,  14,   0,  15, -13,
         -26,   3,  10,   9,   6,   1,   0, -23,
         -22,   9,   5, -11, -10,  -2,   3, -19,
         -31,   8,  -7, -37, -36, -14,   3, -31,
           0,   0,   0,   0,   0,   0,   0,   0,
    ),
    chess.KNIGHT: (
         -66, -53, -75, -75, -10, -55, -58, -70,
          -3,  -6, 100, -36,   4,  62,  -4, -14,
          10,  67,   1,  74,  73,  27,  62,  -2,
          24,  24,  45,  37,  33,  41,  25,  17,
          -1,   5,  31,  21,  22,  35,   2,   0,
         -18,  10,  13,  22,  18,  15,  11, -14,
         -23, -15,   2,   0,   2,   0, -23, -20,
         -74, -23, -26, -24, -19, -35, -22, -69,
    ),
    chess.BISHOP: (
         -59, -78, -82, -76, -23,-107, -37, -50,
          -11,  20,  35, -42, -39,  31,   2, -22,
          -9,  39, -32,  41,  52, -10,  28, -14,
          25,  17,  20,  34,  26,  25,  15,  10,
          13,  10,  17,  23,  17,  16,   0,   7,
          14,  25,  24,  15,   8,  25,  20,  15,
          19,  20,  11,   6,   7,   6,  20,  16,
          -7,   2, -15, -12, -14, -15, -10, -10,
    ),
    chess.ROOK: (
           35,  29,  33,   4,  37,  33,  56,  50,
           55,  29,  56,  67,  55,  62,  34,  60,
           19,  35,  28,  33,  45,  27,  25,  15,
            0,   5,  16,  13,  18,  -4,  -9,  -6,
          -28, -35, -16, -21, -13, -29, -46, -30,
          -42, -28, -42, -25, -25, -35, -26, -46,
          -53, -38, -31, -26, -29, -43, -44, -53,
          -30, -24, -18,   5,  -2, -18, -31, -32,
    ),
    chess.QUEEN: (
            6,   1,  -8,-104,  69,  24,  88,  26,
           14,  32,  60, -10,  20,  76,  57,  24,
           -2,  43,  32,  60,  72,  63,  43,   2,
            1, -16,  22,  17,  25,  20, -13,  -6,
          -14, -15,  -2,  -5,  -1, -10, -20, -22,
          -30,  -6, -13, -11, -16, -11, -16, -27,
          -36, -18,   0, -19, -15, -15, -21, -38,
          -39, -30, -31, -13, -31, -36, -34, -42,
    ),
}

KING_MID: tuple = (
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -10, -20, -20, -20, -20, -20, -20, -10,
     20,  20,   0,   0,   0,   0,  20,  20,
     20,  30,  10,   0,   0,  10,  30,  20,
)
KING_END: tuple = (
    -50, -40, -30, -20, -20, -30, -40, -50,
    -30, -20, -10,   0,   0, -10, -20, -30,
    -30, -10,  20,  30,  30,  20, -10, -30,
    -30, -10,  30,  40,  40,  30, -10, -30,
    -30, -10,  30,  40,  40,  30, -10, -30,
    -30, -10,  20,  30,  30,  20, -10, -30,
    -30, -30,   0,   0,   0,   0, -30, -30,
    -50, -30, -30, -30, -30, -30, -30, -50,
)

def is_endgame(board: chess.Board) -> bool:
    wq = len(board.pieces(chess.QUEEN, chess.WHITE))
    bq = len(board.pieces(chess.QUEEN, chess.BLACK))
    if wq == 0 and bq == 0:
        return True
    for color in (chess.WHITE, chess.BLACK):
        if len(board.pieces(chess.QUEEN, color)) > 0:
            minors = (len(board.pieces(chess.KNIGHT, color))
                      + len(board.pieces(chess.BISHOP, color)))
            if len(board.pieces(chess.ROOK, color)) > 0 or minors > 1:
                return False
    return True

def _pst_idx(square: int, color: chess.Color) -> int:
    return (square ^ 56) if color == chess.WHITE else square

def _material_and_pst(board: chess.Board, endgame: bool) -> float:
    score    = 0
    king_tbl = KING_END if endgame else KING_MID
    for sq, piece in board.piece_map().items():
        idx = _pst_idx(sq, piece.color)
        if piece.piece_type == chess.KING:
            val = PIECE_VALS[chess.KING] + king_tbl[idx]
        else:
            val = PIECE_VALS[piece.piece_type] + PST[piece.piece_type][idx]
        score += val if piece.color == chess.WHITE else -val
    return score

def _king_safety(board: chess.Board) -> float:
    score = 0.0
    for color in (chess.WHITE, chess.BLACK):
        king_sq = board.king(color)
        if king_sq is None:
            continue
        sign  = 1 if color == chess.WHITE else -1
        enemy = not color
        for sq in chess.SquareSet(chess.BB_KING_ATTACKS[king_sq]):
            p = board.piece_at(sq)
            if p and p.color == color and p.piece_type == chess.PAWN:
                score += sign * 10
            if board.is_attacked_by(enemy, sq):
                score -= sign * 8
        if board.is_attacked_by(enemy, king_sq):
            score -= sign * 50
    return score

def _threat_bonus(board: chess.Board) -> float:
    score = 0.0
    for sq, piece in board.piece_map().items():
        sign        = 1 if piece.color == chess.WHITE else -1
        enemy_color = not piece.color
        for attacked_sq in board.attacks(sq):
            target = board.piece_at(attacked_sq)
            if target and target.color == enemy_color:
                bonus = 2.0 if target.piece_type == chess.KING \
                              else PIECE_VALS[target.piece_type] * 0.03
                score += sign * bonus
    return score

def _mobility(board: chess.Board) -> float:
    w = b = 0
    for sq, piece in board.piece_map().items():
        n = len(board.attacks(sq))
        if piece.color == chess.WHITE:
            w += n
        else:
            b += n
    return (w - b) * 0.4

def _raw_material(board: chess.Board) -> float:
    mat = 0
    for sq, piece in board.piece_map().items():
        if piece.piece_type == chess.KING:
            continue
        v = PIECE_VALS[piece.piece_type]
        mat += v if piece.color == chess.WHITE else -v
    return mat

def _mating_net_bonus(board: chess.Board) -> float:
    mat = _raw_material(board)
    if abs(mat) >= 300:
        return 0.0

    score = 0.0
    for color in (chess.WHITE, chess.BLACK):
        king_sq = board.king(color)
        if king_sq is None:
            continue
        sign = 1 if color == chess.WHITE else -1
        enemy = not color
        enemy_king_sq = board.king(enemy)
        if enemy_king_sq is not None:
            enemy_mob = sum(
                1 for sq in chess.SquareSet(chess.BB_KING_ATTACKS[enemy_king_sq])
                if not board.is_attacked_by(color, sq)
            )
            score += sign * (8 - enemy_mob) * 5
    return score

def _endgame_mating_score(board: chess.Board, winning_color: chess.Color) -> float:
    losing_color    = not winning_color
    losing_king_sq  = board.king(losing_color)
    winning_king_sq = board.king(winning_color)
    if losing_king_sq is None or winning_king_sq is None:
        return 0.70

    lk_file = chess.square_file(losing_king_sq)
    lk_rank = chess.square_rank(losing_king_sq)
    wk_file = chess.square_file(winning_king_sq)
    wk_rank = chess.square_rank(winning_king_sq)

    center_dist = max(3 - lk_file, lk_file - 4, 0) + max(3 - lk_rank, lk_rank - 4, 0)
    corner_score = center_dist / 6.0

    enemy_free_squares = sum(
        1 for sq in chess.SquareSet(chess.BB_KING_ATTACKS[losing_king_sq])
        if not board.is_attacked_by(winning_color, sq)
    )
    confinement_score = 1.0 - enemy_free_squares / 8.0

    king_dist = abs(lk_file - wk_file) + abs(lk_rank - wk_rank)
    proximity_score = 1.0 - king_dist / 14.0

    mating_progress = (
        0.40 * corner_score
        + 0.35 * confinement_score
        + 0.25 * proximity_score
    )

    return 0.55 + 0.42 * mating_progress

def evaluate(board: chess.Board) -> float:
    if board.is_checkmate():
        return -1.0 if board.turn == chess.WHITE else 1.0
    if board.is_stalemate() or board.is_insufficient_material():
        return 0.0

    is_rep = (board.is_repetition(2)
              or board.is_fivefold_repetition()
              or board.is_seventyfive_moves())

    mat     = _raw_material(board)
    endgame = is_endgame(board)

    if endgame and abs(mat) >= 200:
        winning_color = chess.WHITE if mat > 0 else chess.BLACK
        sign          = 1.0 if winning_color == chess.WHITE else -1.0
        pos_score     = _endgame_mating_score(board, winning_color)
        result        = sign * pos_score

        if is_rep:
            return result * 0.15
        return result

    raw = (
        _material_and_pst(board, endgame)
        + _king_safety(board)
        + _threat_bonus(board)
        + _mobility(board)
        + _mating_net_bonus(board)
    )
    divisor = 800 if endgame else 3000
    base    = math.tanh(raw / divisor)

    if is_rep:
        if abs(base) < 0.05:
            return 0.0
        return base * 0.15

    return base

def evaluate_move(board: chess.Board, move: chess.Move) -> float:
    piece = board.piece_at(move.from_square)
    if piece is None:
        return 0.0

    endgame  = is_endgame(board)
    king_tbl = KING_END if endgame else KING_MID
    from_idx = _pst_idx(move.from_square, piece.color)
    to_idx   = _pst_idx(move.to_square,   piece.color)

    if piece.piece_type == chess.KING:
        score = float(king_tbl[to_idx] - king_tbl[from_idx])
    else:
        score = float(PST[piece.piece_type][to_idx]
                    - PST[piece.piece_type][from_idx])

    captured = board.piece_at(move.to_square)
    if captured:
        score += 10 * captured.piece_type - piece.piece_type

    if board.is_en_passant(move):
        score += chess.PAWN * 10

    if move.promotion:
        score += PIECE_VALS.get(move.promotion, 0) - PIECE_VALS[chess.PAWN]

    if board.is_castling(move):
        score += 60

    enemy_color   = not piece.color
    enemy_king_sq = board.king(enemy_color)

    if enemy_king_sq is not None:
        dest_attacks = chess.SquareSet(chess.BB_KING_ATTACKS[move.to_square])
        if enemy_king_sq in dest_attacks:
            score += 80
        king_neighbors = chess.SquareSet(chess.BB_KING_ATTACKS[enemy_king_sq])
        if move.to_square in king_neighbors:
            score += 40

        mat = _raw_material(board)
        if endgame and abs(mat) >= 200:
            sign = 1 if piece.color == chess.WHITE else -1
            if mat * sign > 0:

                ek_file = chess.square_file(enemy_king_sq)
                ek_rank = chess.square_rank(enemy_king_sq)
                to_file = chess.square_file(move.to_square)
                to_rank = chess.square_rank(move.to_square)

                if piece.piece_type == chess.KING:
                    from_file = chess.square_file(move.from_square)
                    from_rank = chess.square_rank(move.from_square)
                    dist_before = abs(ek_file - from_file) + abs(ek_rank - from_rank)
                    dist_after  = abs(ek_file - to_file)   + abs(ek_rank - to_rank)
                    score += (dist_before - dist_after) * 25

                elif piece.piece_type in (chess.ROOK, chess.QUEEN):
                    if to_file == ek_file or to_rank == ek_rank:
                        score += 35

                if (move.to_square not in king_neighbors
                        and enemy_king_sq not in dest_attacks):
                    score -= 15

    return score