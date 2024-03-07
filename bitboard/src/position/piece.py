from bitboard.src.types.mod import PieceType
from bitboard.src.types.bitboard import Bitboard

class Piece:
    def __init__(self, char_rep, player_num, piece_type, bitboard):
        self.char_rep = char_rep
        self.player_num = player_num
        self.piece_type = piece_type
        self.bitboard = bitboard

    @classmethod
    def blank_custom(cls, player_num, char_rep):
        return cls(char_rep, player_num, PieceType.Custom(char_rep), Bitboard.zero())

    @classmethod
    def blank_pawn(cls, player_num):
        return cls('p', player_num, PieceType.Pawn, Bitboard.zero())

    @classmethod
    def blank_knight(cls, player_num):
        return cls('n', player_num, PieceType.Knight, Bitboard.zero())

    @classmethod
    def blank_king(cls, player_num):
        return cls('k', player_num, PieceType.King, Bitboard.zero())

    @classmethod
    def blank_rook(cls, player_num):
        return cls('r', player_num, PieceType.Rook, Bitboard.zero())

    @classmethod
    def blank_bishop(cls, player_num):
        return cls('b', player_num, PieceType.Bishop, Bitboard.zero())

    @classmethod
    def blank_queen(cls, player_num):
        return cls('q', player_num, PieceType.Queen, Bitboard.zero())
