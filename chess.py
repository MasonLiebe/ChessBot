

class ChessGame():
    # Custom Chess Game
    # Game representation Structure:
    # Board is a rows x cols 2d ArrayList of integers
    # Black's back rank is rank 0, the board is viewed from white's perspective
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

    def __init__(self, rows = 8, cols = 8, board = None, selfCapture = False, duck = False, white = True):
        # Set board configuration values - dimensions, turn and piece layout
        self.rows = rows
        self.cols = cols
        if board == None:
            self.board = [[0]*cols for _ in range(rows)]  # blank board
        else:
            self.board = board
        
        # Set game state values
        self.white = white
        
        # Set rule values
        self.duck = duck  # Allows a custom game to be duck chess
        self.selfCapture = selfCapture # Allows players to self-capture in custom game

        # Check game-end and check states
        self.check = self.inCheck()
        self.gameEnd = self.gameEnd()
        
    
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


    def get_successors():
        # Computes and returns the possible moves as move, successor tuples
        pass

    def compute_bot_move():
        # Processes move 