import chess
import math
from model.evaluation import evaluate

def alpha_beta_search(board: chess.Board, depth: int, heuristic_func=evaluate, alpha:float=-math.inf, beta:float=math.inf, is_root:bool=True):
    if depth == 0 or board.is_game_over():
        return heuristic_func(board)
    
    best_move = None
    maximizing = board.turn # True = White, False = Black

    if maximizing:
        max_eval = -math.inf
        
        for move in board.legal_moves:
            board.push(move)
            eval_score = alpha_beta_search(board, depth - 1, heuristic_func, alpha, beta, is_root=False)
            board.pop()
            
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
            
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break 
        
        return best_move if is_root else max_eval
    
    else:  
        min_eval = math.inf
        
        for move in board.legal_moves:
            board.push(move)
            eval_score = alpha_beta_search(board, depth - 1, heuristic_func, alpha, beta, is_root=False)
            board.pop()
            
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
            
            beta = min(beta, eval_score)
            if beta <= alpha:
                break  
        
        return best_move if is_root else min_eval
