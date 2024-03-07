from enum import Enum
from typing import Optional
from bitboard.src.types.bitboard import from_index
from bitboard.src.rankfile import to_rank_file


class MoveType(Enum):
    Quiet = 0
    Capture = 1
    QueensideCastle = 2
    KingsideCastle = 3
    Promotion = 4
    PromotionCapture = 5
    Null = 6

class Move:
    def __init__(self, from_square: int, to_square: int, target_loc: Optional[int], move_type: MoveType, promo: Optional[str]):
        self.move_data = (
            from_square
            | (to_square << 8)
            | ((target_loc << 16) if target_loc is not None else 0)
            | (move_type.value << 24)
        )
        self.promo = promo

    @staticmethod
    def null():
        return Move(0, 0, None, MoveType.Null, None)

    def get_from(self) -> int:
        return self.move_data & 255

    def get_to(self) -> int:
        return (self.move_data >> 8) & 255

    def get_is_capture(self) -> bool:
        return ((self.move_data >> 24) & 1) != 0

    def get_move_type(self) -> MoveType:
        return MoveType((self.move_data >> 24) & 7)

    def get_promotion_char(self) -> Optional[str]:
        return self.promo

    def get_target(self) -> int:
        return (self.move_data >> 16) & 255

    def __str__(self):
        x1, y1 = from_index(self.get_from())
        x2, y2 = from_index(self.get_to())
        return f"(from: {to_rank_file(x1, y1)}, to: {to_rank_file(x2, y2)})"