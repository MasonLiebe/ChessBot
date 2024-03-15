# This file handles the valid move generation for each piece. It uses the bitboard representation of the board to generate the moves for each piece.

from typing import Optional, Tuple
from bitboard import Bitboard, from_index, to_index, to_rank_file
from constants import *

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
    6: "KingMove",
    7: "Null"
}


class Move:
    # Stores the move data in a single 32 bit integer
    # 0-7: from square
    # 8-15: to square
    # 16-19: moving piece type
    # 20-23: target piece type
    # 24-27: move type
    # 28-31: promotion piece type

    def __init__(self, from_square: int, to_square: int, moving_piece_type = None, target_piece_type = None, move_type = "Null", promo = None):

        self.move_data = from_square | (to_square << 8) | (PIECE_TO_INT[moving_piece_type] << 16 if moving_piece_type else 0) | (PIECE_TO_INT[target_piece_type] << 20 if target_piece_type else 0) | (moveType[move_type] << 24) | ( PIECE_TO_INT[promo] << 28 if promo else 0)

    @staticmethod
    def null():
        return Move(0, 0, None, 'Null', None)

    def get_from_index(self) -> int:
        return self.move_data & 255

    def get_to_index(self) -> int:
        return (self.move_data >> 8) & 255

    def get_move_type(self) -> str:
        return intToMoveType[(self.move_data >> 24) & 7]
    
    def get_moving_piece_type(self) -> int:
        return INT_TO_PIECE[(self.move_data >> 16) & 15]
    
    def get_target_piece_type(self) -> int:
        return INT_TO_PIECE[(self.move_data >> 20) & 15]
    
    def get_promotion_piece_type(self) -> str:
        return INT_TO_PIECE[(self.move_data >> 28) & 15]

    def __str__(self):
        x1, y1 = from_index(self.get_from_index())
        x2, y2 = from_index(self.get_to_index())
        return f"(from: {to_rank_file(x1, y1)}, to: {to_rank_file(x2, y2)})"

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
        can_enpassant: bool = False,
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
        self.can_enpassant = can_enpassant

    def promotion_at(self, index: int) -> bool:
        if self.promotion_squares is not None:
            return self.promotion_squares.bit(index)
        return False

STANDARD_PATTERNS = {
    'Pawn' : MovementPattern(
        attack_jump_deltas=[(1, 1), (-1, 1)],
        translate_jump_deltas=[(0, 1)],
        can_enpassant=True,
        promo_vals=['Q', 'R', 'B', 'N', 'A', 'C', 'D', 'E', 'F', 'G'] # Can promote to custom squares
        ),
    'Bishop' : MovementPattern(
        attack_northwest = True,
        attack_northeast = True,
        attack_southwest = True,
        attack_southeast = True,
        translate_northwest = True,
        translate_northeast = True,
        translate_southwest = True,
        translate_southeast = True
    ),
    'Knight' : MovementPattern(
        attack_jump_deltas=[(1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1)],
        translate_jump_deltas=[(1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1)]
    ),
    'Rook' : MovementPattern(
        attack_north = True,
        attack_south = True,
        attack_east = True,
        attack_west = True,
        translate_north = True,
        translate_south = True,
        translate_east = True,
        translate_west = True
    ),
    'Queen' : MovementPattern(
        attack_north = True,
        attack_south = True,
        attack_east = True,
        attack_west = True,
        attack_northeast = True,
        attack_northwest = True,
        attack_southeast = True,
        attack_southwest = True,
        translate_north = True,
        translate_south = True,
        translate_east = True,
        translate_west = True,
        translate_northeast = True,
        translate_northwest = True,
        translate_southeast = True,
        translate_southwest = True
    ),
    'King' : MovementPattern(
        attack_jump_deltas=[(1, 1), (-1, 1), (1, -1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1)],
        translate_jump_deltas=[(1, 1), (-1, 1), (1, -1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1)]
    ),
    'NPawn' : MovementPattern(
        attack_jump_deltas=[(1, 1), (-1, 1)],
        translate_sliding_deltas=[[(0,1), (0,2)]],
        can_enpassant=True,
        promo_vals=['Q', 'R', 'B', 'N', 'A', 'C', 'D', 'E', 'F', 'G']
    )
}

# Testing
if __name__ == "__main__":
    test_cases = [{
            'from': 0,
            'to': 8,
            'move_type': 'Quiet',
            'moving_piece_type': 'Pawn',
            'target_piece_type': 'Empty',
            'promotion_piece_type': 'Queen'
        },
        {
            'from': 0,
            'to': 8,
            'move_type': 'Capture',
            'moving_piece_type': 'Pawn',
            'target_piece_type': 'Rook',
            'promotion_piece_type': 'Queen'
        }
    ]

    # for test in test_cases:
    #     print('Test info:')
    #     for key in test:
    #         print(f'{key}: {test[key]}')
    #     print('-----')

    #     move = Move(test['from'], test['to'], test['moving_piece_type'], test['target_piece_type'], test['move_type'], test['promotion_piece_type'])
    #     print(move)
    #     print(move.get_from_index())
    #     print(move.get_to_index())
    #     print(move.get_move_type())
    #     print(move.get_moving_piece_type())
    #     print(move.get_target_piece_type())
    #     print(move.get_promotion_piece_type())
    #     print('-----------------')