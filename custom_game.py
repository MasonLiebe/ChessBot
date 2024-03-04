# Generalized game class to handle custom chess games
from custom_pieces import Piece, Pawn, Rook, Knight, Bishop, Queen, King, Empty

class CustomGame():

    PIECE_MAP = {
        'p': Pawn('b'),
        'r': Rook('b'),
        'n': Knight('b'),
        'b': Bishop('b'),
        'q': Queen('b'),
        'k': King('b'),
        'P': Pawn('w'),
        'R': Rook('w'),
        'N': Knight('w'),
        'B': Bishop('w'),
        'Q': Queen('w'),
        'K': King('w'),
        '.': Empty()
    }


    
    def __init__(self, rows, cols, turn = 'w', self_capture=False, duck_chess=False, starting_board=None, castle_rights = "KQkq", king_capture = False, full_move_counter = 0, half_move_counter = 0, en_passant = None, move_history = []):
        self.rows = rows # number of rows on the board
        self.cols = cols # number of columns on the board
        self.turn = turn # current player whose turn it is, 'w' or 'b'
        self.self_capture = self_capture # True if self-capture is allowed, False otherwise
        self.duck_chess = duck_chess
        if starting_board:
            self.board = starting_board
        else:
            self.board = [[Empty(i ,j) for j in range(self.cols)] for i in range(self.rows)]
        self.game_over = False
        self.winner = None
        self.move_history = []
        self.move_count = 0
        self.game_state = None
        self.game_state = self.get_game_state()
    
    def get_game_state(self):
        # returns the current game state
        return self.game_state
    
    def is_traversable(self, position):
        # parameters: position as a (row, col) tuple
        # returns True if the space can be landed on and passed through, False otherwise
        return self.board[position[0]][position[1]].traversable

    def is_takeable(self, position, color):
        # parameters: position as a (row, col) tuple, color as a string
        # returns True if the space can be landed on and taken, False otherwise
        return self.board[position[0]][position[1]].color != color
    
    def is_pinned(self, position, color):
        # parameters: position as a (row, col) tuple, color as a string
        # returns direction of pin if the piece is pinned, False otherwise
        pass

    def print_board(self):
        # prints the board
        for row in self.board:
            print([str(piece) for piece in row])

test_game = CustomGame(8, 8)
test_game.print_board()