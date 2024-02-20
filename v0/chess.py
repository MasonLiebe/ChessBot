from main import Board
from v1.pieces import Piece, Pawn, Knight, Bishop, Rook, Queen, King, CustomPiece1, CustomPiece2, CustomPiece3, Duck

class ChessGame():
    # Custom Chess Game
    # Game representation Structure:
    # Board is a rows x cols 2d ArrayList of integers
    # Black's back rank is row 0, the board is viewed from white's perspective 
    # that is - [0,0] is black's queenside rook
    # pieces take on the following values:

    #  0 - empty space
    #  1 - white pawn
    #  2 - black pawn
    #  3 - white knight
    #  4 - black knight
    #  5 - white bishop
    #  6 - black bishop
    #  7 - white rook
    #  8 - black rook
    #  9 - white queen
    # 10 - black queen
    # 11 - white king
    # 12 - black king
    # 13 - white custom piece 1 
    # 14 - black custom piece 1
    # 15 - white custom piece 2
    # 16 - black custom piece 2
    # 17 - white custom piece 3
    # 18 - black custom piece 3
    # 19 - duck

    def __init__(self, rows = 8, cols = 8, board = None, selfCapture = False, duck = False, castling = True, white = True):
        # Set board configuration values - dimensions, turn and piece layout
        self.rows = rows
        self.cols = cols
        if board == None:
            self.board = [[0]*cols for _ in range(rows)]  # blank board
        else:
            self.board = board
        
        # Set game state values
        self.white = white
        self.enPassant = None
        
        # Set rule values
        self.duck = duck  # Allows a custom game to be duck chess
        self.selfCapture = selfCapture # Allows players to self-capture in custom game
        if castling:
            self.whiteKingCastle = True
            self.blackKingCastle = True
            self.whiteQueenCastle = True
            self.blackQueenCastle = True
        else:
            self.whiteKingCastle = False
            self.blackKingCastle = False
            self.whiteQueenCastle = False
            self.blackQueenCastle = False

        # Check game-end and check states
        self.check = self.inCheck()
        self.gameOver = self.gameEnd()
    
    # Getters and setters for the board
    def get_board(self):
        return self.board()
    
    def set_board(self, board):
        self.rows = len(board)
        self.cols = len(board[0])
        self.board = board
        return
    
    # Sets a particular square if possible
    def set_square(self, pieceType, row, col, overwrite = False):
        # Sets piece value at given location, testing if placement is valid
        # pieceType - integer representing the pice
        # row - row that the piece will be placed
        # col - col that the piece will be placed
        # overwrite - True if you are simply overwriting a square, false if it's an in-game placement
        # returns - True if placement succeeded, False otherwise.

        if self.can_place(pieceType, row, col, overwrite):
            self.board[row][col] = pieceType
            return True
        return False
    
    # Tests whether placement on a square is possible
    def can_place(self, pieceType, row, col, overwrite = False):
        # returns True if a piece or blank square can be placed at a given spot
        if pieceType == 1 and row == 0:  # white pawn in final rank
            return False
        if pieceType == 2 and col == self.rows - 1:  # black pawn in final rank
            return False
        if overwrite or self.selfCapture or pieceType == 0:
            return True
        else:
            if pieceType == 19:  # placing a duck, only valid in empty square
                if self.board[row][col] == 0:
                    return True
            elif self.board[row][col] != 0 and pieceType % 2 == self.board[row][col] % 2:
                # pieces are same color, invalid move
                return False
            else:
                # pieces are different colors or target square is empty, valid move
                return True

        
    def initialize_standard_game(self, selfCapture = False, duck = False):
        # Initializes the standard board configuration
        self.rows = 8
        self.cols = 8
        self.board = [[8, 4, 6, 10, 12, 6, 4, 8],
                      [2, 2, 2,  2,  2, 2, 2, 2],
                      [0, 0, 0,  0,  0, 0, 0, 0],
                      [0, 0, 0,  0,  0, 0, 0, 0],
                      [0, 0, 0,  0,  0, 0, 0, 0],
                      [0, 0, 0,  0,  0, 0, 0, 0],
                      [1, 1, 1,  1,  1, 1, 1, 1],
                      [7, 2, 5,  9, 11, 5, 3, 7]]
        self.duck = duck
        self.selfCapture = selfCapture
    
    def execute_move(self, row1, col1, row2, col2):
        # Takes in a LEGAL move, in the form of a row and column, then executes it
        pass

    def get_legal_moves(self, row, col, enPassant = None):
        # Given a piece location, and the board state, computes the legal moves of that piece
        pieceType = self.board[row][col] # integer representing piece type
        legalMoves = set()

        # make sure it's the right color given whose turn it is
        if pieceType in range(1, 19):
            if (pieceType % 2 == 1) == self.white:
                return legalMoves
        
        match pieceType:
            case 1: # white pawn
                # check if pawn has occured based on rank
                if row == self.rows - 2:
                    if self.can_place(pieceType, )

                # check if enPassant or capture available
            case 2: # black pawn
                print ('hi')
            case 3, 4: # knight
                print ('hi')
            case 5, 6, 9, 10: # bishop or queen - can do bishop moves
                print ('hi')
            case 7, 8, 9, 10: # rook or queen - can do rook moves 
                print ('hi')
            case 11, 12: # king
                print('hi')
            case 19:
                for i in range(self.rows):
                    for j in range(self.cols):
                        if self.board[i][j] == 0:
                            legalMoves.add((i, j))

        return legalMoves


    def inCheck():
        # Determines whether the current player is in Check
        pass

    def gameEnd():
        # Determines if a game-end state is reached
        # Returns 0, 1, 2, for No, Draw, Loss respectively for the current player
        pass

    def get_successors():
        # Computes and returns the possible moves as move, successor tuples
        pass

    def compute_bot_move(self):
        # Processes current board state and returns 
        pass
