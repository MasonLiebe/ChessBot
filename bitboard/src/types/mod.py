from enum import Enum, unique
from bitboard.src.types.bitboard import *
from bitboard.src.types.chess_move import *

@unique
class PieceType(Enum):
    King = 'k'
    Queen = 'q'
    Rook = 'r'
    Bishop = 'b'
    Knight = 'n'
    Pawn = 'p'
    Custom = None  # Placeholder, actual value set in __init__

    def __init__(self, value):
        if self is PieceType.Custom:
            self._value_ = value

    @classmethod
    def from_char(cls, c):
        c = c.lower()
        if c == 'k':
            return cls.King
        elif c == 'q':
            return cls.Queen
        elif c == 'r':
            return cls.Rook
        elif c == 'b':
            return cls.Bishop
        elif c == 'n':
            return cls.Knight
        elif c == 'p':
            return cls.Pawn
        else:
            return cls.Custom(c)

class Dimensions:
    def __init__(self, width, height):
        self.width = width
        self.height = height
