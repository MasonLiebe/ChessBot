from typing import List, Tuple, Optional
from .bitboard import Bitboard, to_index, from_index
'''
These classes are used to represent the movement patterns of pieces. In the
Position class, there is a dictionary of these pattern objects, indexed on 
the piece type. From the perspective of the Position class, the MovementPattern
class is the internal representation of a movement pattern, and the 
MovementPatternExternal class is the external representation of a movement
pattern. The MovementPatternExternal class is used to serialize the movement
patterns to a JSON file, and the MovementPattern class is used to deserialize
the movement patterns from a JSON file.

SOME NOTES ABOUT THE MOVEMENT PATTERN ITEMS:
The promotion squares are a list of x, y tuples that represent the squares that
a piece can promote on. The promo_vals are the values that a piece can promote to.

The attack_sliding_deltas are a list of lists of x, y tuples that represent different
'sliding' moves a piece can make.  A sliding move is one where it's legality relies
on the sequential emptiness of prior squares.  The only example of such a move in standard 
chess is the Pawn's initial two-square move, where it requires the square in between to be empty.
The x, y values are the offsets from the piece's current position.

The jumping deltas are a list of jumping moves, whose legality does not depend on the emptiness
of the squares in between.  The chanonical example of this in chess is the knight move.
The x, y values are again the offsets from the piece's current position.

The attack vs. translate items are used to destinguish whether a piece can attack in a certain
direction, or whether it can only translate in that direction.  For example, a pawn can only attack
diagonally, and it can only translate forward.
'''

class MovementPatternExternal:
    def __init__(self, promotion_squares: Optional[List[Tuple[int, int]]] = None,
                 promo_vals: Optional[List[str]] = None,
                 attack_sliding_deltas: List[List[Tuple[int, int]]] = None,
                 attack_jump_deltas: List[Tuple[int, int]] = None,
                 attack_north: bool = False,
                 attack_south: bool = False,
                 attack_east: bool = False,
                 attack_west: bool = False,
                 attack_northeast: bool = False,
                 attack_northwest: bool = False,
                 attack_southeast: bool = False,
                 attack_southwest: bool = False,
                 translate_jump_deltas: List[Tuple[int, int]] = None,
                 translate_sliding_deltas: List[List[Tuple[int, int]]] = None,
                 translate_north: bool = False,
                 translate_south: bool = False,
                 translate_east: bool = False,
                 translate_west: bool = False,
                 translate_northeast: bool = False,
                 translate_northwest: bool = False,
                 translate_southeast: bool = False,
                 translate_southwest: bool = False):
        self.promotion_squares = promotion_squares
        self.promo_vals = promo_vals
        self.attack_sliding_deltas = attack_sliding_deltas or []
        self.attack_jump_deltas = attack_jump_deltas or []
        self.attack_north = attack_north
        self.attack_south = attack_south
        self.attack_east = attack_east
        self.attack_west = attack_west
        self.attack_northeast = attack_northeast
        self.attack_northwest = attack_northwest
        self.attack_southeast = attack_southeast
        self.attack_southwest = attack_southwest
        self.translate_jump_deltas = translate_jump_deltas or []
        self.translate_sliding_deltas = translate_sliding_deltas or []
        self.translate_north = translate_north
        self.translate_south = translate_south
        self.translate_east = translate_east
        self.translate_west = translate_west
        self.translate_northeast = translate_northeast
        self.translate_northwest = translate_northwest
        self.translate_southeast = translate_southeast
        self.translate_southwest = translate_southwest
    
    def __str__(self) -> str:
        return f'MovementPatternExternal(promotion_squares={self.promotion_squares}, promo_vals={self.promo_vals}, attack_sliding_deltas={self.attack_sliding_deltas}, attack_jump_deltas={self.attack_jump_deltas}, attack_north={self.attack_north}, attack_south={self.attack_south}, attack_east={self.attack_east}, attack_west={self.attack_west}, attack_northeast={self.attack_northeast}, attack_northwest={self.attack_northwest}, attack_southeast={self.attack_southeast}, attack_southwest={self.attack_southwest}, translate_jump_deltas={self.translate_jump_deltas}, translate_sliding_deltas={self.translate_sliding_deltas}, translate_north={self.translate_north}, translate_south={self.translate_south}, translate_east={self.translate_east}, translate_west={self.translate_west}, translate_northeast={self.translate_northeast}, translate_northwest={self.translate_northwest}, translate_southeast={self.translate_southeast}, translate_southwest={self.translate_southwest})'

class MovementPattern:
    def __init__(self, promotion_squares: Optional[Bitboard] = None,
                 promo_vals: Optional[List[str]] = None,
                 attack_sliding_deltas: List[List[Tuple[int, int]]] = None,
                 attack_jump_deltas: List[Tuple[int, int]] = None,
                 attack_north: bool = False,
                 attack_south: bool = False,
                 attack_east: bool = False,
                 attack_west: bool = False,
                 attack_northeast: bool = False,
                 attack_northwest: bool = False,
                 attack_southeast: bool = False,
                 attack_southwest: bool = False,
                 translate_jump_deltas: List[Tuple[int, int]] = None,
                 translate_sliding_deltas: List[List[Tuple[int, int]]] = None,
                 translate_north: bool = False,
                 translate_south: bool = False,
                 translate_east: bool = False,
                 translate_west: bool = False,
                 translate_northeast: bool = False,
                 translate_northwest: bool = False,
                 translate_southeast: bool = False,
                 translate_southwest: bool = False):
        self.promotion_squares = promotion_squares
        self.promo_vals = promo_vals
        self.attack_sliding_deltas = attack_sliding_deltas or []
        self.attack_jump_deltas = attack_jump_deltas or []
        self.attack_north = attack_north
        self.attack_south = attack_south
        self.attack_east = attack_east
        self.attack_west = attack_west
        self.attack_northeast = attack_northeast
        self.attack_northwest = attack_northwest
        self.attack_southeast = attack_southeast
        self.attack_southwest = attack_southwest
        self.translate_jump_deltas = translate_jump_deltas or []
        self.translate_sliding_deltas = translate_sliding_deltas or []
        self.translate_north = translate_north
        self.translate_south = translate_south
        self.translate_east = translate_east
        self.translate_west = translate_west
        self.translate_northeast = translate_northeast
        self.translate_northwest = translate_northwest
        self.translate_southeast = translate_southeast
        self.translate_southwest = translate_southwest

    def promotion_at(self, index: int) -> bool:
        if self.promotion_squares:
            return self.promotion_squares.bit(index)
        return False

    def __str__(self) -> str:
        return f'MovementPattern(promotion_squares={self.promotion_squares}, promo_vals={self.promo_vals}, attack_sliding_deltas={self.attack_sliding_deltas}, attack_jump_deltas={self.attack_jump_deltas}, attack_north={self.attack_north}, attack_south={self.attack_south}, attack_east={self.attack_east}, attack_west={self.attack_west}, attack_northeast={self.attack_northeast}, attack_northwest={self.attack_northwest}, attack_southeast={self.attack_southeast}, attack_southwest={self.attack_southwest}, translate_jump_deltas={self.translate_jump_deltas}, translate_sliding_deltas={self.translate_sliding_deltas}, translate_north={self.translate_north}, translate_south={self.translate_south}, translate_east={self.translate_east}, translate_west={self.translate_west}, translate_northeast={self.translate_northeast}, translate_northwest={self.translate_northwest}, translate_southeast={self.translate_southeast}, translate_southwest={self.translate_southwest})'

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