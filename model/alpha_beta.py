import chess
from model.evaluation import evaluate

# Maximum captures to search in quiescence
QUIESCENCE_DEPTH = 4

# Transposition Table to store evaluated positions
# Key: Zobrist hash (or board FEN), Value: (depth, score, flag)
# flag: 0 = exact, 1 = alpha (upper bound), 2 = beta (lower bound)
transposition_table = {}

def get_transposition(board, depth, alpha, beta):
    key = board.fen()
    if key in transposition_table:
        entry_depth, entry_score, entry_flag = transposition_table[key]
        if entry_depth >= depth:
            if entry_flag == 0:
                return entry_score
            elif entry_flag == 1 and entry_score <= alpha:
                return alpha
            elif entry_flag == 2 and entry_score >= beta:
                return beta
    return None

def store_transposition(board, depth, score, flag):
    key = board.fen()
    transposition_table[key] = (depth, score, flag)

def quiescence(board: chess.Board, alpha: float, beta: float, depth: int):
    """
    Search all captures until a "quiet" position is reached.
    Uses Negamax style: score is relative to the side to move.
    """
    # Base evaluation from the perspective of the side to move
    stand_pat = evaluate(board) if board.turn == chess.WHITE else -evaluate(board)
    
    if stand_pat >= beta:
        return beta
    if alpha < stand_pat:
        alpha = stand_pat

    if depth <= 0:
        return stand_pat

    # Only look at captures
    moves = [m for m in board.legal_moves if board.is_capture(m)]
    # Sort by MVV-LVA
    moves.sort(key=lambda m: evaluate_move(board, m), reverse=True)

    for move in moves:
        board.push(move)
        # Negamax: -quiescence with flipped alpha/beta
        score = -quiescence(board, -beta, -alpha, depth - 1)
        board.pop()

        if score >= beta:
            return beta
        if score > alpha:
            alpha = score
    
    return alpha

def evaluate_move(board: chess.Board, move: chess.Move):
    """
    Score a move for move ordering (MVV-LVA).
    """
    score = 0
    if board.is_capture(move):
        victim = board.piece_at(move.to_square)
        attacker = board.piece_at(move.from_square)
        if victim and attacker:
            score = 10 * victim.piece_type - attacker.piece_type
    
    # Prioritize promotions
    if move.promotion:
        score += 900
        
    return score

def negamax(board: chess.Board, depth: int, alpha: float, beta: float):
    """
    Negamax implementation of Alpha-Beta Pruning.
    """
    alpha_orig = alpha
    
    # Check Transposition Table
    cached_score = get_transposition(board, depth, alpha, beta)
    if cached_score is not None:
        return cached_score

    if board.is_game_over():
        score = evaluate(board)
        return score if board.turn == chess.WHITE else -score
    
    if depth == 0:
        return quiescence(board, alpha, beta, QUIESCENCE_DEPTH)

    best_value = -float('inf')
    moves = list(board.legal_moves)
    # Better move ordering: captures and promotions first
    moves.sort(key=lambda m: evaluate_move(board, m), reverse=True)

    for move in moves:
        board.push(move)
        value = -negamax(board, depth - 1, -beta, -alpha)
        board.pop()
        
        best_value = max(best_value, value)
        alpha = max(alpha, value)
        if alpha >= beta:
            break
            
    # Store in Transposition Table
    flag = 0
    if best_value <= alpha_orig:
        flag = 1 # Upper bound
    elif best_value >= beta:
        flag = 2 # Lower bound
    else:
        flag = 0 # Exact
    store_transposition(board, depth, best_value, flag)
    
    return best_value

def alpha_beta_best_move(board: chess.Board, depth: int):
    """
    Entry point for bot move selection using Negamax.
    """
    # Clear TT for a new search to avoid stale data if memory is an issue, 
    # but keeping it across turns is usually better.
    # transposition_table.clear() 

    best_move = None
    best_value = -float('inf')
    
    alpha = -float('inf')
    beta = float('inf')

    moves = list(board.legal_moves)
    moves.sort(key=lambda m: evaluate_move(board, m), reverse=True)
    
    for move in moves:
        board.push(move)
        # Negamax: value is relative to the side that just moved
        value = -negamax(board, depth - 1, -beta, -alpha)
        board.pop()

        if value > best_value:
            best_value = value
            best_move = move
        
        alpha = max(alpha, value)

    return best_move
