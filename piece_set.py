from bitboard import Bitboard
from piece import Piece

class PieceSet:
    def __init__(self, player_num):
        self.occupied = Bitboard.zero()
        self.king = Piece.blank_king(player_num)
        self.queen = Piece.blank_queen(player_num)
        self.bishop = Piece.blank_bishop(player_num)
        self.knight = Piece.blank_knight(player_num)
        self.rook = Piece.blank_rook(player_num)
        self.pawn = Piece.blank_pawn(player_num)
        self.custom = []
        self.player_num = player_num

    @classmethod
    def new(cls, player_num):
        return cls(player_num)

    def piece_at(self, index):
        if self.pawn.bitboard.bit(index):
            return self.pawn
        elif self.rook.bitboard.bit(index):
            return self.rook
        elif self.bishop.bitboard.bit(index):
            return self.bishop
        elif self.knight.bitboard.bit(index):
            return self.knight
        elif self.queen.bitboard.bit(index):
            return self.queen
        elif self.king.bitboard.bit(index):
            return self.king
        else:
            for p in self.custom:
                if p.bitboard.bit(index):
                    return p
        return None

    def get_piece_refs(self):
        return_vec = [
            self.king,
            self.queen,
            self.bishop,
            self.knight,
            self.rook,
            self.pawn,
            *self.custom
        ]
        return return_vec

    def update_occupied(self):
        self.occupied = Bitboard.zero()
        self.occupied |= self.king.bitboard
        self.occupied |= self.queen.bitboard
        self.occupied |= self.bishop.bitboard
        self.occupied |= self.knight.bitboard
        self.occupied |= self.rook.bitboard
        self.occupied |= self.pawn.bitboard
        for p in self.custom:
            self.occupied |= p.bitboard