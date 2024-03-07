# Generalized game class to handle custom chess games
from custom_pieces import Piece, Pawn, Rook, Knight, Bishop, Queen, King, Empty, enPassant
from copy import deepcopy

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
    
    def __init__(self, rows, cols, turn = 'w', self_capture=False, duck_chess=False, king_capture = False, starting_board=None, castle_rights = "KQkq", full_move_counter = 0, half_move_counter = 0, move_history = [], capture_history = []):
        self.rows = rows # number of rows on the board
        self.cols = cols # number of columns on the board
        self.turn = turn # current player whose turn it is, 'w' or 'b'
        self.self_capture = self_capture # True if self-capture is allowed, False otherwise
        self.king_capture = king_capture
        self.duck_chess = duck_chess
        self.move_history = move_history # list of moves made in the game as ((orgin),(dest)) tuples.
        self.state_history = capture_history # list of boards before each move
        if starting_board: # if a starting board is provided, use it, otherwise create an empty board
            self.board_string_list = starting_board
            self.board = [[self.CHAR_TO_PIECE[piece]((i, j)) for j, piece in enumerate(row)] for i, row in enumerate(starting_board)]
            # find the king locations
            for row in self.board:
                for piece in row:
                    if isinstance(piece, King) and piece.color == 'w':
                        self.white_king = piece
                    elif isinstance(piece, King) and piece.color == 'b':
                        self.black_king = piece
        else:
            self.board_string_list = ["·" * self.cols for _ in range(self.rows)]
            self.board = [[Empty((i ,j)) for j in range(self.cols)] for i in range(self.rows)]
            # set the kings in the middle of the board in the back rank
            self.white_king = King('w', (self.rows - 1, self.cols // 2))
            self.black_king = King('b', (0, self.cols // 2))
            self.board[self.rows - 1][self.cols // 2] = self.white_king
            self.board[0][self.cols // 2] = self.black_king

        self.board_history = [] # list of boards at each move
        self.board_history.append(deepcopy(self.board))

        self.game_over = False # True if the game is over, False otherwise
        self.winner = None # winner of the game, 'w', 'b', or 'd'
        self.move_history = [] # list of moves made in the game as e1e2, e7e5, etc.
        self.move_count = 0 # number of moves made in the game
        self.game_state = 'normal'
        self.game_state = self.get_game_state(self.turn) # current game state as a string, 'normal' 'check', 'checkmate', etc.
        self.full_move_counter = full_move_counter # full move counter for the game
        self.half_move_counter = half_move_counter # half move counter for the game
        self.castle_rights = castle_rights # string representing the castle rights of the game
        self.castle_rooks = self.get_castle_rooks()
        self.castle_rights_history = [castle_rights] # list of castle rights at each move
        
    # Game state evaluation

    def get_game_state(self, color_to_move):
        # returns the current game state as a string, 'normal' 'check', 'checkmate', etc.
        # iterate through the board to find king
        if self.is_check(color_to_move):
            self.game_state = "check"
            if self.is_stalemate(color_to_move):
                return 'checkmate'
            return 'check'
        if self.is_stalemate(color_to_move):
            return 'stalemate'
        return 'normal'

    def is_check(self, color_to_move):
        # returns True if the color is in check, False otherwise
        king = self.white_king if color_to_move == 'w' else self.black_king
        return self.square_is_attacked(king.position, 'w' if color_to_move == 'b' else 'b')
    
    def is_stalemate(self, color_to_move):
        # returns True if the color is in stalemate, False otherwise
        for row in self.board:
            for piece in row:
                if piece.color == color_to_move:
                    if len(piece.get_legal_moves(self)) != 0:
                        print(piece.__class__.__name__, piece.position, "can move")
                        print(piece.get_legal_moves(self))
                        return False
        return True
    
    # Game movement handlers
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
        
        self.move_history.append((start, end))
        self.board_history.append(deepcopy(self.board))
        self.castle_rights_history.append(deepcopy(self.castle_rights))
        
        # if the move is legal, execute it
        piece.move(self, end)

        # update the game information
        self.turn = 'w' if self.turn == 'b' else 'b'
        self.move_count += 1
        self.game_state = self.get_game_state(self.turn)

        print('game state is now: ', self.game_state)

        return True
    
    
    def undo_move(self):
        # undoes the last move made in the game
        if len(self.move_history) == 0:
            return False
        # get last move from move history
        self.board = self.board_history.pop()
        self.castle_rights = self.castle_rights_history.pop()

        # update the game information
        self.turn = 'w' if self.turn == 'b' else 'b'
        self.move_count -= 1
        self.game_state = self.get_game_state(self.turn)

    def reset_game(self):
        # undo moves until the game is reset
        while len(self.move_history) > 0:
            self.undo_move()


    # game state checking functions
    
    def square_is_attacked(self, position, color):
        # returns True if the square at position is attacked by the color, False otherwise
        for row in self.board:
            for piece in row:
                if piece.color == color:
                    if position in piece.get_vision(self):
                        print(position, " is attacked by ", piece.__class__.__name__)
                        return True
        return False

    def get_castle_rooks(self):
        output = {}
        for c in self.castle_rights:
            if c == 'K':
                # look for rightmost rook in bottom rank
                for i in range(self.cols-1, -1, -1):
                    if isinstance(self.board[self.rows - 1][i], Rook) and self.board[self.rows - 1][i].color == 'w':
                        output['K'] = (self.rows - 1, i)
                        break
                    elif isinstance(self.board[self.rows - 1][i], King):  # no rook found
                        break
            elif c == 'Q':
                # look for leftmost rook in bottom rank
                for i in range(self.cols):
                    if isinstance(self.board[self.rows - 1][i], Rook) and self.board[self.rows - 1][i].color == 'w':
                        output['Q'] = (self.rows -1 , i)
                        break
                    elif isinstance(self.board[self.rows(-1)][i], King):
                        break
            elif c == 'k':
                # look for rightmost rook in top rank
                for i in range(self.cols-1, -1, -1):
                    if isinstance(self.board[0][i], Rook) and self.board[0][i].color == 'b':
                        output['k'] = (0, i)
                        break
                    elif isinstance(self.board[0][i], King):
                        break

            elif c == 'q':
                # look for leftmost rook in top rank
                for i in range(self.cols):
                    if isinstance(self.board[0][i], Rook) and self.board[0][i].color == 'b':
                        output['q'] = (0, i)
                        break
                    elif isinstance(self.board[0][i], King):
                        break
            else:
                continue
        return output


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