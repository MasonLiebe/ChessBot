from typing import List, Tuple, Dict
from position import Position, Dimensions
from bitboard import Bitboard, to_index
from movement_pattern import MovementPatternExternal
from move import Move, PieceType
from move_generator import MoveGenerator


'''
Class to handle a game, including the current position and the ability to make moves
'''
class Game:
    def __init__(self):
        self.current_position: Position = Position.default()

    @classmethod
    def default(cls) -> 'Game':
        return cls()

    def set_bounds(self, width: int, height: int, valid_squares: List[Tuple[int, int]]):
        bounds = Bitboard.zero()
        for square in valid_squares:
            bounds.set_bit(to_index(square[0], square[1]), True)
        self.current_position.set_bounds(Dimensions(width, height), bounds)

    @staticmethod
    def each_owner_contains_k(vec: List[Tuple[int, int, int, str]]) -> bool:
        num_players = 0
        for owner, x, y, pce in vec:
            if owner >= num_players:
                num_players = owner + 1

        has_k = [False] * num_players
        for owner, x, y, pce_char in vec:
            if pce_char.lower() == 'k':
                has_k[owner] = True

        return all(has_k)

    def set_state(self, movement_patterns: Dict[str, MovementPatternExternal],
                  valid_squares: List[Tuple[int, int]], pieces: List[Tuple[int, int, int, str]]):
        assert Game.each_owner_contains_k(pieces)

        width = 0
        height = 0
        bounds = Bitboard.zero()
        for sq in valid_squares:
            if sq[0] >= width:
                width = sq[0] + 1
            if sq[1] >= height:
                height = sq[1] + 1
            bounds.set_bit(to_index(sq[0], sq[1]), True)

        pieces = [(owner, to_index(x, y), PieceType.from_char(pce_chr)) for owner, x, y, pce_chr in pieces]

        self.current_position = Position.custom(Dimensions(width, height), bounds, movement_patterns, pieces)

    def get_width(self) -> int:
        return self.current_position.dimensions.width

    def get_height(self) -> int:
        return self.current_position.dimensions.height

    def to_string(self) -> str:
        return self.current_position.to_string()

    def get_zobrist(self) -> int:
        return self.current_position.get_zobrist()

    def make_move(self, move_generator: MoveGenerator, x1: int, y1: int, x2: int, y2: int) -> bool:
        from_ = to_index(x1, y1)
        to = to_index(x2, y2)
        moves = move_generator.get_pseudo_moves(self.current_position)
        print('We made it past get_pseudo_moves')

        i = 0
        for move_ in moves:
            if not move_generator.is_move_legal(move_, self.current_position):
                continue
            if move_.get_from() == from_ and move_.get_to() == to:
                self.current_position.make_move(move_)
                return True
        
        return False

    def undo(self):
        self.current_position.unmake_move()

    def get_whos_turn(self) -> int:
        return self.current_position.whos_turn
    
    
if __name__ == '__main__':
    game = Game.default()
    mg = MoveGenerator()

    print(game.get_width())
    print(game.get_height())
    print(game.to_string())

    print(mg.count_legal_moves(game.current_position))

    game.make_move(mg, 4, 1, 4, 3)
    print(game.to_string())

    print('bounds:\n', game.current_position.bounds)
    