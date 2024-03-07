from bitboard.src.position.castle_rights import CastleRights
from bitboard.src.types.mod import PieceType
from bitboard.src.types.chess_move import Move

class PositionProperties:
    def __init__(self):
        self.zobrist_key = 0
        self.move_played = None
        self.promote_from = None
        self.castling_rights = CastleRights()
        self.ep_square = None
        self.captured_piece = None
        self.prev_properties = None

    @staticmethod
    def default():
        return PositionProperties()

    def get_prev(self):
        return self.prev_properties
