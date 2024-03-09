from enum import Enum, auto
from bitboard import Bitboard

# this is weird because it's a bit of a retrofit, I will convert to dictionary at some point
class PieceType(Enum):
    King = auto()
    Queen = auto()
    Rook = auto()
    Bishop = auto()
    Knight = auto()
    Pawn = auto()
    Custom1 = auto()
    Custom2 = auto()
    Custom3 = auto()
    Custom4 = auto()
    Custom5 = auto()
    Custom6 = auto()

    @staticmethod
    def from_char(c):
        c = c.lower()
        if c == 'k':
            return PieceType.King
        elif c == 'q':
            return PieceType.Queen
        elif c == 'r':
            return PieceType.Rook
        elif c == 'b':
            return PieceType.Bishop
        elif c == 'n':
            return PieceType.Knight
        elif c == 'p':
            return PieceType.Pawn
        elif c == 'a':
            return PieceType.Custom1
        elif c == 'c':
            return PieceType.Custom2
        elif c == 'd':
            return PieceType.Custom3
        elif c == 'e':
            return PieceType.Custom4
        elif c == 'f':
            return PieceType.Custom5
        elif c == 'g':
            return PieceType.Custom6
        else:
            raise ValueError(f'Invalid piece character: {c}')
    
class Piece:
    def __init__(self, player_num, char_rep, piece_type, bitboard):
        self.player_num = player_num # 0 for white, 1 for black
        self.char_rep = char_rep # character representation of the piece
        self.piece_type = piece_type # type of piece as a PieceType Object
        self.bitboard = bitboard # bitboard representing the locations of the piece

    # The methods below are used to create blank pieces of each type
    @classmethod
    def blank_pawn(cls, player_num):
        return cls(player_num, 'p', "Pawn", Bitboard(0))

    @classmethod
    def blank_knight(cls, player_num):
        return cls(player_num, 'n', "Knight", Bitboard(0))

    @classmethod
    def blank_king(cls, player_num):
        return cls(player_num, 'k', "King", Bitboard(0))

    @classmethod
    def blank_rook(cls, player_num):
        return cls(player_num, 'r', "Rook", Bitboard(0))

    @classmethod
    def blank_bishop(cls, player_num):
        return cls(player_num, 'b', "Bishop", Bitboard(0))

    @classmethod
    def blank_queen(cls, player_num):
        return cls(player_num, 'q', "Queen", Bitboard(0))
    
    @classmethod
    def blank_custom1(cls, player_num):
        return cls(player_num, 'a', "Custom1", Bitboard(0))
    
    @classmethod
    def blank_custom2(cls, player_num):
        return cls(player_num, 'c', "Custom2", Bitboard(0))
    
    @classmethod
    def blank_custom3(cls, player_num):
        return cls(player_num, 'd', "Custom3", Bitboard(0))
    
    @classmethod
    def blank_custom4(cls, player_num):
        return cls(player_num, 'e', "Custom4", Bitboard(0))
    
    @classmethod
    def blank_custom5(cls, player_num):
        return cls(player_num, 'f', "Custom5", Bitboard(0))
    
    @classmethod
    def blank_custom6(cls, player_num):
        return cls(player_num, 'g', "Custom6", Bitboard(0))
    

