from bitboard import Bitboard
from piece import Piece

class PieceSet:
    def __init__(self, player_num):
        self.occupied = Bitboard(0)
        self.King = Piece.blank_king(player_num)
        self.Queen = Piece.blank_queen(player_num)
        self.Bishop = Piece.blank_bishop(player_num)
        self.Knight = Piece.blank_knight(player_num)
        self.Rook = Piece.blank_rook(player_num)
        self.Pawn = Piece.blank_pawn(player_num)
        self.Custom1 = Piece.blank_custom1(player_num)
        self.Custom2 = Piece.blank_custom2(player_num)
        self.Custom3 = Piece.blank_custom3(player_num)
        self.Custom4 = Piece.blank_custom4(player_num)
        self.Custom5 = Piece.blank_custom5(player_num)
        self.Custom6 = Piece.blank_custom6(player_num)
        self.player_num = player_num

    def piece_at(self, index):
        if self.King.bitboard.bit(index):
            return self.King
        elif self.Queen.bitboard.bit(index):
            return self.Queen
        elif self.Bishop.Bitboard.bit(index):
            return self.Bishop
        elif self.Knight.bitboard.bit(index):
            return self.Knight
        elif self.Rook.bitboard.bit(index):
            return self.Rook
        elif self.Pawn.bitboard.bit(index):
            return self.Pawn
        elif self.Custom1.bitboard.bit(index):
            return self.Custom1
        elif self.Custom2.bitboard.bit(index):
            return self.Custom2
        elif self.Custom3.bitboard.bit(index):
            return self.Custom3
        elif self.Custom4.bitboard.bit(index):
            return self.Custom4
        elif self.Custom5.bitboard.bit(index):
            return self.Custom5
        elif self.Custom6.bitboard.bit(index):
            return self.Custom6
        else:
            return None

    def get_piece_refs(self):
        return_vec = [self.King, self.Queen, self.Bishop, self.Knight, self.Rook, self.Pawn, self.Custom1, self.Custom2, self.Custom3, self.Custom4, self.Custom5, self.Custom6]
        return return_vec

    def update_occupied(self):
        self.occupied.zero()
        self.occupied |= self.King.bitboard
        self.occupied |= self.Queen.bitboard
        self.occupied |= self.Bishop.bitboard
        self.occupied |= self.Knight.bitboard
        self.occupied |= self.Rook.bitboard
        self.occupied |= self.Pawn.bitboard
        self.occupied |= self.Custom1.bitboard
        self.occupied |= self.Custom2.bitboard
        self.occupied |= self.Custom3.bitboard
        self.occupied |= self.Custom4.bitboard
        self.occupied |= self.Custom5.bitboard
        self.occupied |= self.Custom6.bitboard