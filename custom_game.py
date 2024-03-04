# Generalized game class to handle custom chess games
from custom_pieces import Piece, Pawn, Rook, Knight, Bishop, Queen, King, Empty, enPassant

class CustomGame():

    CHAR_TO_PIECE = {
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
        '·': Empty(),
        'x': enPassant('w'),
        'X': enPassant('b')
    }

    PIECE_NAME_TO_CHAR = {
        'Pawn': 'p',
        'Rook': 'r',
        'Knight': 'n',
        'Bishop': 'b',
        'Queen': 'q',
        'King': 'k',
        'Empty': '·'
    }
    
    def __init__(self, rows, cols, turn = 'w', self_capture=False, duck_chess=False, king_capture = False, starting_board=None, castle_rights = "KQkq", full_move_counter = 0, half_move_counter = 0, move_history = []):
        self.rows = rows # number of rows on the board
        self.cols = cols # number of columns on the board
        self.turn = turn # current player whose turn it is, 'w' or 'b'
        self.self_capture = self_capture # True if self-capture is allowed, False otherwise
        self.king_capture = king_capture
        self.duck_chess = duck_chess
        if starting_board: # if a starting board is provided, use it, otherwise create an empty board
            self.board_string_list = starting_board
            self.board = [[CustomGame.CHAR_TO_PIECE[piece] for piece in row] for row in starting_board]
        else:
            self.board_string_list = ["·" * self.cols for _ in range(self.rows)]
            self.board = [[Empty((i ,j)) for j in range(self.cols)] for i in range(self.rows)]
        self.castle_rights = castle_rights # string representing the castle rights of the game
        self.game_over = False # True if the game is over, False otherwise
        self.winner = None # winner of the game, 'w', 'b', or 'd'
        self.move_history = [] # list of moves made in the game as e1e2, e7e5, etc.
        self.move_count = 0 # number of moves made in the game
        self.game_state = self.get_game_state() # current game state as a string, 'normal' 'check', 'checkmate', etc.
        self.full_move_counter = full_move_counter # full move counter for the game
        self.half_move_counter = half_move_counter # half move counter for the game
        self.move_history = move_history # list of moves made in the game as e1e2, e7e5, etc.

    def get_game_state(self):
        # returns the current game state as a string, 'normal' 'check', 'checkmate', etc.
        return self.game_state
    
    def get_board(self):
        # returns the current board as a list of lists of Piece objects
        return self.board

    # BELOW IS FOR TESTING AND DEBUGGING
    def print_board(self):
        # prints the board
        for row in self.board_string_list:
            print(row)
        

test_game1 = CustomGame(8, 8, starting_board = ['rnbqkbnr',
                                                'pppppppp', 
                                                '········', 
                                                '········', 
                                                '········', 
                                                '········', 
                                                'PPPPPPPP',
                                                'RNBQKBNR'])

test_game1.print_board()

# play a game taking in a move as a start and end tuple then updating the board