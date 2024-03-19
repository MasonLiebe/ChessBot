from bitboard import Bitboard
from move import *

class Piece:
    def __init__(self, player_num, char_rep, piece_type, bitboard):
        self.player_num = player_num
        self.char_rep = char_rep
        self.piece_type = piece_type
        self.bitboard = bitboard
    
    # Below are methods to create a blank piece of a certain type
    @classmethod
    def blank_custom(cls, player_num, char_rep):
        return cls(player_num, char_rep, char_rep, Bitboard.zero())
    
    @classmethod
    def blank_pawn(cls, player_num):
        return cls(player_num, 'p', PieceType.Pawn, Bitboard.zero())
    
    @classmethod
    def blank_knight(cls, player_num):
        return cls(player_num, 'n', PieceType.Knight, Bitboard.zero())
    
    @classmethod
    def blank_king(cls, player_num):
        return cls(player_num, 'k', PieceType.King, Bitboard.zero())
    
    @classmethod
    def blank_rook(cls, player_num):
        return cls(player_num, 'r', PieceType.Rook, Bitboard.zero())
    
    @classmethod
    def blank_bishop(cls, player_num):
        return cls(player_num, 'b', PieceType.Bishop, Bitboard.zero())
    
    @classmethod
    def blank_queen(cls, player_num):
        return cls(player_num, 'q', PieceType.Queen, Bitboard.zero())