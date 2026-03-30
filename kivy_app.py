from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.properties import StringProperty, ObjectProperty, NumericProperty, ListProperty, DictProperty
from kivy.clock import Clock
import chess
import random
import os
from model.alpha_beta import alpha_beta_best_move
from model.mcts import mcts

# Setup Absolute Paths for Assets
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE_DIR, 'UI', 'assets', 'chess_img')

# Exact colors from style.css
COLORS = {
    'bg_dark': [49/255, 46/255, 43/255, 1],
    'bg_light': [38/255, 36/255, 33/255, 1],
    'accent': [129/255, 182/255, 76/255, 1],
    'square_light': [235/255, 236/255, 208/255, 1],
    'square_dark': [119/255, 149/255, 86/255, 1],
    'highlight': [1, 1, 0, 0.4],
    'last_move': [245/255, 246/255, 130/255, 1],
    'text_main': [1, 1, 1, 1],
    'text_muted': [186/255, 186/255, 186/255, 1],
}

FEN_TO_IMAGE = {
    'P': os.path.join(IMG_DIR, 'white_pawn.png'),
    'R': os.path.join(IMG_DIR, 'white_rook.png'),
    'N': os.path.join(IMG_DIR, 'white_knight.png'),
    'B': os.path.join(IMG_DIR, 'white_bishop.png'),
    'Q': os.path.join(IMG_DIR, 'white_queen.png'),
    'K': os.path.join(IMG_DIR, 'white_king.png'),
    'p': os.path.join(IMG_DIR, 'black_pawn.png'),
    'r': os.path.join(IMG_DIR, 'black_rook.png'),
    'n': os.path.join(IMG_DIR, 'black_knight.png'),
    'b': os.path.join(IMG_DIR, 'black_bishop.png'),
    'q': os.path.join(IMG_DIR, 'black_queen.png'),
    'k': os.path.join(IMG_DIR, 'black_king.png'),
}

KV = f"""
<SquareWidget>:
    canvas.before:
        Color:
            rgba: self.background_color
        Rectangle:
            pos: self.pos
            size: self.size
        Color:
            rgba: {COLORS['highlight']} if self.is_selected else (0, 0, 0, 0)
        Rectangle:
            pos: self.pos
            size: self.size
        Color:
            rgba: {COLORS['last_move']} if self.is_last_move else (0, 0, 0, 0)
        Rectangle:
            pos: self.pos
            size: self.size
    
    canvas.after:
        # Piece
        Color:
            rgba: (1, 1, 1, 1) if self.piece_img else (1, 1, 1, 0)
        Rectangle:
            source: self.piece_img
            pos: self.x + self.width * 0.075, self.y + self.height * 0.075
            size: self.width * 0.85, self.height * 0.85
        
        # Valid Move Hint (Dot)
        Color:
            rgba: (0, 0, 0, 0.2) if self.is_valid_move else (0, 0, 0, 0)
        Ellipse:
            pos: self.x + self.width * 0.375, self.y + self.height * 0.375
            size: self.width * 0.25, self.height * 0.25

<MenuScreen>:
    canvas.before:
        Color:
            rgba: {COLORS['bg_dark']}
        Rectangle:
            pos: self.pos
            size: self.size
    BoxLayout:
        orientation: 'vertical'
        padding: 50
        spacing: 20
        Label:
            text: "Chess AI Intro"
            font_size: '32sp'
            bold: True
            color: {COLORS['text_main']}
            size_hint_y: 0.3
        Button:
            text: "Start Game"
            background_normal: ''
            background_color: {COLORS['accent']}
            color: (1, 1, 1, 1)
            size_hint_y: 0.2
            on_release: root.manager.current = 'settings'
        Label:
            text: "Explore AI algorithms in Chess"
            color: {COLORS['text_muted']}
            font_size: '14sp'

<SettingsScreen>:
    canvas.before:
        Color:
            rgba: {COLORS['bg_dark']}
        Rectangle:
            pos: self.pos
            size: self.size
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 15
        Label:
            text: "AI Settings"
            font_size: '24sp'
            color: {COLORS['text_main']}
            size_hint_y: 0.1

        BoxLayout:
            orientation: 'horizontal'
            spacing: 10
            size_hint_y: 0.1
            Button:
                text: "Random"
                background_color: {COLORS['accent']} if app.bot_type == 'random' else [0.2, 0.2, 0.2, 1]
                on_release: app.bot_type = 'random'
            Button:
                text: "AlphaBeta"
                background_color: {COLORS['accent']} if app.bot_type == 'alphabeta' else [0.2, 0.2, 0.2, 1]
                on_release: app.bot_type = 'alphabeta'
            Button:
                text: "MCTS"
                background_color: {COLORS['accent']} if app.bot_type == 'mcts' else [0.2, 0.2, 0.2, 1]
                on_release: app.bot_type = 'mcts'

        # Alpha-Beta Settings
        BoxLayout:
            orientation: 'vertical'
            size_hint_y: 0.4 if app.bot_type == 'alphabeta' else 0
            opacity: 1 if app.bot_type == 'alphabeta' else 0
            disabled: app.bot_type != 'alphabeta'
            Label:
                text: f"Search Depth: {{int(depth_slider.value)}}"
                color: {COLORS['text_muted']}
            Slider:
                id: depth_slider
                min: 1
                max: 10
                value: 3
                step: 1
            Label:
                text: f"Quiescence Depth: {{int(q_depth_slider.value)}}"
                color: {COLORS['text_muted']}
            Slider:
                id: q_depth_slider
                min: 0
                max: 10
                value: 4
                step: 1
            
        # MCTS Settings
        BoxLayout:
            orientation: 'vertical'
            size_hint_y: 0.4 if app.bot_type == 'mcts' else 0
            opacity: 1 if app.bot_type == 'mcts' else 0
            disabled: app.bot_type != 'mcts'
            Label:
                text: f"Iterations: {{int(iter_slider.value)}}"
                color: {COLORS['text_muted']}
            Slider:
                id: iter_slider
                min: 100
                max: 10000
                value: 1000
                step: 100
            Label:
                text: f"Rollout Depth: {{int(rollout_slider.value)}}"
                color: {COLORS['text_muted']}
            Slider:
                id: rollout_slider
                min: 1
                max: 100
                value: 30
                step: 1

        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: 0.1
            spacing: 10
            Button:
                text: "Back"
                on_release: root.manager.current = 'menu'
            Button:
                text: "Battle!"
                background_normal: ''
                background_color: {COLORS['accent']}
                on_release: 
                    app.depth = int(depth_slider.value)
                    app.q_depth = int(q_depth_slider.value)
                    app.iterations = int(iter_slider.value)
                    app.rollout_depth = int(rollout_slider.value)
                    root.manager.current = 'game'

<GameScreen>:
    canvas.before:
        Color:
            rgba: {COLORS['bg_dark']}
        Rectangle:
            pos: self.pos
            size: self.size
    BoxLayout:
        orientation: 'horizontal'
        padding: 10
        spacing: 10

        # Chess Board Area
        BoxLayout:
            orientation: 'vertical'
            size_hint_x: 0.7
            Widget: # Spacer
                size_hint_y: 0.05
            BoxLayout:
                orientation: 'horizontal'
                BoxLayout:
                    id: ranks_labels
                    orientation: 'vertical'
                    size_hint_x: 0.05
                ChessBoardWidget:
                    id: board_ui
                Widget:
                    size_hint_x: 0.05
            BoxLayout:
                id: files_labels
                orientation: 'horizontal'
                size_hint_y: 0.05
                padding: [0.05 * root.width, 0, 0, 0] # Offset for ranks

        # Sidebar Area
        BoxLayout:
            orientation: 'vertical'
            size_hint_x: 0.3
            canvas.before:
                Color:
                    rgba: {COLORS['bg_light']}
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [8,]
            padding: 15
            Label:
                text: "Live Match"
                font_size: '20sp'
                bold: True
                size_hint_y: 0.1
            ScrollView:
                Label:
                    id: move_history
                    text: ""
                    valign: 'top'
                    text_size: self.width, None
                    size_hint_y: None
                    height: self.texture_size[1]
            Button:
                text: "Resign"
                size_hint_y: 0.1
                background_normal: ''
                background_color: [1, 0.25, 0.18, 1]
                on_release: app.reset_game()
"""

class SquareWidget(Button):
    coords = ObjectProperty(None)
    piece = StringProperty('')
    piece_img = StringProperty('')
    is_selected = NumericProperty(0)
    is_last_move = NumericProperty(0)
    is_valid_move = NumericProperty(0)
    background_color = ListProperty([1, 1, 1, 1])

    def on_piece(self, instance, value):
        self.piece_img = FEN_TO_IMAGE.get(value, '')

class ChessBoardWidget(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 8
        self.squares = {}
        self.last_move = (None, None)

    def build_board(self, board_logic):
        self.clear_widgets()
        for r in range(7, -1, -1):
            for c in range(8):
                color = COLORS['square_light'] if (r + c) % 2 == 1 else COLORS['square_dark']
                sq_widget = SquareWidget(coords=(r, c), background_color=color, background_normal='')
                sq_widget.bind(on_release=self.handle_press)
                self.add_widget(sq_widget)
                self.squares[(r, c)] = sq_widget
        self.update_board(board_logic)

    def update_board(self, board_logic):
        for r in range(8):
            for c in range(8):
                piece = board_logic.piece_at(chess.square(c, r))
                self.squares[(r, c)].piece = piece.symbol() if piece else ''
                self.squares[(r, c)].is_selected = 0
                self.squares[(r, c)].is_last_move = 1 if chess.square(c, r) in self.last_move else 0
                self.squares[(r, c)].is_valid_move = 0

    def handle_press(self, instance):
        r, c = instance.coords
        sq = chess.square(c, r)
        app = App.get_running_app()
        app.on_square_clicked(sq)

class MenuScreen(Screen): pass
class SettingsScreen(Screen): pass
class GameScreen(Screen):
    def on_enter(self):
        self.ids.board_ui.build_board(App.get_running_app().board)
        self.setup_labels()

    def setup_labels(self):
        self.ids.ranks_labels.clear_widgets()
        for i in range(8, 0, -1):
            self.ids.ranks_labels.add_widget(Label(text=str(i), color=COLORS['text_muted']))
        
        self.ids.files_labels.clear_widgets()
        for c in 'abcdefgh':
            self.ids.files_labels.add_widget(Label(text=c, color=COLORS['text_muted']))

class ChessApp(App):
    bot_type = StringProperty('alphabeta')
    depth = NumericProperty(3)
    q_depth = NumericProperty(4)
    iterations = NumericProperty(10000)
    rollout_depth = NumericProperty(30)
    
    def build(self):
        self.board = chess.Board()
        self.selected_square = None
        Builder.load_string(KV)
        self.sm = ScreenManager()
        self.sm.add_widget(MenuScreen(name='menu'))
        self.sm.add_widget(SettingsScreen(name='settings'))
        self.sm.add_widget(GameScreen(name='game'))
        return self.sm

    def on_square_clicked(self, sq):
        game_screen = self.sm.get_screen('game')
        board_ui = game_screen.ids.board_ui

        if self.selected_square is None:
            piece = self.board.piece_at(sq)
            if piece and piece.color == self.board.turn:
                self.selected_square = sq
                # Highlight selection
                r, c = chess.square_rank(sq), chess.square_file(sq)
                board_ui.squares[(r, c)].is_selected = 1
                # Highlight valid moves
                for move in self.board.legal_moves:
                    if move.from_square == sq:
                        tr, tc = chess.square_rank(move.to_square), chess.square_file(move.to_square)
                        board_ui.squares[(tr, tc)].is_valid_move = 1
        else:
            # Check if clicking the same square to deselect
            if sq == self.selected_square:
                self.selected_square = None
                board_ui.update_board(self.board)
                return

            # Check for a different piece of the same color
            piece = self.board.piece_at(sq)
            if piece and piece.color == self.board.turn:
                self.selected_square = None
                board_ui.update_board(self.board)
                self.on_square_clicked(sq)
                return

            # Try to move
            move = chess.Move(self.selected_square, sq)
            # Handle promotion
            piece = self.board.piece_at(self.selected_square)
            if piece and piece.piece_type == chess.PAWN:
                if chess.square_rank(sq) in [0, 7]:
                    move.promotion = chess.QUEEN

            if move in self.board.legal_moves:
                self.execute_move(move)
                Clock.schedule_once(self.bot_move, 0.5)
            else:
                self.selected_square = None
                board_ui.update_board(self.board)

    def execute_move(self, move):
        san = self.board.san(move)
        self.board.push(move)
        game_screen = self.sm.get_screen('game')
        game_screen.ids.board_ui.last_move = (move.from_square, move.to_square)
        game_screen.ids.board_ui.update_board(self.board)
        
        if len(self.board.move_stack) % 2 == 1:
            move_num = (len(self.board.move_stack) // 2) + 1
            game_screen.ids.move_history.text += f"{move_num}. {san} "
        else:
            game_screen.ids.move_history.text += f"{san}\n"
        
        self.selected_square = None

    def bot_move(self, dt):
        if self.board.is_game_over(): return
        if self.bot_type == 'random':
            move = random.choice(list(self.board.legal_moves))
        elif self.bot_type == 'alphabeta':
            move = alpha_beta_best_move(self.board, self.depth, self.q_depth)
        else:
            move = mcts(self.board, iterations=self.iterations, rollout_depth=self.rollout_depth)
        if move:
            self.execute_move(move)

    def reset_game(self):
        self.board = chess.Board()
        self.sm.get_screen('game').ids.board_ui.last_move = (None, None)
        self.sm.get_screen('game').ids.board_ui.update_board(self.board)
        self.sm.get_screen('game').ids.move_history.text = ""
        self.sm.current = 'menu'

if __name__ == '__main__':
    ChessApp().run()
