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

    def enable_kingside_castle(self, playernum):
        self.kingside_rights |= 1 << playernum

    def enable_queenside_castle(self, playernum):
        self.queenside_rights |= 1 << playernum

    def set_from_string(self, string: str):
        # sets the castling rights from standard FEN string
        if 'K' in string:
            self.enable_kingside_castle(0)
        else:
            self.disable_kingside_castle(0)
        if 'Q' in string:
            self.enable_queenside_castle(0)
        else:
            self.disable_queenside_castle(0)
        if 'k' in string:
            self.enable_kingside_castle(1)
        else:
            self.disable_kingside_castle(1)
        if 'q' in string:
            self.enable_queenside_castle(1)
        else:
            self.disable_queenside_castle(1)

class PositionProperties:
    def __init__(self, zobrist_key: int = 0, move_played: Optional[Move] = None, promote_from: Optional[str] = None, castling_rights: CastleRights = CastleRights(), ep_square: Optional[int] = None, captured_piece: Optional[Tuple[int, str]] = None, prev_properties: Optional['PositionProperties'] = None):
        self.zobrist_key = zobrist_key # 64 bit integer representing the zobrist key of the position
        self.move_played = move_played # Move object for the most recent move
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



# testing 

# def print_castle_rights(castle_rights: CastleRights):
#     print('Information for white')
#     print('Kingside:', castle_rights.can_player_castle_kingside(0))
#     print('Queenside:', castle_rights.can_player_castle_queenside(0))
#     print('Can Castle:', castle_rights.can_player_castle(0))
#     print('Did Castle:', castle_rights.did_player_castle(0))

#     print('Information for black')
#     print('Kingside:', castle_rights.can_player_castle_kingside(1))
#     print('Queenside:', castle_rights.can_player_castle_queenside(1))
#     print('Can Castle:', castle_rights.can_player_castle(1))
#     print('Did Castle:', castle_rights.did_player_castle(1))

# def correct_from_str(string):
#     answers = []
#     if 'K' in string:
#         answers.append(True)
#     else:
#         answers.append(False)
#     if 'Q' in string:
#         answers.append(True)
#     else:
#         answers.append(False)
#     if 'k' in string:
#         answers.append(True)
#     else:
#         answers.append(False)
#     if 'q' in string:
#         answers.append(True)
#     else:
#         answers.append(False)
#     return answers

# def answers_from_cr(castle_rights):
#     answers = []
#     answers.append(castle_rights.can_player_castle_kingside(0))
#     answers.append(castle_rights.can_player_castle_queenside(0))
#     answers.append(castle_rights.can_player_castle_kingside(1))
#     answers.append(castle_rights.can_player_castle_queenside(1))
#     return answers

# passed_count = 0
# for string in ['KQkq', 'Kkq', 'KQk', 'Kk', 'KQq', 'Kq', 'KQ', 'K', 'Qkq', 'Qk', 'Qq', 'Q', 'kq', 'k', 'q', '', '-']:
#     cr = CastleRights()
#     cr.set_from_string(string)

#     print('TESTING:', string)
#     if answers_from_cr(cr) == correct_from_str(string):
#         print('PASSED')
#         passed_count += 1
#     else:
#         print('FAILED')
#     print('Correct:', correct_from_str(string))
#     print('Answers:', answers_from_cr(cr))
# print('Passed', passed_count, 'out of 17')
