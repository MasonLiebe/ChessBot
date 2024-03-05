# Generalized game class to handle custom chess games
from custom_pieces import Piece, Pawn, Rook, Knight, Bishop, Queen, King, Empty, enPassant

class CustomGame():

    CHAR_TO_PIECE = {
    'p': lambda position: Pawn('b', position),
    'r': lambda position: Rook('b', position),
    'n': lambda position: Knight('b', position),
    'b': lambda position: Bishop('b', position),
    'q': lambda position: Queen('b', position),
    'k': lambda position: King('b', position),
    'P': lambda position: Pawn('w', position),
    'R': lambda position: Rook('w', position),
    'N': lambda position: Knight('w', position),
    'B': lambda position: Bishop('w', position),
    'Q': lambda position: Queen('w', position),
    'K': lambda position: King('w', position),
    '·': lambda position: Empty(position),
    'x': lambda position: enPassant('b', position),
    'X': lambda position: enPassant('w', position)
}

    PIECE_NAME_TO_CHAR = {
        'Pawn': 'p',
        'Rook': 'r',
        'Knight': 'n',
        'Bishop': 'b',
        'Queen': 'q',
        'King': 'k',
        'Empty': '·',
        'enPassant': 'x'
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
            self.board = [[self.CHAR_TO_PIECE[piece]((i, j)) for j, piece in enumerate(row)] for i, row in enumerate(starting_board)]
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
        # TODO: Implement this function
        return 'normal'

    def execute_move(self, start, end):
        # executes a move from start to end and updates the board
        # get the piece at start
        piece = self.board[start[0]][start[1]]

        if piece.color != self.turn:
            print("It is not {}'s turn to move".format(piece.color))
            return False

        # get the legal moves for the piece at start
        legal_moves = piece.get_legal_moves(self)
        print('legal moves found: ', legal_moves)

        # don't allow the move if the end is not in the legal moves
        if end not in legal_moves:
            print("The move from {} to {} is not legal".format(start, end))
            return False
        
        # if the move is legal, execute it
        piece.move(self, end)

        # update the game information
        self.turn = 'w' if self.turn == 'b' else 'b'
        self.move_count += 1
        self.game_state = self.get_game_state()

        return True

    # BELOW IS FOR TESTING AND DEBUGGING
    def print_board(self):
        # prints the board
        for row in self.board:
            for piece in row:
                if piece.color == 'w':
                    print(self.PIECE_NAME_TO_CHAR[piece.__class__.__name__].upper(), end=' ')
                else:
                    print(self.PIECE_NAME_TO_CHAR[piece.__class__.__name__], end=' ')
            print()
        

# test_game1 = CustomGame(8, 8, starting_board = ['rnbqkbnr',
#                                                 'pppppppp', 
#                                                 '········', 
#                                                 '········', 
#                                                 '········', 
#                                                 '········', 
#                                                 'PPPPPPPP',
#                                                 'RNBQKBNR'])

# test_game1.print_board()

# # play a game taking in a move as a start and end position

# while True:
#     start = input("Enter the start position: ")
#     end = input("Enter the end position: ")
#     start = (int(start[0]), int(start[1]))
#     end = (int(end[0]), int(end[1]))
#     test_game1.execute_move(start, end)
#     test_game1.print_board()