import chess
from model.evaluation import evaluate, evaluate_move

# Transposition Table to store evaluated positions
transposition_table = {}

def clear_transposition_table():
    global transposition_table
    transposition_table = {}
    print("AI Transposition Table cleared.")

def get_position_key(board):
    """Simplified FEN excluding move counters for better cache hits."""
    parts = board.fen().split(' ')
    return " ".join(parts[:4])

def get_transposition(board, depth, alpha, beta):
    key = get_position_key(board)
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
    key = get_position_key(board)
    transposition_table[key] = (depth, score, flag)

def quiescence(board: chess.Board, alpha: float, beta: float, depth: int):
    stand_pat = evaluate(board) if board.turn == chess.WHITE else -evaluate(board)
    
    if stand_pat >= beta:
        return beta
    if alpha < stand_pat:
        alpha = stand_pat

    if depth <= 0:
        return stand_pat

    moves = [m for m in board.legal_moves if board.is_capture(m)]
    moves.sort(key=lambda m: evaluate_move(board, m), reverse=True)
    for move in moves:
        board.push(move)
        score = -quiescence(board, -beta, -alpha, depth - 1)
        board.pop()

        if score >= beta:
            return beta
        if score > alpha:
            alpha = score
    
    return alpha

def negamax(board: chess.Board, depth: int, alpha: float, beta: float, q_depth: int):
    # 1. CRITICAL: Check for game over (including repetitions) BEFORE cache lookup
    # This prevents AI from using a "winning" score from history for a position that is now a draw.
    if board.is_game_over():
        score = evaluate(board)
        # Mate distance scoring: prefer faster mates
        if score > 90000: score += depth
        elif score < -90000: score -= depth
        return score if board.turn == chess.WHITE else -score

    # 2. Treat 2-fold repetition as draw during search to avoid loops
    if board.is_repetition(2):
        score = evaluate(board) # This will return the draw penalty if winning
        return score if board.turn == chess.WHITE else -score

    alpha_orig = alpha
    
    # 3. Check Transposition Table
    cached_score = get_transposition(board, depth, alpha, beta)
    if cached_score is not None:
        return cached_score

    if depth == 0:
        return quiescence(board, alpha, beta, q_depth)

    best_value = -float('inf')
    moves = list(board.legal_moves)
    # Move ordering: captures and promotions first
    moves.sort(key=lambda m: evaluate_move(board, m), reverse=True)

    for move in moves:
        board.push(move)
        value = -negamax(board, depth - 1, -beta, -alpha, q_depth)
        board.pop()
        
        if value > best_value:
            best_value = value
        
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

def alpha_beta_best_move(board: chess.Board, depth: int, q_depth: int = 4):
    best_move = None
    best_value = -float('inf')
    
    alpha = -float('inf')
    beta = float('inf')

    moves = list(board.legal_moves)
    moves.sort(key=lambda m: evaluate_move(board, m), reverse=True)
    
    for move in moves:
        board.push(move)
        value = -negamax(board, depth - 1, -beta, -alpha, q_depth)
        board.pop()

        if value > best_value:
            best_value = value
            best_move = move
        
        alpha = max(alpha, value)

    return best_move
