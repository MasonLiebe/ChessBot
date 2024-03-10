# This file handles the valid move generation for each piece. It uses the bitboard representation of the board to generate the moves for each piece.

from enum import Enum
from typing import Optional, Tuple
from bitboard import Bitboard, from_index, to_index, to_rank_file

moveType = {
    "Quiet": 0,
    "Capture": 1,
    "QueensideCastle": 2,
    "KingsideCastle": 3,
    "Promotion": 4,
    "PromotionCapture": 5,
    "Null": 6
}

intToMoveType = {
    0: "Quiet",
    1: "Capture",
    2: "QueensideCastle",
    3: "KingsideCastle",
    4: "Promotion",
    5: "PromotionCapture",
    6: "Null"
}


class Move:
    # Stores the move data in a single 32 bit integer
    # 0-7: from square
    # 8-15: to square
    # 16-23: target square
    # 24-26: move type
    # 27-31: promotion type

    def __init__(self, from_square: int, to_square: int, target_loc: Optional[int], move_type: str, promo: Optional[str]):
        self.move_data = from_square | (to_square << 8) | (target_loc << 16 if target_loc is not None else 0) | (moveType[move_type] << 24)
        self.promo = promo

    @staticmethod
    def null():
        return Move(0, 0, None, 'Null', None)

    def get_from(self) -> int:
        return self.move_data & 255

    def get_to(self) -> int:
        return (self.move_data >> 8) & 255

    def get_is_capture(self) -> bool:
        return ((self.move_data >> 24) & 1) != 0

    def get_move_type(self) -> str:
        return intToMoveType[(self.move_data >> 24) & 7]

    def get_promotion_char(self) -> Optional[str]:
        return self.promo

    def get_target(self) -> int:
        return (self.move_data >> 16) & 255

    def __str__(self):
        x1, y1 = from_index(self.get_from())
        x2, y2 = from_index(self.get_to())
        return f"(from: {to_rank_file(x1, y1)}, to: {to_rank_file(x2, y2)})"


class MovementPatternExternal:
    def __init__(
        self,
        promotion_squares: Optional[list[Tuple[int, int]]] = None,
        promo_vals: Optional[list[str]] = None,
        attack_sliding_deltas: list[list[Tuple[int, int]]] = [],
        attack_jump_deltas: list[Tuple[int, int]] = [],
        attack_north: bool = False,
        attack_south: bool = False,
        attack_east: bool = False,
        attack_west: bool = False,
        attack_northeast: bool = False,
        attack_northwest: bool = False,
        attack_southeast: bool = False,
        attack_southwest: bool = False,
        translate_jump_deltas: list[Tuple[int, int]] = [],
        translate_sliding_deltas: list[list[Tuple[int, int]]] = [],
        translate_north: bool = False,
        translate_south: bool = False,
        translate_east: bool = False,
        translate_west: bool = False,
        translate_northeast: bool = False,
        translate_northwest: bool = False,
        translate_southeast: bool = False,
        translate_southwest: bool = False,
    ):
        self.promotion_squares = promotion_squares
        self.promo_vals = promo_vals
        self.attack_sliding_deltas = attack_sliding_deltas
        self.attack_jump_deltas = attack_jump_deltas
        self.attack_north = attack_north
        self.attack_south = attack_south
        self.attack_east = attack_east
        self.attack_west = attack_west
        self.attack_northeast = attack_northeast
        self.attack_northwest = attack_northwest
        self.attack_southeast = attack_southeast
        self.attack_southwest = attack_southwest
        self.translate_jump_deltas = translate_jump_deltas
        self.translate_sliding_deltas = translate_sliding_deltas
        self.translate_north = translate_north
        self.translate_south = translate_south
        self.translate_east = translate_east
        self.translate_west = translate_west
        self.translate_northeast = translate_northeast
        self.translate_northwest = translate_northwest
        self.translate_southeast = translate_southeast
        self.translate_southwest = translate_southwest

class MovementPattern:
    def __init__(
        self,
        promotion_squares: Optional[Bitboard] = None,
        promo_vals: Optional[list[str]] = None,
        attack_sliding_deltas: list[list[Tuple[int, int]]] = [],
        attack_jump_deltas: list[Tuple[int, int]] = [],
        attack_north: bool = False,
        attack_south: bool = False,
        attack_east: bool = False,
        attack_west: bool = False,
        attack_northeast: bool = False,
        attack_northwest: bool = False,
        attack_southeast: bool = False,
        attack_southwest: bool = False,
        translate_jump_deltas: list[Tuple[int, int]] = [],
        translate_sliding_deltas: list[list[Tuple[int, int]]] = [],
        translate_north: bool = False,
        translate_south: bool = False,
        translate_east: bool = False,
        translate_west: bool = False,
        translate_northeast: bool = False,
        translate_northwest: bool = False,
        translate_southeast: bool = False,
        translate_southwest: bool = False,
    ):
        self.promotion_squares = promotion_squares
        self.promo_vals = promo_vals
        self.attack_sliding_deltas = attack_sliding_deltas
        self.attack_jump_deltas = attack_jump_deltas
        self.attack_north = attack_north
        self.attack_south = attack_south
        self.attack_east = attack_east
        self.attack_west = attack_west
        self.attack_northeast = attack_northeast
        self.attack_northwest = attack_northwest
        self.attack_southeast = attack_southeast
        self.attack_southwest = attack_southwest
        self.translate_jump_deltas = translate_jump_deltas
        self.translate_sliding_deltas = translate_sliding_deltas
        self.translate_north = translate_north
        self.translate_south = translate_south
        self.translate_east = translate_east
        self.translate_west = translate_west
        self.translate_northeast = translate_northeast
        self.translate_northwest = translate_northwest
        self.translate_southeast = translate_southeast
        self.translate_southwest = translate_southwest

    def promotion_at(self, index: int) -> bool:
        if self.promotion_squares is not None:
            return self.promotion_squares.bit(index)
        return False

def external_mp_to_internal(mpe: MovementPatternExternal) -> MovementPattern:
    promotion_squares = None
    if mpe.promotion_squares is not None:
        bb = Bitboard(0)
        for x, y in mpe.promotion_squares:
            bb.set_bit(to_index(x, y), True)
        promotion_squares = bb
    return MovementPattern(
        promotion_squares=promotion_squares,
        promo_vals=mpe.promo_vals,
        attack_sliding_deltas=mpe.attack_sliding_deltas,
        attack_jump_deltas=mpe.attack_jump_deltas,
        attack_north=mpe.attack_north,
        attack_south=mpe.attack_south,
        attack_east=mpe.attack_east,
        attack_west=mpe.attack_west,
        attack_northeast=mpe.attack_northeast,
        attack_northwest=mpe.attack_northwest,
        attack_southeast=mpe.attack_southeast,
        attack_southwest=mpe.attack_southwest,
        translate_jump_deltas=mpe.translate_jump_deltas,
        translate_sliding_deltas=mpe.translate_sliding_deltas,
        translate_north=mpe.translate_north,
        translate_south=mpe.translate_south,
        translate_east=mpe.translate_east,
        translate_west=mpe.translate_west,
        translate_northeast=mpe.translate_northeast,
        translate_northwest=mpe.translate_northwest,
        translate_southeast=mpe.translate_southeast,
        translate_southwest=mpe.translate_southwest,
    )

def internal_mp_to_external(mp: MovementPattern) -> MovementPatternExternal:
    promotion_squares = []
    if mp.promotion_squares is not None:
        bb = mp.promotion_squares
        while not bb.is_zero():
            index = bb.lowest_one()
            sq = from_index(index)
            promotion_squares.append(sq)
            bb.set_bit(index, False)
    return MovementPatternExternal(
        promotion_squares=promotion_squares if promotion_squares else None,
        promo_vals=mp.promo_vals,
        attack_sliding_deltas=mp.attack_sliding_deltas,
        attack_jump_deltas=mp.attack_jump_deltas,
        attack_north=mp.attack_north,
        attack_south=mp.attack_south,
        attack_east=mp.attack_east,
        attack_west=mp.attack_west,
        attack_northeast=mp.attack_northeast,
        attack_northwest=mp.attack_northwest,
        attack_southeast=mp.attack_southeast,
        attack_southwest=mp.attack_southwest,
        translate_jump_deltas=mp.translate_jump_deltas,
        translate_sliding_deltas=mp.translate_sliding_deltas,
        translate_north=mp.translate_north,
        translate_south=mp.translate_south,
        translate_east=mp.translate_east,
        translate_west=mp.translate_west,
        translate_northeast=mp.translate_northeast,
        translate_northwest=mp.translate_northwest,
        translate_southeast=mp.translate_southeast,
        translate_southwest=mp.translate_southwest,
    )


# Testing
if __name__ == "__main__":
    mp = Move(0, 10, 1, promo='Q', move_type = "Capture")
    
    null_move = Move.null()

    print(mp.get_from())
    print(mp.get_to())
    print(mp.get_target())
    print(mp.get_is_capture())
    print(mp.get_move_type())
    print(mp.get_promotion_char())