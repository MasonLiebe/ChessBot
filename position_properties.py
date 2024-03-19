from typing import Optional, Tuple
from move import Move, PieceType

class CastleRights:
    def __init__(self):
        self.kingside_rights = 255
        self.queenside_rights = 255
        self.castled = 0

    def can_player_castle_kingside(self, playernum: int) -> bool:
        return ((self.kingside_rights >> playernum) & 1) != 0

    def can_player_castle_queenside(self, playernum: int) -> bool:
        return ((self.queenside_rights >> playernum) & 1) != 0

    def can_player_castle(self, playernum: int) -> bool:
        return self.can_player_castle_kingside(playernum) or self.can_player_castle_queenside(playernum)

    def did_player_castle(self, playernum: int) -> bool:
        return ((self.castled >> playernum) & 1) != 0

    def set_player_castled(self, playernum: int):
        self.castled |= 1 << playernum

    def disable_kingside_castle(self, playernum: int):
        self.kingside_rights &= ~(1 << playernum)

    def disable_queenside_castle(self, playernum: int):
        self.queenside_rights &= ~(1 << playernum)


class PositionProperties:
    def __init__(self):
        self.zobrist_key: int = 0
        self.move_played: Optional[Move] = None
        self.promote_from: Optional[PieceType] = None
        self.castling_rights: CastleRights = CastleRights()
        self.ep_square: Optional[int] = None
        self.captured_piece: Optional[Tuple[int, PieceType]] = None
        self.prev_properties: Optional[PositionProperties] = None

    @classmethod
    def default(cls) -> 'PositionProperties':
        return cls()

    def get_prev(self) -> Optional['PositionProperties']:
        return self.prev_properties