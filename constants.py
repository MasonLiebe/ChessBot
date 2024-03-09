# Contains the constants used throughout the program

# CHARACTER TO PIECE LOOKUPS
CHAR_TO_PIECE = {'p': 'new_pawn', # can double move
             'z': 'old_pawn', # cannot double move
             'r': 'rook',
             'n': 'knight',
             'b': 'bishop',
             'q': 'queen',
             'k': 'king',
             'x': 'enpassant',
             'a': 'custom1',
             'c': 'custom2',
             'd': 'custom3',
             'e': 'custom4',
             'f': 'custom5',
             'g': 'custom6',
             '.': 'empty',}

CHAR_TO_FILE_NAME = {   
                        'p': '/assets/pieces/black_pawn.png',
                        'z': '/assets/pieces/black_pawn.png',
                        'r': '/assets/pieces/black_rook.png',
                        'n': '/assets/pieces/black_knight.png',
                        'b': '/assets/pieces/black_bishop.png',
                        'q': '/assets/pieces/black_queen.png',
                        'k': '/assets/pieces/black_king.png',
                        'x': '/assets/pieces/black_enpassant.png',
                        'a': '/assets/pieces/black_custom1.png',
                        'c': '/assets/pieces/black_custom2.png',
                        'd': '/assets/pieces/black_custom3.png',
                        'e': '/assets/pieces/black_custom4.png',
                        'f': '/assets/pieces/black_custom5.png',
                        'g': '/assets/pieces/black_custom6.png',
                        'P': '/assets/pieces/white_pawn.png',
                        'Z': '/assets/pieces/white_pawn.png',
                        'R': '/assets/pieces/white_rook.png',
                        'N': '/assets/pieces/white_knight.png',
                        'B': '/assets/pieces/white_bishop.png',
                        'Q': '/assets/pieces/white_queen.png',
                        'K': '/assets/pieces/white_king.png',
                        'X': '/assets/pieces/white_enpassant.png',
                        'A': '/assets/pieces/white_custom1.png',
                        'C': '/assets/pieces/white_custom2.png',
                        'D': '/assets/pieces/white_custom3.png',
                        'E': '/assets/pieces/white_custom4.png',
                        'F': '/assets/pieces/white_custom5.png',
                        'G': '/assets/pieces/white_custom6.png'
                    }

# FENS
STARTING_FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
E4E5_FEN = 'rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1'
D4D5_FEN = 'rnbqkbnr/pppppppp/8/8/3pP3/8/PPP2PPP/RNBQKBNR w KQkq - 0 1'
D4E5_FEN = 'rnbqkbnr/pppppppp/8/8/3P4/8/PPP2PPP/RNBQKBNR b KQkq - 0 1'
JUST_KINGS_FEN = '8/8/8/8/8/8/8/4k3 w - - 0 1'
NINEBYNINE_FEN = 'rnbqkqbnr/ppppppppp/9/9/9/9/9/PPPPPPPPP/RNBQKQBNR w KQkq - 0 1'
NINEBYEIGHT_FEN = 'rnbqkqbnr/ppppppppp/9/9/9/9/PPPPPPPPP/RNBQKQBNR w KQkq - 0 1'
FOURBYFIVE_FEN = 'rqkr/pppp/4/PPPP/RQKR w - - 0 1'

# Board Information
FILE_TO_INT = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9, 'k': 10, 'l': 11, 'm': 12, 'n': 13, 'o': 14, 'p': 15}
