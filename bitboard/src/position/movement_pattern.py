from typing import Optional, Tuple
from bitboard.src.types.bitboard import from_index, to_index

class MovementPatternExternal:
    def __init__(
        self,
        promotion_squares: Optional[List[Tuple[int, int]]],
        promo_vals: Optional[List[str]],
        attack_sliding_deltas: List[List[Tuple[int, int]]],
        attack_jump_deltas: List[Tuple[int, int]],
        attack_north: bool,
        attack_south: bool,
        attack_east: bool,
        attack_west: bool,
        attack_northeast: bool,
        attack_northwest: bool,
        attack_southeast: bool,
        attack_southwest: bool,
        translate_jump_deltas: List[Tuple[int, int]],
        translate_sliding_deltas: List[List[Tuple[int, int]]],
        translate_north: bool,
        translate_south: bool,
        translate_east: bool,
        translate_west: bool,
        translate_northeast: bool,
        translate_northwest: bool,
        translate_southeast: bool,
        translate_southwest: bool
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
        promotion_squares: Optional[Bitboard],
        promo_vals: Optional[List[str]],
        attack_sliding_deltas: List[List[Tuple[int, int]]],
        attack_jump_deltas: List[Tuple[int, int]],
        attack_north: bool,
        attack_south: bool,
        attack_east: bool,
        attack_west: bool,
        attack_northeast: bool,
        attack_northwest: bool,
        attack_southeast: bool,
        attack_southwest: bool,
        translate_jump_deltas: List[Tuple[int, int]],
        translate_sliding_deltas: List[List[Tuple[int, int]]],
        translate_north: bool,
        translate_south: bool,
        translate_east: bool,
        translate_west: bool,
        translate_northeast: bool,
        translate_northwest: bool,
        translate_southeast: bool,
        translate_southwest: bool
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
        bb = Bitboard.zero()
        for x, y in mpe.promotion_squares:
            bb.set_bit(to_index(x, y), True)
        promotion_squares = bb
    return MovementPattern(
        promotion_squares,
        mpe.promo_vals,
        mpe.attack_sliding_deltas,
        mpe.attack_jump_deltas,
        mpe.attack_north,
        mpe.attack_south,
        mpe.attack_east,
        mpe.attack_west,
        mpe.attack_northeast,
        mpe.attack_northwest,
        mpe.attack_southeast,
        mpe.attack_southwest,
        mpe.translate_jump_deltas,
        mpe.translate_sliding_deltas,
        mpe.translate_north,
        mpe.translate_south,
        mpe.translate_east,
        mpe.translate_west,
        mpe.translate_northeast,
        mpe.translate_northwest,
        mpe.translate_southeast,
        mpe.translate_southwest
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
        if len(promotion_squares) == 0:
            promotion_squares = None
    return MovementPatternExternal(
        promotion_squares,
        mp.promo_vals,
        mp.attack_sliding_deltas,
        mp.attack_jump_deltas,
        mp.attack_north,
        mp.attack_south,
        mp.attack_east,
        mp.attack_west,
        mp.attack_northeast,
        mp.attack_northwest,
        mp.attack_southeast,
        mp.attack_southwest,
        mp.translate_jump_deltas,
        mp.translate_sliding_deltas,
        mp.translate_north,
        mp.translate_south,
        mp.translate_east,
        mp.translate_west,
        mp.translate_northeast,
        mp.translate_northwest,
        mp.translate_southeast,
        mp.translate_southwest
    )


