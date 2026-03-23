import eel
from model.alpha_beta import *
from model.mcts import *
import chess
import random

eel.init('UI')

@eel.expose
def get_legal_moves(fen: str):
    board = chess.Board(fen)
    moves_dict = {}
    for move in board.legal_moves:
        from_sq = chess.square_name(move.from_square)
        to_sq = chess.square_name(move.to_square)
        if from_sq not in moves_dict:
            moves_dict[from_sq] = []
        moves_dict[from_sq].append(to_sq)
    return moves_dict

@eel.expose
def apply_move(fen: str, from_sq: str, to_sq: str, promotion=None):
    board = chess.Board(fen)
    move_uci = from_sq + to_sq
    
    if promotion:
        move_uci += promotion
    else:
        from_square = chess.parse_square(from_sq)
        to_square = chess.parse_square(to_sq)
        piece = board.piece_at(from_square)
        
        if piece and piece.piece_type == chess.PAWN:
            to_rank = chess.square_rank(to_square)
            if to_rank == 7 or to_rank == 0:
                move_uci += 'q'
    
    move = chess.Move.from_uci(move_uci)
    if move in board.legal_moves:
        board.push(move)
        return board.fen()
    return fen

@eel.expose
def get_bot_move(fen: str, bot_type: str, depth: int):
    board = chess.Board(fen)
    move = None
    
    if bot_type == 'random':
        moves = list(board.legal_moves)
        move = random.choice(moves)
    elif bot_type == 'alphabeta':
        move = alpha_beta_best_move(board, int(depth))
    elif bot_type == 'mcts':
        # * Fixed iterations for MCTS
        move = mcts(board, iterations=500)
    else:
        raise Exception('Unknown Bot type')

    if not move: raise Exception('Bot could not find a move')
    return {
        'from': chess.square_name(move.from_square),
        'to': chess.square_name(move.to_square),
        'promotion': chess.piece_symbol(move.promotion) if move.promotion else None
    }

@eel.expose
def get_game_status(fen: str):
    board = chess.Board(fen)
    
    if board.is_checkmate():
        if board.turn == chess.WHITE:
            return {'game_over': True, 'result': 'black'}
        else:
            return {'game_over': True, 'result': 'white'}
    elif board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves() or board.is_fivefold_repetition():
        return {'game_over': True, 'result': 'draw'}
    
    return {'game_over': False, 'result': ''}

if __name__ == "__main__":
    print("Chess AI starting...")
    print("If no browser window opens automatically, please visit: http://localhost:8000")
    try:
        # Standard launch (tries to find Chrome/Chromium)
        eel.start('index.html', size=(1000, 700), cmdline_args=['--no-sandbox'])
    except Exception as e:
        print(f"Native browser launch failed ({e}). Falling back to browser mode...")
        # Fallback for WSL/headless: opens in the default system browser (Windows or Linux)
        eel.start('index.html', size=(1000, 700), mode='browser')
