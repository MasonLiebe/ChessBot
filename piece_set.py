from bitboard import Bitboard
from piece import Piece

class PieceSet:
    def __init__(self, player_num):
        self.occupied = Bitboard(0)
        self.king = Piece.blank_king(player_num)
        self.queen = Piece.blank_queen(player_num)
        self.bishop = Piece.blank_bishop(player_num)
        self.knight = Piece.blank_knight(player_num)
        self.rook = Piece.blank_rook(player_num)
        self.pawn = Piece.blank_pawn(player_num)
        self.custom1 = Piece.blank_custom1(player_num)
        self.custom2 = Piece.blank_custom2(player_num)
        self.custom3 = Piece.blank_custom3(player_num)
        self.custom4 = Piece.blank_custom4(player_num)
        self.custom5 = Piece.blank_custom5(player_num)
        self.custom6 = Piece.blank_custom6(player_num)
        self.player_num = player_num

    def piece_at(self, index):
        if self.king.bitboard.bit(index):
            return self.king
        elif self.queen.bitboard.bit(index):
            return self.queen
        elif self.bishop.bitboard.bit(index):
            return self.bishop
        elif self.knight.bitboard.bit(index):
            return self.knight
        elif self.rook.bitboard.bit(index):
            return self.rook
        elif self.pawn.bitboard.bit(index):
            return self.pawn
        elif self.custom1.bitboard.bit(index):
            return self.custom1
        elif self.custom2.bitboard.bit(index):
            return self.custom2
        elif self.custom3.bitboard.bit(index):
            return self.custom3
        elif self.custom4.bitboard.bit(index):
            return self.custom4
        elif self.custom5.bitboard.bit(index):
            return self.custom5
        elif self.custom6.bitboard.bit(index):
            return self.custom6
        else:
            return None

    def get_piece_refs(self):
        return_vec = [self.king, self.queen, self.bishop, self.knight, self.rook, self.pawn, self.custom1, self.custom2, self.custom3, self.custom4, self.custom5, self.custom6]
        return return_vec

    def update_occupied(self):
        self.occupied.zero()
        self.occupied |= self.king.bitboard
        self.occupied |= self.queen.bitboard
        self.occupied |= self.bishop.bitboard
        self.occupied |= self.knight.bitboard
        self.occupied |= self.rook.bitboard
        self.occupied |= self.pawn.bitboard
        self.occupied |= self.custom1.bitboard
        self.occupied |= self.custom2.bitboard
        self.occupied |= self.custom3.bitboard
        self.occupied |= self.custom4.bitboard
        self.occupied |= self.custom5.bitboard
        self.occupied |= self.custom6.bitboard


