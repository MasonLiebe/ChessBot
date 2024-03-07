from bitboard.src.types.bitboard import Bitboard, from_index, to_index
from bitboard.src.position.piece import Piece

class Bitboard:
    def __init__(self):
        self.bits = 0

    @staticmethod
    def zero():
        return Bitboard()

    def bit(self, index):
        return (self.bits >> index) & 1

    def __ior__(self, other):
        self.bits |= other.bits
        return self


class Piece:
    def __init__(self, player_num, piece_type):
        self.bitboard = Bitboard()
        self.player_num = player_num
        self.piece_type = piece_type

    @staticmethod
    def blank_piece(player_num, piece_type):
        return Piece(player_num, piece_type)


class PieceSet:
    def __init__(self, player_num):
        self.occupied = Bitboard.zero()
        self.king = Piece.blank_piece(player_num, 'king')
        self.queen = Piece.blank_piece(player_num, 'queen')
        self.bishop = Piece.blank_piece(player_num, 'bishop')
        self.knight = Piece.blank_piece(player_num, 'knight')
        self.rook = Piece.blank_piece(player_num, 'rook')
        self.pawn = Piece.blank_piece(player_num, 'pawn')
        self.custom = []
        self.player_num = player_num

    def piece_at(self, index):
        pieces = [self.king, self.queen, self.bishop, self.knight, self.rook, self.pawn] + self.custom
        for piece in pieces:
            if piece.bitboard.bit(index):
                return piece
        return None

    def get_piece_refs(self):
        return [self.king, self.queen, self.bishop, self.knight, self.rook, self.pawn] + self.custom

    def update_occupied(self):
        self.occupied = Bitboard.zero()
        for piece in self.get_piece_refs():
            self.occupied |= piece.bitboard


