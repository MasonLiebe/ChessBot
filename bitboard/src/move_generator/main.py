from typing import List, Tuple

from bitboard.src.types.mod import PieceType
from types.bitboard import Bitboard, from_index, to_index
from position.mod import Position
from position.piece_set import PieceSet
from move_generator.attack_tables.mod import AttackTables
from move_generator.bitboard_moves import BitboardMoves
from types.chess_move import Move, MoveType
from position.piece import Piece


class MoveGenerator:
    def __init__(self):
        self.attack_tables = AttackTables()

    def get_legal_moves_as_tuples(self, position: Position) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        legal_tuples = []
        for move_ in self.get_pseudo_moves(position):
            if not self.is_move_legal(move_, position):
                continue
            legal_tuples.append((from_index(move_.get_from()), from_index(move_.get_to())))
        return legal_tuples

    def get_pseudo_moves(self, position: Position):
        return self.get_classical_pseudo_moves(position) + self.get_custom_psuedo_moves(position)

    def get_capture_moves(self, position: Position):
        return filter(lambda x: x.get_is_capture(), self.get_classical_pseudo_moves(position)) + \
               filter(lambda x: x.get_is_capture(), self.get_custom_psuedo_moves(position))

    def get_classical_pseudo_moves(self, position: Position):
        my_pieces: PieceSet = position.pieces[position.whos_turn]
        enemies = position.occupied & ~my_pieces.occupied
        iters = []
        occ_or_not_in_bounds = position.occupied | ~position.bounds

        def apply_to_each(pieceset: Bitboard, func):
            while not pieceset.is_zero():
                index = pieceset.lowest_one().unwrap()
                raw_attacks = func(self.attack_tables, index, occ_or_not_in_bounds, enemies)
                raw_attacks &= ~my_pieces.occupied
                raw_attacks &= position.bounds
                iters.append(BitboardMoves(
                    enemies.copy(),
                    raw_attacks,
                    index,
                    None,
                    None,
                ))
                pieceset.set_bit(index, False)

        apply_to_each(my_pieces.king.bitboard.copy(), AttackTables.get_king_attack)
        apply_to_each(my_pieces.queen.bitboard.copy(), AttackTables.get_queen_attack)
        apply_to_each(my_pieces.rook.bitboard.copy(), AttackTables.get_rook_attack)
        apply_to_each(my_pieces.bishop.bitboard.copy(), AttackTables.get_bishop_attack)
        apply_to_each(my_pieces.knight.bitboard.copy(), AttackTables.get_knight_attack)

        extra_moves = []
        p_copy = my_pieces.pawn.bitboard.copy()
        while not p_copy.is_zero():
            index = p_copy.lowest_one().unwrap()
            if position.whos_turn == 0:
                raw_attacks = self.attack_tables.get_north_pawn_attack(index, position.occupied, enemies)
            else:
                raw_attacks = self.attack_tables.get_south_pawn_attack(index, position.occupied, enemies)
            raw_attacks &= ~my_pieces.occupied
            raw_attacks &= position.bounds
            promotion_squares = self.attack_tables.masks.get_rank(position.dimensions.height - 1) if position.whos_turn == 0 else \
                self.attack_tables.masks.get_rank(0)
            promo_vals = ['r', 'b', 'n', 'q']
            iters.append(BitboardMoves(
                enemies.copy(),
                raw_attacks,
                index,
                promotion_squares.copy(),
                promo_vals.copy()
            ))
            if position.properties.ep_square is not None:
                ep_sq = position.properties.ep_square
                if position.whos_turn == 0:
                    attack_only = self.attack_tables.get_north_pawn_attack_raw(index) & ~my_pieces.occupied
                else:
                    attack_only = self.attack_tables.get_south_pawn_attack_raw(index) & ~my_pieces.occupied
                if attack_only.bit(ep_sq):
                    cap_x, cap_y = from_index(ep_sq)
                    if position.whos_turn == 0:
                        cap_y -= 1
                    else:
                        cap_y += 1
                    move_ = Move(index, ep_sq, to_index(cap_x, cap_y), MoveType.Capture, None)
                    extra_moves.append(move_)
            p_copy.set_bit(index, False)

        if my_pieces.king.bitboard.lowest_one() is not None:
            king_index = my_pieces.king.bitboard.lowest_one()
            kx, ky = from_index(king_index)
            whos_turn = position.whos_turn
            if position.properties.castling_rights.can_player_castle_kingside(position.whos_turn):
                rook_index = to_index(position.dimensions.width - 1, ky)
                owner, pt = position.piece_at(rook_index)
                if owner == whos_turn and pt.piece_type == PieceType.Rook:
                    east = self.attack_tables.masks.get_east(king_index)
                    occ = east & position.occupied
                    occ.set_bit(rook_index, False)
                    if occ.is_zero():
                        king_one_step_indx = to_index(kx + 1, ky)
                        if self.is_move_legal(Move.null(), position) and self.is_move_legal(
                                Move(king_index, king_one_step_indx, None, MoveType.Quiet, None),
                                position
                        ):
                            to_index = to_index(kx + 2, ky)
                            extra_moves.append(Move(king_index, to_index, rook_index, MoveType.KingsideCastle, None))
            if position.properties.castling_rights.can_player_castle_queenside(position.whos_turn):
                rook_index = to_index(0, ky)
                owner, pt = position.piece_at(rook_index)
                if owner == whos_turn and pt.piece_type == PieceType.Rook:
                    west = self.attack_tables.masks.get_west(king_index)
                    occ = west & position.occupied
                    occ.set_bit(rook_index, False)
                    if occ.is_zero():
                        king_one_step_indx = to_index(kx - 1, ky)
                        if self.is_move_legal(Move.null(), position) and self.is_move_legal(
                                Move(king_index, king_one_step_indx, None, MoveType.Quiet, None),
                                position
                        ):
                            to_index = to_index(kx - 2, ky)
                            extra_moves.append(Move(king_index, to_index, rook_index, MoveType.QueensideCastle, None))

        return iters + extra_moves

    def get_custom_psuedo_moves(self, position: Position):
        my_pieces: PieceSet = position.pieces[position.whos_turn]
        iters = []
        moves = []
        if len(my_pieces.custom) == 0:
            return iters + moves
        enemies = position.occupied & ~my_pieces.occupied
        occ_or_not_in_bounds = position.occupied | ~position.bounds
        for p in my_pieces.custom:
            movement = position.get_movement_pattern(p.piece_type)
            if movement is None:
                continue
            bb = p.bitboard
            bb_copy = bb.copy()
            while not bb_copy.is_zero():
                index = bb_copy.lowest_one().unwrap()
                raw_attacks = self.attack_tables.get_sliding_moves_bb(
                    index,
                    occ_or_not_in_bounds,
                    movement.attack_north,
                    movement.attack_east,
                    movement.attack_south,
                    movement.attack_west,
                    movement.attack_northeast,
                    movement.attack_northwest,
                    movement.attack_southeast,
                    movement.attack_southwest
                )
                raw_attacks &= enemies
                raw_attacks &= position.bounds
                iters.append(BitboardMoves(
                    enemies.copy(),
                    raw_attacks,
                    index,
                    movement.promotion_squares.copy(),
                    movement.promo_vals.copy(),
                ))
                raw_moves = self.attack_tables.get_sliding_moves_bb(
                    index,
                    occ_or_not_in_bounds,
                    movement.translate_north,
                    movement.translate_east,
                    movement.translate_south,
                    movement.translate_west,
                    movement.translate_northeast,
                    movement.translate_northwest,
                    movement.translate_southeast,
                    movement.translate_southwest
                )
                raw_moves &= ~position.occupied
                raw_moves &= position.bounds
                iters.append(BitboardMoves(
                    enemies.copy(),
                    raw_moves,
                    index,
                    movement.promotion_squares.copy(),
                    movement.promo_vals.copy(),
                ))
                x, y = from_index(index)
                for dx, dy in movement.translate_jump_deltas:
                    x2, y2 = x + dx, y + dy
                    if x2 < 0 or y2 < 0 or x2 > 15 or y2 > 15:
                        continue
                    to = to_index(x2, y2)
                    if position.xy_in_bounds(x2, y2) and not position.occupied.bit(to):
                        if movement.promotion_at(to):
                            for c in movement.promo_vals:
                                moves.append(Move(index, to, None, MoveType.Promotion, c))
                        else:
                            moves.append(Move(index, to, None, MoveType.Quiet, None))
                for dx, dy in movement.attack_jump_deltas:
                    x2, y2 = x + dx, y + dy
                    if x2 < 0 or y2 < 0 or x2 > 15 or y2 > 15:
                        continue
                    to = to_index(x2, y2)
                    if enemies.bit(to):
                        if movement.promotion_at(to):
                            for c in movement.promo_vals:
                                moves.append(Move(index, to, to, MoveType.PromotionCapture, c))
                        else:
                            moves.append(Move(index, to, to, MoveType.Capture, None))
                for run in movement.attack_sliding_deltas:
                    for dx, dy in run:
                        x2, y2 = x + dx, y + dy
                        if x2 < 0 or y2 < 0 or x2 > 15 or y2 > 15:
                            break
                        to = to_index(x2, y2)
                        if not position.xy_in_bounds(x2, y2):
                            break
                        if enemies.bit(to):
                            if movement.promotion_at(to):
                                for c in movement.promo_vals:
                                    moves.append(Move(index, to, to, MoveType.PromotionCapture, c))
                            else:
                                moves.append(Move(index, to, to, MoveType.Capture, None))
                            break
                        if position.occupied.bit(to):
                            break
                for run in movement.translate_sliding_deltas:
                    for dx, dy in run:
                        x2, y2 = x + dx, y + dy
                        if x2 < 0 or y2 < 0 or x2 > 15 or y2 > 15:
                            break
                        to = to_index(x2, y2)
                        if not position.xy_in_bounds(x2, y2) or position.occupied.bit(to):
                            break
                        if movement.promotion_at(to):
                            for c in movement.promo_vals:
                                moves.append(Move(index, to, None, MoveType.Quiet, c))
                        else:
                            moves.append(Move(index, to, None, MoveType.Quiet, None))
                bb_copy.set_bit(index, False)
        return iters + moves

    def get_num_moves_on_empty_board(self, index: int, position: Position, piece: Piece, bounds: Bitboard) -> int:
        x, y = from_index(index)
        if not position.xy_in_bounds(x, y):
            return 0
        zero = Bitboard.zero()
        not_in_bounds = ~position.bounds
        moves = 0
        if piece.piece_type == PieceType.Queen:
            moves = self.attack_tables.get_queen_attack(index, not_in_bounds, zero)
        elif piece.piece_type == PieceType.Bishop:
            moves = self.attack_tables.get_bishop_attack(index, not_in_bounds, zero)
        elif piece.piece_type == PieceType.Rook:
            moves = self.attack_tables.get_rook_attack(index, not_in_bounds, zero)
        elif piece.piece_type == PieceType.Knight:
            moves = self.attack_tables.get_knight_attack(index, not_in_bounds, zero)
        elif piece.piece_type == PieceType.King:
            moves = self.attack_tables.get_king_attack(index, not_in_bounds, zero)
        elif piece.piece_type == PieceType.Pawn:
            moves = self.attack_tables.get_north_pawn_attack(index, not_in_bounds, zero)
        elif piece.piece_type == PieceType.Custom:
            mp = position.get_movement_pattern(piece.piece_type)
            if mp is None:
                return 0
            slides = self.attack_tables.get_sliding_moves_bb(
                index,
                not_in_bounds,
                mp.translate_north or mp.attack_north,
                mp.translate_east or mp.attack_east,
                mp.translate_south or mp.attack_south,
                mp.translate_west or mp.attack_west,
                mp.translate_northeast or mp.attack_northeast,
                mp.translate_northwest or mp.attack_northwest,
                mp.translate_southeast or mp.attack_southeast,
                mp.translate_southwest or mp.attack_southwest
            )
            for dx, dy in mp.translate_jump_deltas + mp.attack_jump_deltas:
                x2, y2 = x + dx, y + dy
                if x2 < 0 or y2 < 0 or x2 > 15 or y2 > 15:
                    continue
                to = to_index(x2, y2)
                if bounds.bit(to):
                    slides.set_bit(to, True)
            for run in mp.attack_sliding_deltas + mp.translate_sliding_deltas:
                for dx, dy in run:
                    x2, y2 = x + dx, y + dy
                    if x2 < 0 or y2 < 0 or x2 > 15 or y2 > 15:
                        break
                    to = to_index(x2, y2)
                    if not bounds.bit(to):
                        break
                    slides.set_bit(to, True)
            moves = slides
        moves &= bounds
        return moves.count_ones()

    def is_in_check_from_king(self, position: Position, my_player_num: int) -> bool:
        my_pieces = position.pieces[my_player_num]
        enemies = position.occupied & ~my_pieces.occupied
        occ_or_not_in_bounds = position.occupied | ~position.bounds
        enemy_pieces = position.pieces[position.whos_turn]
        enemy_pawns = enemy_pieces.pawn.bitboard
        enemy_knights = enemy_pieces.knight.bitboard
        enemy_bishops = enemy_pieces.bishop.bitboard
        enemy_queens = enemy_pieces.queen.bitboard
        enemy_rooks = enemy_pieces.rook.bitboard
        enemy_kings = enemy_pieces.king.bitboard
        loc_index = my_pieces.king.bitboard.lowest_one()
        patt = 0
        if my_player_num == 0:
            patt = self.attack_tables.get_north_pawn_attack_masked(loc_index, occ_or_not_in_bounds, enemies)
        else:
            patt = self.attack_tables.get_south_pawn_attack_masked(loc_index, occ_or_not_in_bounds, enemies)
        if patt & enemy_pawns:
            return True
        natt = self.attack_tables.get_knight_attack(loc_index, occ_or_not_in_bounds, enemies)
        if natt & enemy_knights:
            return True
        katt = self.attack_tables.get_king_attack(loc_index, occ_or_not_in_bounds, enemies)
        if katt & enemy_kings:
            return True
        ratt = self.attack_tables.get_rook_attack(loc_index, occ_or_not_in_bounds, enemies)
        if ratt & enemy_queens or ratt & enemy_rooks:
            return True
        batt = self.attack_tables.get_bishop_attack(loc_index, occ_or_not_in_bounds, enemies)
        if batt & enemy_queens or batt & enemy_bishops:
            return True
        return False

    def in_check(self, position: Position) -> bool:
        my_player_num = position.whos_turn
        in_check = False
        position.make_move(Move.null())
        if self.is_in_check_from_king(position, my_player_num):
            in_check = True
        for move_ in self.get_custom_psuedo_moves(position):
            if move_.get_is_capture() and position.piece_at(move_.get_target()).piece_type == PieceType.King:
                in_check = True
                break
        position.unmake_move()
        return in_check

    def is_move_legal(self, move_: Move, position: Position) -> bool:
        if move_.get_move_type() == MoveType.PromotionCapture or move_.get_move_type() == MoveType.Capture:
            if position.piece_at(move_.get_target()).piece_type == PieceType.King:
                return False
        my_player_num = position.whos_turn
        legality = True
        position.make_move(move_)
        if self.is_in_check_from_king(position, my_player_num):
            legality = False
        for move_ in self.get_custom_psuedo_moves(position):
            if move_.get_is_capture() and position.piece_at(move_.get_target()).piece_type == PieceType.King:
                legality = False
                break
        position.unmake_move()
        return legality

    def count_legal_moves(self, position: Position) -> int:
        nodes = 0
        for move_ in self.get_pseudo_moves(position):
            if not self.is_move_legal(move_, position):
                continue
            nodes += 1
        return nodes


class EvalTest:
    def capture_moves(self):
        pos = Position.from_fen("rnb1kbnr/ppppqppp/8/8/5P2/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1")
        movegen = MoveGenerator()
        print(pos.get_zobrist())
        print(movegen.in_check(pos))
        print(pos.get_zobrist())
        for move_ in movegen.get_capture_moves(pos):
            print(move_)
            assert move_.get_is_capture()

# To run the test, you would create an instance of EvalTest and call capture_moves method.
eval_test = EvalTest()
eval_test.capture_moves()