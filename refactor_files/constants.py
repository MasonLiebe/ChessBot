# Contains the constants used throughout the program
DEFAULT_WIDTH = 8
DEFAULT_HEIGHT = 8

# CHARACTER TO PIECE LOOKUPS
CHAR_TO_PIECE = {'p': 'Pawn',
             'z': 'NPawn', # New Pawn that can move 2 squares
             'r': 'Rook',
             'n': 'Knight',
             'b': 'Bishop',
             'q': 'Queen',
             'k': 'King',
             'x': 'Enpassant',
             'a': 'Custom1',
             'c': 'Custom2',
             'd': 'Custom3',
             'e': 'Custom4',
             'f': 'Custom5',
             'g': 'Custom6',
             '.': 'Empty',
}

# Int to Piece Lookups
INT_TO_PIECE = {0: 'Empty',
                1: 'King',
                2: 'Queen',
                3: 'Rook',
                4: 'Bishop',
                5: 'Knight',
                6: 'Pawn',
                7: 'NPawn',
                8: 'Custom1',
                9: 'Custom2',
                10: 'Custom3',
                11: 'Custom4',
                12: 'Custom5',
                13: 'Custom6',
}

PIECE_TO_INT = {'Empty': 0,
                'King': 1,
                'Queen': 2,
                'Rook': 3,
                'Bishop': 4,
                'Knight': 5,
                'Pawn': 6,
                'NPawn': 7,
                'Custom1': 8,
                'Custom2': 9,
                'Custom3': 10,
                'Custom4': 11,
                'Custom5': 12,
                'Custom6': 13,
}


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
STARTING_FEN = 'rnbqkbnr/zzzzzzzz/8/8/8/8/ZZZZZZZZZ/RNBQKBNR w KQkq - 0 1'
E4E5_FEN = 'rnbqkbnr/zzzz1zzz/8/4p3/4P3/8/ZZZZ1ZZZ/RNBQKBNR w KQkq e6 0 1'
JUST_KINGS_FEN = '8/8/8/8/8/8/8/4k3 w - - 0 1'
NINEBYNINE_FEN = 'rnbqkqbnr/zzzzzzzzz/9/9/9/9/9/ZZZZZZZZZ/RNBQKQBNR w KQkq - 0 1'
NINEBYEIGHT_FEN = 'rnbqkqbnr/zzzzzzzzz/9/9/9/9/ZZZZZZZZZ/RNBQKQBNR w KQkq - 0 1'
FOURBYFIVE_FEN = 'rqkr/zzzz/4/ZZZZ/RQKR w - - 0 1'

# Board Information
FILE_TO_INT = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9, 'k': 10, 'l': 11, 'm': 12, 'n': 13, 'o': 14, 'p': 15}

