from bitboard import *
from constants import *
from enum import Enum

MoveType = {
    'Quiet': 0,
    'Capture': 1,
    'QueensideCastle': 2,
    'KingsideCastle': 3,
    'Promotion': 4,
    'PromotionCapture': 5,
    'Null': 6,
}

# MoveType = {
#     0: 'Quiet',
#     1: 'Capture',
#     2: 'QueensideCastle',
#     3: 'KingsideCastle',
#     4: 'Promotion',
#     5: 'PromotionCapture',
#     6: 'Null',
# }

class Move:
    '''
    Stores the move data in a single 32 bit integer
    0-7: from square
    8-15: to square
    16-23: target square
    24-26: move type
    27-31: promotion piece type
    '''
    def __init__(self, value, promo=None):
        self.value = value
        self.promo = promo
    
    @classmethod
    def new(cls, from_index, to_index, target_loc=None, move_type='Quiet', promo=None):
        value = (
            from_index |
            (to_index << 8) |
            (target_loc << 16 if target_loc is not None else 0) |
            (MoveType[move_type] << 24)
        )
        return cls(value, promo)
    
    @classmethod
    def null(cls):
        return cls.new(0, 0, None, 'Null', None)
    
    def get_from(self):
        return self.value & 255
    
    def get_to(self):
        return (self.value >> 8) & 255
    
    def get_is_capture(self):
        return ((self.value >> 24) & 1) != 0
    
    def get_move_type(self):
        move_type_value = (self.value >> 24) & 7
        for move_type, value in MoveType.items():
            if value == move_type_value:
                return move_type
        return 'Quiet'
    
    def get_promotion_char(self):
        return self.promo
    
    def get_target(self):
        return (self.value >> 16) & 255
    
    def __str__(self):
        x1, y1 = from_index(self.get_from())
        x2, y2 = from_index(self.get_to())
        return f"(from: {to_rank_file(x1, y1)}, to:{to_rank_file(x2, y2)})"
    
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.value == other.value and self.promo == other.promo
        return False

class PieceType(Enum):
    '''
    Enum representing the type of a piece
    '''
    King = 'k'
    Queen = 'q'
    Rook = 'r'
    Bishop = 'b'
    Knight = 'n'
    Pawn = 'p'
    Custom1 = 'a'
    Custom2 = 'c'
    Custom3 = 'd'
    Custom4 = 'e'
    Custom5 = 'f'
    Custom6 = 'g'
    
    @classmethod
    def from_char(cls, c):
        c = c.lower()
        if c in [piece_type.value for piece_type in cls]:
            return cls(c)
        else:
            return c

class Dimensions:
    '''
    class representing the dimensions of a board
    '''
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def __eq__(self, other):
        if isinstance(other, Dimensions):
            return self.width == other.width and self.height == other.height
        return False
    
    def __hash__(self):
        return hash((self.width, self.height))
    
    def __str__(self):
        return f"Dimensions(width={self.width}, height={self.height})"
    
    def __repr__(self):
        return self.__str__()