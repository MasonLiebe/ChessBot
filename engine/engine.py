from . import coreGame as cg
from .searcher import Searcher
from .game import Game

from typing import List, Tuple, Dict, Optional
import time

class Engine:
    def __init__(self, position = cg.Position.default()):
        timer = time.time()
        self.current_position: cg.Position = position
        print('position setup time:', time.time() - timer)
        timer = time.time()
        self.move_generator: cg.MoveGenerator = cg.MoveGenerator()
        print('move generator setup time:', time.time() - timer)
        self.evaluator: cg.Evaluator = cg.Evaluator()
        print('evaluator setup time:', time.time() - timer)
        self.searcher: Searcher = Searcher()
        print('searcher setup time:', time.time() - timer)

    @classmethod
    def default(cls) -> 'Engine':
        return cls()

    def get_zobrist(self) -> int:
        return self.current_position.get_zobrist()

    def get_score(self) -> int:
        return self.evaluator.evaluate(self.current_position, self.move_generator)

    def register_piecetype(self, char_rep: str, mpe: cg.MovementPatternExternal):
        self.current_position.register_piecetype(char_rep, mpe)

    def add_piece(self, owner: int, piece_type: cg.PieceType, x: int, y: int):
        self.current_position.add_piece(owner, piece_type, cg.to_index(x, y))

    def remove_piece(self, index: int):
        self.current_position.remove_piece(index)

    def make_move(self, x1: int, y1: int, x2: int, y2: int) -> bool:
        from_ = cg.to_index(x1, y1)
        to = cg.to_index(x2, y2)

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
            move_generator=cg.MoveGenerator(),
            evaluator=cg.Evaluator(),
            searcher=Searcher(),
            current_position=cg.Position.from_fen(fen)
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

            x, y = cg.from_index(move_.get_from())
            x2, y2 = cg.from_index(move_.get_to())
            self.current_position.make_move(move_)
            plus = self.perft(depth - 1)
            nodes += plus
            self.current_position.unmake_move()
            printing.append(f"{cg.to_rank_file(x, y)}{cg.to_rank_file(x2, y2)}: {plus}")
        printing.sort()
        for s in printing:
            print(s)
        return nodes

    def play_best_move(self, depth: int) -> bool:
        best = self.searcher.get_best_move(self.current_position, self.evaluator, self.move_generator, depth)
        if best:
            x1, y1 = cg.from_index(best.get_from())
            x2, y2 = cg.from_index(best.get_to())
            return self.make_move(x1, y1, x2, y2)
        else:
            return False

    def get_best_move(self, depth: int) -> Optional[Tuple[int, int, int, int]]:
        best = self.searcher.get_best_move(self.current_position, self.evaluator, self.move_generator, depth)
        if best:
            x1, y1 = cg.from_index(best.get_from())
            x2, y2 = cg.from_index(best.get_to())
            return x1, y1, x2, y2
        else:
            return None

    def play_best_move_timeout(self, max_sec: int) -> Tuple[bool, int]:
        result = self.searcher.get_best_move_timeout(self.current_position, self.evaluator, self.move_generator, max_sec)
        if result:
            best, depth = result
            x1, y1 = cg.from_index(best.get_from())
            x2, y2 = cg.from_index(best.get_to())
            return self.make_move(x1, y1, x2, y2), depth
        else:
            return False, 0

    def get_best_move_timeout(self, max_sec: int) -> Optional[Tuple[Tuple[int, int, int, int], int]]:
        result = self.searcher.get_best_move_timeout(self.current_position, self.evaluator, self.move_generator, max_sec)
        if result:
            best, depth = result
            x1, y1 = cg.from_index(best.get_from())
            x2, y2 = cg.from_index(best.get_to())
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

    def set_state(self, movement_patterns: Dict[str, cg.MovementPatternExternal],
                  valid_squares: List[Tuple[int, int]], pieces: List[Tuple[int, int, int, str]]):
        assert Game.each_owner_contains_k(pieces)
        width = 0
        height = 0
        bounds = cg.Bitboard.zero()
        for sq in valid_squares:
            if sq[0] >= width:
                width = sq[0] + 1
            if sq[1] >= height:
                height = sq[1] + 1
            bounds.set_bit(cg.to_index(sq[0], sq[1]), True)

        pieces = [(owner, cg.to_index(x, y), cg.PieceType.from_char(pce_chr)) for owner, x, y, pce_chr in pieces]
        self.current_position = cg.Position.custom(cg.Dimensions(width, height), bounds, movement_patterns, pieces)

    def get_pieces(self):
        # returns a list of tuples of the form (owner, x, y, piece_char)
        pieces = []
        for x in range(self.current_position.dimensions.width):
            for y in range(self.current_position.dimensions.height):
                index = cg.to_index(x, y)
                pos_info = self.current_position.piece_at(index)
                if pos_info is not None:
                    owner, piece = pos_info
                    color = 'white' if owner == 0 else 'black'
                    pieces.append((color, x, y, piece.piece_type.name))
        return pieces


# def play_test(engine):
#     while True:
#         print(engine.to_string())
#         print()
#         start = time.time()
#         if engine.to_move_in_check():
#             print("Check!")
#         x1, y1, x2, y2 = engine.get_best_move(6)
#         if x1 is None:
#             print("No legal moves!")
#             break
#         print(f"Playing move: {to_rank_file(x1, y1)}{to_rank_file(x2, y2)}")
#         engine.make_move(x1, y1, x2, y2)
#         print("Score:", engine.get_score())
#         print("Zobrist:", engine.get_zobrist())
#         print('time_taken:', time.time() - start)
#         print()


if __name__ == '__main__':


    start = time.time()
    engine = Engine(cg.Position.default())
    print(engine.current_position.to_string())
    print('engine_setup_time:', time.time() - start)

    start = time.time()
    print(engine.perft(5))
    print('perft4_time:', time.time() - start)



    # start = time.time()
    # print(engine.perft(5))
    # print('perft5_time:', time.time() - start)
    
    # print(engine.perft(2))
    # print(engine.perft(3))
    # print(engine.perft(4))
