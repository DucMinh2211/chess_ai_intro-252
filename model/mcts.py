import chess
import math
import random

# ===================== EVALUATION =====================

PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000
}

PAWN_TABLE = [
    0,0,0,0,0,0,0,0,
    50,50,50,50,50,50,50,50,
    10,10,20,30,30,20,10,10,
    5,5,10,25,25,10,5,5,
    0,0,0,20,20,0,0,0,
    5,-5,-10,0,0,-10,-5,5,
    5,10,10,-20,-20,10,10,5,
    0,0,0,0,0,0,0,0
]

KNIGHT_TABLE = [
    -50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,0,0,0,0,-20,-40,
    -30,0,10,15,15,10,0,-30,
    -30,5,15,20,20,15,5,-30,
    -30,0,15,20,20,15,0,-30,
    -30,5,10,15,15,10,5,-30,
    -40,-20,0,5,5,0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50
]

BISHOP_TABLE = [
    -20,-10,-10,-10,-10,-10,-10,-20,
    -10,0,0,0,0,0,0,-10,
    -10,0,5,10,10,5,0,-10,
    -10,5,5,10,10,5,5,-10,
    -10,0,10,10,10,10,0,-10,
    -10,10,10,10,10,10,10,-10,
    -10,5,0,0,0,0,5,-10,
    -20,-10,-10,-10,-10,-10,-10,-20
]

ROOK_TABLE = [
    0,0,0,0,0,0,0,0,
    5,10,10,10,10,10,10,5,
    -5,0,0,0,0,0,0,-5,
    -5,0,0,0,0,0,0,-5,
    -5,0,0,0,0,0,0,-5,
    -5,0,0,0,0,0,0,-5,
    -5,0,0,0,0,0,0,-5,
    0,0,0,5,5,0,0,0
]

QUEEN_TABLE = [
    -20,-10,-10,-5,-5,-10,-10,-20,
    -10,0,0,0,0,0,0,-10,
    -10,0,5,5,5,5,0,-10,
    -5,0,5,5,5,5,0,-5,
    0,0,5,5,5,5,0,-5,
    -10,5,5,5,5,5,0,-10,
    -10,0,5,0,0,0,0,-10,
    -20,-10,-10,-5,-5,-10,-10,-20
]

KING_MID = [
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -20,-30,-30,-40,-40,-30,-30,-20,
    -10,-20,-20,-20,-20,-20,-20,-10,
    20,20,0,0,0,0,20,20,
    20,30,10,0,0,10,30,20
]

KING_END = [
    -50,-40,-30,-20,-20,-30,-40,-50,
    -30,-20,-10,0,0,-10,-20,-30,
    -30,-10,20,30,30,20,-10,-30,
    -30,-10,30,40,40,30,-10,-30,
    -30,-10,30,40,40,30,-10,-30,
    -30,-10,20,30,30,20,-10,-30,
    -30,-30,0,0,0,0,-30,-30,
    -50,-30,-30,-30,-30,-30,-30,-50
]

PST = {
    chess.PAWN: PAWN_TABLE,
    chess.KNIGHT: KNIGHT_TABLE,
    chess.BISHOP: BISHOP_TABLE,
    chess.ROOK: ROOK_TABLE,
    chess.QUEEN: QUEEN_TABLE
}

def is_endgame(board):
    return len(board.pieces(chess.QUEEN, True)) == 0 and len(board.pieces(chess.QUEEN, False)) == 0

def evaluate(board):
    if board.is_checkmate():
        return -99999 if board.turn else 99999
    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    score = 0
    endgame = is_endgame(board)

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if not piece:
            continue

        value = PIECE_VALUES[piece.piece_type]

        if piece.piece_type == chess.KING:
            table = KING_END if endgame else KING_MID
        else:
            table = PST.get(piece.piece_type, [0]*64)

        idx = square if piece.color else chess.square_mirror(square)
        value += table[idx]

        score += value if piece.color else -value

    return score


# ===================== MCTS =====================

C = 1.4
ROLLOUT_DEPTH = 100

class Node:
    def __init__(self, board, parent=None):
        self.board = board
        self.parent = parent
        self.children = []
        self.visits = 0
        self.value = 0


def uct(node):
    if node.visits == 0:
        return float('inf')

    exploit = node.value / node.visits
    explore = C * math.sqrt(math.log(node.parent.visits) / node.visits)

    heuristic = evaluate(node.board) * 0.01

    return exploit + explore + heuristic


def select(node):
    while node.children:
        node = max(node.children, key=uct)
    return node


def expand(node):
    moves = list(node.board.legal_moves)
    for move in moves:
        b = node.board.copy()
        b.push(move)
        node.children.append(Node(b, node))
    return random.choice(node.children) if node.children else node


def heuristic_move(board):
    moves = list(board.legal_moves)

    captures = [m for m in moves if board.is_capture(m)]
    if captures:
        return random.choice(captures)

    checks = []
    for m in moves:
        board.push(m)
        if board.is_check():
            checks.append(m)
        board.pop()

    if checks:
        return random.choice(checks)

    return random.choice(moves)


def simulate(board):
    depth = 0

    while not board.is_game_over():
        if depth >= ROLLOUT_DEPTH:
            return evaluate(board)

        move = heuristic_move(board)
        board.push(move)
        depth += 1

    if board.is_checkmate():
        return -99999 if board.turn else 99999

    return 0


def backpropagate(node, result):
    while node:
        node.visits += 1
        node.value += result
        node = node.parent


def mcts(board, iterations=1000):
    root = Node(board)

    for _ in range(iterations):
        node = select(root)
        node = expand(node)
        result = simulate(node.board.copy())
        backpropagate(node, result)

    if not root.children:
        return None

    best = max(root.children, key=lambda n: n.visits)
    return best.board.peek()


