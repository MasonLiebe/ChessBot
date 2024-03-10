from bitboard import Bitboard

PieceType = {
    "Pawn": 0,
    "Knight": 1,
    "King": 2,
    "Rook": 3,
    "Bishop": 4,
    "Queen": 5,
    "Custom1": 6,
    "Custom2": 7,
    "Custom3": 8,
    "Custom4": 9,
    "Custom5": 10,
    "Custom6": 11
}

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
    

