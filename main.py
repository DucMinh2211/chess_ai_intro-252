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
        san_move = board.san(move)
        board.push(move)
        print(f"Move played: {san_move}")
        return {'fen': board.fen(), 'san': san_move}
    return {'fen': fen, 'san': ''}

@eel.expose
def get_bot_move(fen: str, bot_type: str, params: dict):
    board = chess.Board(fen)
    move = None
    
    print(f"AI ({bot_type}) is thinking...", end=" ", flush=True)
    if bot_type == 'random':
        moves = list(board.legal_moves)
        move = random.choice(moves)
    elif bot_type == 'alphabeta':
        depth = int(params.get('depth', 3))
        q_depth = int(params.get('q_depth', 4))
        move = alpha_beta_best_move(board, depth, q_depth)
    elif bot_type == 'mcts':
        iters = int(params.get('iterations', 10000))
        rollout_depth = int(params.get('rollout_depth', 30))
        move = mcts(board, iterations=iters, rollout_depth=rollout_depth)
    else:
        print("Error!")
        raise Exception('Unknown Bot type')

    if not move: 
        print("Failed!")
        raise Exception('Bot could not find a move')
    
    print(f"Done. Selected: {board.san(move)}")
    return {
        'from': chess.square_name(move.from_square),
        'to': chess.square_name(move.to_square),
        'promotion': chess.piece_symbol(move.promotion) if move.promotion else None
    }

@eel.expose
def get_game_status(fen: str):
    board = chess.Board(fen)
    if board.is_checkmate():
        res = 'black' if board.turn == chess.WHITE else 'white'
        print(f"Game Over: Checkmate! Winner: {res}")
        return {'game_over': True, 'result': res}
    if board.is_game_over():
        print(f"Game Over: Draw! ({board.outcome().termination.name})")
        return {'game_over': True, 'result': 'draw'}
    return {'game_over': False, 'result': ''}

if __name__ == "__main__":
    print("--- Chess AI Backend Started ---")
    print("WSL2 Mode: Server is running at http://localhost:8000")
    print("Please open the URL above in your Windows browser.")
    print("--------------------------------")
    
    # mode=None prevents Eel from trying to open a native browser window
    eel.start('index.html', mode=None, host='localhost', port=8000)
