from typing import Dict, List 
from position import Position
from move_generator import MoveGenerator
from move import Move, PieceType
from piece_set import PieceSet
from bitboard import Bitboard, from_index


# Relative Centipawn Values provided by alpha zero in 2020
# https://arxiv.org/pdf/2009.04374.pdf

KING_SCORE = 9999
QUEEN_SCORE = 950
ROOK_SCORE = 563
BISHOP_SCORE = 333
KNIGHT_SCORE = 305
PAWN_SCORE = 100
CHECKMATED_SCORE = -99999
CASTLING_BONUS = 400
PST_MULTIPLIER = 5

'''
The Evaluator class is responsible for evaluating the position statically and returning a score.  This is used once the search reaches a maximum depth.  The evaluator uses a combination of material score and positional score to determine the score of a position.  The evaluator also uses a custom piece value table to store the value of custom pieces, and a piece square table to store the positional value of pieces.  Because of the general nature of this implementation, the evaluator is not optimized for traditional test, although it should
generalize relatively well.

There are some conceptual notes that are obvious that aren't accounted for.  For example, you might find that the evaluator doesn't account for the fact that a piece is pinned, or that a piece is attacking a square.  This is because the evaluator is only used at the end of the search, and the search should have already accounted for these things.  The evaluator is only used to give a rough estimate of the position, and is not used to make any decisions.  The search is responsible for making the decisions, and the evaluator is only used to give a rough estimate of the position.
'''

class Evaluator:
    def __init__(self):
        self.custom_piece_value_table: Dict[PieceType, int] = {}
        self.piece_square_table: Dict[PieceType, List[int]] = {}

    def evaluate(self, position: Position, movegen: MoveGenerator) -> int:
        # sums the material and positional scores for each piece
        score = 0
        player_num = position.whos_turn
        total_material_score = 0
        for ps in position.pieces:
            side_multiplier = 1 if ps.player_num == player_num else -1
            material_score = self.get_material_score_for_pieceset(position, ps)
            score += side_multiplier * material_score
            total_material_score += material_score

        # if it's an endgame, evaluation will be handled differently
        is_endgame = total_material_score < 2 * KING_SCORE + 2 * QUEEN_SCORE + 2 * ROOK_SCORE
        for ps in position.pieces:
            side_multiplier = 1 if ps.player_num == player_num else -1
            positional_score = self.get_positional_score(is_endgame, position, ps, movegen)
            if position.properties.castling_rights.did_player_castle(ps.player_num) and not is_endgame:
                score += CASTLING_BONUS
            score += side_multiplier * positional_score

        return score

    def get_material_score_for_pieceset(self, position: Position, piece_set: PieceSet) -> int:
        # sums the material score
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
        # scores a move based on the history and killer moves, used to rank and prioritize moves to improve
        # The efficiency of the alpha-beta pruning process
        if not move_.get_is_capture():
            return 9000 if move_ == killer_moves[depth][0] or move_ == killer_moves[depth][1] else history_moves[move_.get_from()][move_.get_to()]

        attacker: PieceType = position.piece_at(move_.get_from()).piece_type
        victim: PieceType = position.piece_at(move_.get_target()).piece_type

        attack_score = self.get_material_score(attacker, position)
        victim_score = self.get_material_score(victim, position)

        return KING_SCORE + (victim_score - attack_score)

    def get_material_score(self, piece_type: PieceType, position: Position) -> int:
        if isinstance(piece_type, PieceType.Custom):
            if piece_type in self.custom_piece_value_table:
                return self.custom_piece_value_table[piece_type]
            else:
                option_mp = position.get_movement_pattern(piece_type)
                score = Evaluator.score_movement_pattern(option_mp) if option_mp else 0
                self.custom_piece_value_table[piece_type] = score
                return score
        else:
            return {
                PieceType.Pawn: PAWN_SCORE,
                PieceType.Knight: KNIGHT_SCORE,
                PieceType.Bishop: BISHOP_SCORE,
                PieceType.Rook: ROOK_SCORE,
                PieceType.Queen: QUEEN_SCORE,
                PieceType.King: KING_SCORE,
            }[piece_type]

    def can_do_null_move(self, position: Position) -> bool:
        return self.get_material_score_for_pieceset(position, position.pieces[position.whos_turn]) > KING_SCORE + ROOK_SCORE

    @staticmethod
    def score_movement_pattern(mp) -> int:
        # Computes the value of a custom piece based on its movement pattern
        # Values were set based on the known relative value of the standard pieces
        score = 0
        if mp.attack_north:
            score += 112
        if mp.translate_north:
            score += 37
        if mp.attack_east:
            score += 112
        if mp.translate_east:
            score += 37
        if mp.attack_south:
            score += 112
        if mp.translate_south:
            score += 37
        if mp.attack_west:
            score += 112
        if mp.translate_west:
            score += 37
        if mp.attack_northeast:
            score += 66
        if mp.translate_northeast:
            score += 22
        if mp.attack_northwest:
            score += 66
        if mp.translate_northwest:
            score += 22
        if mp.attack_southeast:
            score += 66
        if mp.translate_southeast:
            score += 22
        if mp.attack_southwest:
            score += 66
        if mp.translate_southwest:
            score += 22

        score += len(mp.translate_jump_deltas) * 18
        score += len(mp.attack_jump_deltas) * 18
        for d in mp.translate_sliding_deltas + mp.attack_sliding_deltas:
            score += (len(d) ** .8) * 18 # Longer is better, but there are diminishing returns

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
                    score += -score_table[index] * PST_MULTIPLIER if not is_endgame else score_table[index] * PST_MULTIPLIER
                else:
                    score += score_table[index] * PST_MULTIPLIER
                bb_copy.set_bit(index, False)

        return score

    @staticmethod
    def get_positional_score_vec(position: Position, piece: PieceSet, movegen: MoveGenerator) -> List[int]:
        return_vec = [0] * 256
        total_entries = 0
        sum_ = 0
        for i in range(256):
            x, y = from_index(i)
            num_moves = movegen.get_num_moves_on_empty_board(i, position, piece, position.bounds)
            if position.xy_in_bounds(x, y):
                total_entries += 1
                sum_ += num_moves
            return_vec[i] = num_moves

        mean = sum_ // total_entries
        return_vec = [score - mean for score in return_vec]

        return return_vec