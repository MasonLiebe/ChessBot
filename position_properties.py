# This code manages the properties of a position
from moves import Move
from typing import Optional, Tuple

class CastleRights:
    """
    Castling rights for each player
    CastleRights.0 -- kingside rights
    CastleRights.1 -- Queenside rights
    CastleRights.2 -- 1 if the player actually castled
    Where each bit in the u8 represents the castling right for the player at that index
    Ex if CastleRights.0 == 1 then the 0th player can castle kingside
    """
    def __init__(self):
        self.kingside_rights = 7
        self.queenside_rights = 7
        self.has_castled = 0

    def can_player_castle_kingside(self, playernum):
        return (self.kingside_rights >> playernum) & 1 != 0

    def can_player_castle_queenside(self, playernum):
        return (self.queenside_rights >> playernum) & 1 != 0

    def can_player_castle(self, playernum):
        return self.can_player_castle_kingside(playernum) or self.can_player_castle_queenside(playernum)

    def did_player_castle(self, playernum):
        return (self.has_castled >> playernum) & 1 != 0

    def set_player_castled(self, playernum):
        self.has_castled |= 1 << playernum

    def disable_kingside_castle(self, playernum):
        self.kingside_rights &= ~(1 << playernum)

    def disable_queenside_castle(self, playernum):
        self.queenside_rights &= ~(1 << playernum)

    def set_from_string(self, string: str):
        # sets the castling rights from standard FEN string
        for c in string:
            if c == 'K':
                self.disable_kingside_castle(0)
            elif c == 'Q':
                self.disable_queenside_castle(0)
            elif c == 'k':
                self.disable_kingside_castle(1)
            elif c == 'q':
                self.disable_queenside_castle(1)


class PositionProperties:
    def __init__(self, zobrist_key: int = 0, move_played: Optional[Move] = None, promote_from: Optional[str] = None, castling_rights: CastleRights = CastleRights(), ep_square: Optional[int] = None, captured_piece: Optional[Tuple[int, str]] = None, prev_properties: Optional['PositionProperties'] = None):
        self.zobrist_key = zobrist_key # 64 bit integer representing the zobrist key of the position
        self.move_played = move_played # Move object
        self.promote_from = promote_from # string representation of the piece type promoted from 'Pawn'
        self.castling_rights = castling_rights # CastleRights object
        self.ep_square = ep_square # integer representing the index of the en passant square
        self.captured_piece = captured_piece # string representation of the piece type captuere 'Pawn'
        self.prev_properties = prev_properties # PositionProperties object

    @staticmethod
    def default():
        return PositionProperties()

    def get_prev(self) -> Optional['PositionProperties']:
        return self.prev_properties
