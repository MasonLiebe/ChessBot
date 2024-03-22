from typing import List, Tuple, Dict, Optional
from position import Position, Dimensions
from move_generator import MoveGenerator
from evaluator import Evaluator
from searcher import Searcher
from bitboard import Bitboard, to_index, from_index, to_rank_file
from movement_pattern import MovementPatternExternal
from move import PieceType 
from game import Game


class Engine:
    def __init__(self, position = Position.default()):
        self.current_position: Position = position
        self.move_generator: MoveGenerator = MoveGenerator()
        self.evaluator: Evaluator = Evaluator()
        self.searcher: Searcher = Searcher()

    @classmethod
    def default(cls) -> 'Engine':
        return cls()

    def get_zobrist(self) -> int:
        return self.current_position.get_zobrist()

    def get_score(self) -> int:
        return self.evaluator.evaluate(self.current_position, self.move_generator)

    def register_piecetype(self, char_rep: str, mpe: MovementPatternExternal):
        self.current_position.register_piecetype(char_rep, mpe)

    def add_piece(self, owner: int, piece_type: PieceType, x: int, y: int):
        self.current_position.add_piece(0, PieceType.Custom('a'), to_index(x, y))

    def remove_piece(self, index: int):
        self.current_position.remove_piece(index)

    def make_move(self, x1: int, y1: int, x2: int, y2: int) -> bool:
        from_ = to_index(x1, y1)
        to = to_index(x2, y2)

        moves = self.move_generator.get_pseudo_moves(self.current_position)
        for move_ in moves:
            if not self.move_generator.is_move_legal(move_, self.current_position):
                continue
            if move_.get_from() == from_ and move_.get_to() == to:
                self.current_position.make_move(move_)
                return True
        return False

    def undo(self):
        self.current_position.unmake_move()

    def to_string(self) -> str:
        return self.current_position.to_string()

    @classmethod
    def from_fen(cls, fen: str) -> 'Engine':
        return cls(
            move_generator=MoveGenerator(),
            evaluator=Evaluator(),
            searcher=Searcher(),
            current_position=Position.from_fen(fen)
        )

    def perft(self, depth: int) -> int:
        nodes = 0

        moves = self.move_generator.get_pseudo_moves(self.current_position)

        if depth == 1:
            return self.move_generator.count_legal_moves(self.current_position)
        for move_ in moves:
            if not self.move_generator.is_move_legal(move_, self.current_position):
                continue
            self.current_position.make_move(move_)
            nodes += self.perft(depth - 1)
            self.current_position.unmake_move()
        return nodes

    def perft_divide(self, depth: int) -> int:
        nodes = 0

        moves = self.move_generator.get_pseudo_moves(self.current_position)
        if depth == 1:
            return self.move_generator.count_legal_moves(self.current_position)
        printing = []
        for move_ in moves:
            if not self.move_generator.is_move_legal(move_, self.current_position):
                continue

            x, y = from_index(move_.get_from())
            x2, y2 = from_index(move_.get_to())
            self.current_position.make_move(move_)
            plus = self.perft(depth - 1)
            nodes += plus
            self.current_position.unmake_move()
            printing.append(f"{to_rank_file(x, y)}{to_rank_file(x2, y2)}: {plus}")
        printing.sort()
        for s in printing:
            print(s)
        return nodes

    def play_best_move(self, depth: int) -> bool:
        best = self.searcher.get_best_move(self.current_position, self.evaluator, self.move_generator, depth)
        if best:
            x1, y1 = from_index(best.get_from())
            x2, y2 = from_index(best.get_to())
            return self.make_move(x1, y1, x2, y2)
        else:
            return False

    def get_best_move(self, depth: int) -> Optional[Tuple[int, int, int, int]]:
        best = self.searcher.get_best_move(self.current_position, self.evaluator, self.move_generator, depth)
        if best:
            x1, y1 = from_index(best.get_from())
            x2, y2 = from_index(best.get_to())
            return x1, y1, x2, y2
        else:
            return None

    def play_best_move_timeout(self, max_sec: int) -> Tuple[bool, int]:
        result = self.searcher.get_best_move_timeout(self.current_position, self.evaluator, self.move_generator, max_sec)
        if result:
            best, depth = result
            x1, y1 = from_index(best.get_from())
            x2, y2 = from_index(best.get_to())
            return self.make_move(x1, y1, x2, y2), depth
        else:
            return False, 0

    def get_best_move_timeout(self, max_sec: int) -> Optional[Tuple[Tuple[int, int, int, int], int]]:
        result = self.searcher.get_best_move_timeout(self.current_position, self.evaluator, self.move_generator, max_sec)
        if result:
            best, depth = result
            x1, y1 = from_index(best.get_from())
            x2, y2 = from_index(best.get_to())
            return (x1, y1, x2, y2), depth
        else:
            return None

    def moves_from(self, x: int, y: int) -> List[Tuple[int, int]]:
        moves = self.move_generator.get_legal_moves_as_tuples(self.current_position)
        possible_moves = []
        for from_, to_ in moves:
            if from_ == (x, y):
                possible_moves.append(to_)
        return possible_moves

    def to_move_in_check(self) -> bool:
        return self.move_generator.in_check(self.current_position)

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


if __name__ == '__main__':

    engine = Engine(Position.from_fen("rnbqkbnr/pppppppp/8/4B3/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"))
    print(engine.current_position.to_string())
    
    print(engine.perft(1))