import eel
from model.alpha_beta import *
from model.mcts import *
import chess
import random
import time

# Global board to keep track of move history (CRITICAL for threefold repetition)
game_board = chess.Board()
move_times = []

eel.init('UI')

def sync_board(fen: str):
    """Syncs the global board with UI while preserving history if possible."""
    global game_board
    # Only reset or jump if the position is significantly different
    if game_board.fen().split(' ')[0] != fen.split(' ')[0]:
        if fen == chess.STARTING_FEN:
            game_board = chess.Board()
            alpha_beta_clear_transposition_table() # Reset AI memory for new game
        else:
            game_board = chess.Board(fen)

@eel.expose
def get_legal_moves(fen: str):
    global move_times, game_board
    sync_board(fen)
    
    if fen == chess.STARTING_FEN:
        move_times = []
        
    moves_dict = {}
    for move in game_board.legal_moves:
        from_sq = chess.square_name(move.from_square)
        to_sq = chess.square_name(move.to_square)
        if from_sq not in moves_dict:
            moves_dict[from_sq] = []
        moves_dict[from_sq].append(to_sq)
    return moves_dict

@eel.expose
def apply_move(fen: str, from_sq: str, to_sq: str, promotion=None):
    global game_board
    sync_board(fen)
    
    move_uci = from_sq + to_sq
    if promotion:
        move_uci += promotion
    else:
        # Auto-promote to queen
        from_square = chess.parse_square(from_sq)
        to_square = chess.parse_square(to_sq)
        piece = game_board.piece_at(from_square)
        if piece and piece.piece_type == chess.PAWN:
            if chess.square_rank(to_square) in [0, 7]:
                move_uci += 'q'
    
    move = chess.Move.from_uci(move_uci)
    if move in game_board.legal_moves:
        san_move = game_board.san(move)
        game_board.push(move)
        print(f"Move played: {san_move}")
        return {'fen': game_board.fen(), 'san': san_move}
    return {'fen': fen, 'san': ''}

@eel.expose
def get_bot_move(fen: str, bot_type: str, params: dict):
    global move_times, game_board
    sync_board(fen)
    
    print(f"AI ({bot_type}) is thinking...", end=" ", flush=True)
    start_time = time.time()
    
    if bot_type == 'random':
        moves = list(game_board.legal_moves)
        move = random.choice(moves)
    elif bot_type == 'alphabeta':
        depth = int(params.get('depth', 3))
        q_depth = int(params.get('q_depth', 4))
        move = alpha_beta_best_move(game_board, depth, q_depth)
    elif bot_type == 'mcts':
        iters = int(params.get('iterations', 10000))
        rollout_depth = int(params.get('rollout_depth', 30))
        move = mcts(game_board, iterations=iters, rollout_depth=rollout_depth)
    else:
        raise Exception('Unknown Bot type')

    duration = time.time() - start_time
    move_times.append(duration)

    if not move: 
        raise Exception('Bot could not find a move')
    
    print(f"Done ({duration:.5f}s). Selected: {game_board.san(move)}")
    return {
        'from': chess.square_name(move.from_square),
        'to': chess.square_name(move.to_square),
        'promotion': chess.piece_symbol(move.promotion) if move.promotion else None
    }

@eel.expose
def log_session_stats():
    global move_times
    if move_times:
        avg_time = sum(move_times) / len(move_times)
        print(f"\n--- AI Session Stats ---")
        print(f"Total AI moves: {len(move_times)}")
        print(f"Average time per move: {avg_time:.5f}s")
        print(f"------------------------\n")
        move_times = []

@eel.expose
def get_game_status(fen: str):
    global game_board
    sync_board(fen)
    
    if game_board.is_checkmate():
        res = 'black' if game_board.turn == chess.WHITE else 'white'
        log_session_stats()
        return {'game_over': True, 'result': res, 'reason': 'Checkmate'}
    
    # Check for draw claims (Repetition, 50-move rule)
    outcome = game_board.outcome(claim_draw=True)
    if outcome:
        reason = outcome.termination.name.replace('_', ' ').title()
        log_session_stats()
        return {'game_over': True, 'result': 'draw', 'reason': reason}
        
    return {'game_over': False, 'result': '', 'reason': ''}

if __name__ == "__main__":
    url = "http://localhost:8000"
    print("--- Chess AI Backend Started ---")
    print(f"Web interface: {url}")
    try:
        eel.start('index.html', size=(1000, 700), shutdown_delay=1.0)
    except (OSError, Exception) as e:
        if isinstance(e, SystemExit): raise
        print(f"Native browser launch skipped. Running in server mode...")
        eel.start('index.html', mode=None, host='localhost', port=8000, shutdown_delay=1.0)
