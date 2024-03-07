import sys

sys.path.insert(1, 'chessBot//bitboard//src')

from typing import List, Dict
from position.mod import Position
from collections import defaultdict
from position.piece_set import PieceSet
from move_generator.mod import MoveGenerator
from types.mod import PieceType
from position.piece import Piece
from types.bitboard import from_index
from types.chess_move import Move

# Scores are in centipawns
KING_SCORE = 9999
QUEEN_SCORE = 900
ROOK_SCORE = 500
BISHOP_SCORE = 350
KNIGHT_SCORE = 300
PAWN_SCORE = 100
CHECKMATED_SCORE = -99999
CASTLING_BONUS = 400
# Multiplier for the piece square table
PST_MULTIPLIER = 5

class Evaluator:
    def __init__(self):
        # Piece values for pieces,
        # Hard coded for builtin pieces,
        # generated dynamically based on the piece's movement pattern
        self.custom_piece_value_table = defaultdict(int)
        # Piece-square values for all pieces, done as a function of movement possibilities
        # Generated dynamically for all pieces
        self.piece_square_table = defaultdict(list)

    def evaluate(self, position: Position, movegen: MoveGenerator) -> int:
        score = 0
        player_num = position.whos_turn
        # Material score
        total_material_score = 0
        for ps in position.pieces:
            side_multiplier = 1 if ps.player_num == player_num else -1
            material_score = self.get_material_score_for_pieceset(position, ps)
            score += side_multiplier * material_score
            total_material_score += material_score
        # Positional score
        is_endgame = total_material_score < 2 * KING_SCORE + 2 * QUEEN_SCORE + 2 * ROOK_SCORE
        for ps in position.pieces:
            side_multiplier = 1 if ps.player_num == player_num else -1
            positional_score = self.get_positional_score(is_endgame, position, ps, movegen)
            # Castling bonus
            if position.properties.castling_rights.did_player_castle(ps.player_num) and not is_endgame:
                score += CASTLING_BONUS
            score += side_multiplier * positional_score
        return score

    def get_material_score_for_pieceset(self, position: Position, piece_set: PieceSet) -> int:
        material_score = 0
        material_score += piece_set.king.bitboard.count_ones() * KING_SCORE
        material_score += piece_set.queen.bitboard.count_ones() * QUEEN_SCORE
        material_score += piece_set.rook.bitboard.count_ones() * ROOK_SCORE
        material_score += piece_set.knight.bitboard.count_ones() * KNIGHT_SCORE
        material_score += piece_set.bishop.bitboard.count_ones() * BISHOP_SCORE
        material_score += piece_set.pawn.bitboard.count_ones() * PAWN_SCORE
        for custom in piece_set.custom:
            if custom.piece_type in self.custom_piece_value_table:
                score = self.custom_piece_value_table[custom.piece_type]
                material_score += custom.bitboard.count_ones() * score
            else:
                option_mp = position.get_movement_pattern(custom.piece_type)
                score = Evaluator.score_movement_pattern(option_mp) if option_mp else 0
                self.custom_piece_value_table[custom.piece_type] = score
                material_score += custom.bitboard.count_ones() * score
        return material_score

    def score_move(self, depth: int, history_moves: List[List[int]], killer_moves: List[List[Move]], position: Position, move_: Move) -> int:
        if not move_.get_is_capture():
            if move_ == killer_moves[depth][0] or move_ == killer_moves[depth][1]:
                return 9000
            else:
                return history_moves[move_.get_from()][move_.get_to()]
        attacker = position.piece_at(move_.get_from()).piece_type
        victim = position.piece_at(move_.get_target()).piece_type
        attack_score = self.get_material_score(attacker, position)
        victim_score = self.get_material_score(victim, position)
        return KING_SCORE + (victim_score - attack_score)

    def get_material_score(self, piece_type: PieceType, position: Position) -> int:
        if piece_type == PieceType.Pawn:
            return PAWN_SCORE
        elif piece_type == PieceType.Knight:
            return KNIGHT_SCORE
        elif piece_type == PieceType.Bishop:
            return BISHOP_SCORE
        elif piece_type == PieceType.Rook:
            return ROOK_SCORE
        elif piece_type == PieceType.Queen:
            return QUEEN_SCORE
        elif piece_type == PieceType.King:
            return KING_SCORE
        elif isinstance(piece_type, PieceType.Custom):
            if piece_type in self.custom_piece_value_table:
                return self.custom_piece_value_table[piece_type]
            else:
                option_mp = position.get_movement_pattern(piece_type)
                score = Evaluator.score_movement_pattern(option_mp) if option_mp else 0
                self.custom_piece_value_table[piece_type] = score
                return score

    def can_do_null_move(self, position: Position) -> bool:
        return self.get_material_score_for_pieceset(position, position.pieces[position.whos_turn]) > KING_SCORE + ROOK_SCORE

    @staticmethod
    def score_movement_pattern(mp) -> int:
        score = 0
        if mp.attack_north:
            score += 60
        if mp.translate_north:
            score += 60
        if mp.attack_east:
            score += 60
        if mp.translate_east:
            score += 60
        if mp.attack_south:
            score += 60
        if mp.translate_south:
            score += 60
        if mp.attack_west:
            score += 60
        if mp.translate_west:
            score += 60
        if mp.attack_northeast:
            score += 60
        if mp.translate_northeast:
            score += 60
        if mp.attack_northwest:
            score += 60
        if mp.translate_northwest:
            score += 60
        if mp.attack_southeast:
            score += 60
        if mp.translate_southeast:
            score += 60
        if mp.attack_southwest:
            score += 60
        if mp.translate_southwest:
            score += 60
        score += len(mp.translate_jump_deltas) * 18
        score += len(mp.attack_jump_deltas) * 18
        for d in mp.translate_sliding_deltas + mp.attack_sliding_deltas:
            score += len(d) * 18
        return score

    def get_positional_score(self, is_endgame: bool, position: Position, piece_set: PieceSet, movegen: MoveGenerator) -> int:
        score = 0
        for p in piece_set.get_piece_refs():
            if p.piece_type not in self.piece_square_table:
                score_vec = Evaluator.get_positional_score_vec(position, p, movegen)
                self.piece_square_table[p.piece_type] = score_vec
            bb_copy = p.bitboard.copy()
            score_table = self.piece_square_table[p.piece_type]
            while not bb_copy.is_zero():
                index = bb_copy.lowest_one()
                if p.piece_type == PieceType.King:
                    if not is_endgame:
                        score += -score_table[index] * PST_MULTIPLIER
                    else:
                        score += score_table[index] * PST_MULTIPLIER
                else:
                    score += score_table[index] * PST_MULTIPLIER
                bb_copy.set_bit(index, False)
        return score

    @staticmethod
    def get_positional_score_vec(position: Position, piece: Piece, movegen: MoveGenerator) -> List[int]:
        return_vec = []
        total_entries = 0
        sum_ = 0
        for i in range(256):
            x, y = from_index(i)
            num_moves = movegen.get_num_moves_on_empty_board(i, position, piece, position.bounds)
            if position.xy_in_bounds(x, y):
                total_entries += 1
                sum_ += num_moves
            return_vec.append(num_moves)
        mean = sum_ // total_entries
        for i in range(256):
            return_vec[i] -= mean
        return return_vec

def test():
    eval = Evaluator()
    movegen = MoveGenerator()
    pos = Position.from_fen("rnbqkbnr/pppppppp/8/8/8/3PP3/PPP2PPP/RNBQKBNR w KQkq - 0 1")
    print(eval.evaluate(pos, movegen))

test()


