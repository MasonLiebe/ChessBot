from typing import List, Tuple, Optional
from bitboard import Bitboard, to_index, from_index

class MovementPatternExternal:
    def __init__(self):
        self.promotion_squares: Optional[List[Tuple[int, int]]] = None
        self.promo_vals: Optional[List[str]] = None
        self.attack_sliding_deltas: List[List[Tuple[int, int]]] = []
        self.attack_jump_deltas: List[Tuple[int, int]] = []
        self.attack_north: bool = False
        self.attack_south: bool = False
        self.attack_east: bool = False
        self.attack_west: bool = False
        self.attack_northeast: bool = False
        self.attack_northwest: bool = False
        self.attack_southeast: bool = False
        self.attack_southwest: bool = False
        self.translate_jump_deltas: List[Tuple[int, int]] = []
        self.translate_sliding_deltas: List[List[Tuple[int, int]]] = []
        self.translate_north: bool = False
        self.translate_south: bool = False
        self.translate_east: bool = False
        self.translate_west: bool = False
        self.translate_northeast: bool = False
        self.translate_northwest: bool = False
        self.translate_southeast: bool = False
        self.translate_southwest: bool = False

class MovementPattern:
    def __init__(self):
        self.promotion_squares: Optional[Bitboard] = None
        self.promo_vals: Optional[List[str]] = None
        self.attack_sliding_deltas: List[List[Tuple[int, int]]] = []
        self.attack_jump_deltas: List[Tuple[int, int]] = []
        self.attack_north: bool = False
        self.attack_south: bool = False
        self.attack_east: bool = False
        self.attack_west: bool = False
        self.attack_northeast: bool = False
        self.attack_northwest: bool = False
        self.attack_southeast: bool = False
        self.attack_southwest: bool = False
        self.translate_jump_deltas: List[Tuple[int, int]] = []
        self.translate_sliding_deltas: List[List[Tuple[int, int]]] = []
        self.translate_north: bool = False
        self.translate_south: bool = False
        self.translate_east: bool = False
        self.translate_west: bool = False
        self.translate_northeast: bool = False
        self.translate_northwest: bool = False
        self.translate_southeast: bool = False
        self.translate_southwest: bool = False

    def promotion_at(self, index: int) -> bool:
        if self.promotion_squares:
            return self.promotion_squares.bit(index)
        return False

def external_mp_to_internal(mpe: MovementPatternExternal) -> MovementPattern:
    promotion_squares = None
    if mpe.promotion_squares:
        bb = Bitboard.zero()
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
        translate_southwest=mpe.translate_southwest
    )

def internal_mp_to_external(mp: MovementPattern) -> MovementPatternExternal:
    promotion_squares = None
    if mp.promotion_squares:
        bb = mp.promotion_squares.copy()
        sq = []
        while not bb.is_zero():
            index = bb.lowest_one()
            sq.append(from_index(index))
            bb.set_bit(index, False)
        if sq:
            promotion_squares = sq

    return MovementPatternExternal(
        promotion_squares=promotion_squares,
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
        translate_southwest=mp.translate_southwest
    )