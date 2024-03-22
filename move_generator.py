from bitboard import Bitboard
from move import Move, MoveType, PieceType
from typing import Optional, List
from attack_tables import AttackTables, MaskHandler
from bitboard import Bitboard, from_index, to_index
from position import Position
from typing import List, Tuple, Iterator
from itertools import chain
from piece import Piece

class BitboardMoves:
    def __init__(self, enemies: Bitboard, moves: Bitboard, source_index: int,
                 promotion_squares: Optional[Bitboard], promo_vals: Optional[List[str]]):
        self.enemies = enemies
        self.moves = moves
        self.source_index = source_index
        self.promotion_squares = promotion_squares
        self.promo_vals = promo_vals
        self.current_promo_vals: Optional[List[str]] = None

    def __iter__(self):
        return self

    def __next__(self) -> Move:
        if (to := self.moves.lowest_one()) >= 0:
            promo_here = self.promotion_squares.bit(to) if self.promotion_squares else False
            capture_here = self.enemies.bit(to)

            move_type = {
                (True, True): "PromotionCapture",
                (True, False): "Capture",
                (False, True): "Promotion",
                (False, False): "Quiet",
            }[(capture_here, promo_here)]

            target = to if capture_here else 0

            if promo_here:
                if self.current_promo_vals:
                    promo_options = self.current_promo_vals
                else:
                    self.current_promo_vals = self.promo_vals.copy() if self.promo_vals else None
                    promo_options = self.current_promo_vals

                next_char = promo_options.pop()

                if len(promo_options) == 0:
                    self.current_promo_vals = None
                    self.moves.set_bit(to, False)

                promo_char = next_char
            else:
                self.moves.set_bit(to, False)
                promo_char = None

            return Move.new(self.source_index, to, target, move_type, promo_char)
        else:
            raise StopIteration

# MOVE GENERATOR CLASS BELOW
        
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

    def get_pseudo_moves(self, position: Position) -> Iterator[Move]:
        return chain(self.get_classical_pseudo_moves(position), self.get_custom_psuedo_moves(position))

    def get_capture_moves(self, position: Position) -> Iterator[Move]:
        return chain(
            filter(lambda x: x.get_is_capture(), self.get_classical_pseudo_moves(position)),
            filter(lambda x: x.get_is_capture(), self.get_custom_psuedo_moves(position))
        )

    def get_classical_pseudo_moves(self, position: Position) -> Iterator[Move]:
        my_pieces = position.pieces[position.whos_turn]
        enemies = position.occupied & ~my_pieces.occupied

        iters: List[BitboardMoves] = []
        occ_or_not_in_bounds = position.occupied | ~position.bounds

        def apply_to_each(pieceset: Bitboard, func):
            while not pieceset.is_zero():
                index = pieceset.lowest_one()
                raw_attacks = func(self.attack_tables, index, occ_or_not_in_bounds, enemies)
                raw_attacks &= ~my_pieces.occupied
                raw_attacks &= position.bounds
                iters.append(BitboardMoves(enemies.copy(), raw_attacks, index, None, None))
                pieceset.set_bit(index, False)

        apply_to_each(my_pieces.king.bitboard.copy(), AttackTables.get_king_attack)
        apply_to_each(my_pieces.queen.bitboard.copy(), AttackTables.get_queen_attack)
        apply_to_each(my_pieces.rook.bitboard.copy(), AttackTables.get_rook_attack)
        apply_to_each(my_pieces.bishop.bitboard.copy(), AttackTables.get_bishop_attack)
        apply_to_each(my_pieces.knight.bitboard.copy(), AttackTables.get_knight_attack)

        extra_moves = []
        p_copy = my_pieces.pawn.bitboard.copy()
        while not p_copy.is_zero():
            index = p_copy.lowest_one()
            raw_attacks = (
                self.attack_tables.get_north_pawn_attack(index, position.occupied, enemies)
                if position.whos_turn == 0
                else self.attack_tables.get_south_pawn_attack(index, position.occupied, enemies)
            )
            raw_attacks &= ~my_pieces.occupied
            raw_attacks &= position.bounds
            promotion_squares = (
                self.attack_tables.masks.get_rank(position.dimensions.height - 1).copy()
                if position.whos_turn == 0
                else self.attack_tables.masks.get_rank(0).copy()
            )
            promo_vals = ['r', 'b', 'n', 'q']
            iters.append(BitboardMoves(enemies.copy(), raw_attacks, index, promotion_squares, promo_vals))

            if position.properties.ep_square is not None:
                ep_sq = position.properties.ep_square
                attack_only = (
                    self.attack_tables.get_north_pawn_attack_raw(index) & ~my_pieces.occupied
                    if position.whos_turn == 0
                    else self.attack_tables.get_south_pawn_attack_raw(index) & ~my_pieces.occupied
                )
                if attack_only.bit(ep_sq):
                    cap_x, cap_y = from_index(ep_sq)
                    if position.whos_turn == 0:
                        cap_y -= 1
                    else:
                        cap_y += 1
                    move_ = Move.new(index, ep_sq, to_index(cap_x, cap_y), 'Capture', None)
                    extra_moves.append(move_)
            p_copy.set_bit(index, False)

        if my_pieces.king.bitboard.lowest_one() is not None:
            king_index = my_pieces.king.bitboard.lowest_one()
            kx, ky = from_index(king_index)
            whos_turn = position.whos_turn
            if position.properties.castling_rights.can_player_castle_kingside(position.whos_turn):
                rook_index = to_index(position.dimensions.width - 1, ky)
                piece_info = position.piece_at(rook_index)
                if piece_info is not None:
                    owner, pt = piece_info
                    if owner == whos_turn and pt.piece_type == PieceType.Rook:
                        east = self.attack_tables.masks.get_east(king_index)
                        occ = east & position.occupied
                        occ.set_bit(rook_index, False)
                        if occ.is_zero():
                            king_one_step_indx = to_index(kx + 1, ky)
                            if self.is_move_legal(Move.null(), position) and self.is_move_legal(
                                Move.new(king_index, king_one_step_indx, None, 'Quiet', None), position
                            ):
                                to_index_ = to_index(kx + 2, ky)
                                extra_moves.append(Move.new(king_index, to_index_, rook_index, 'KingsideCastle', None))

            if position.properties.castling_rights.can_player_castle_queenside(position.whos_turn):
                rook_index = to_index(0, ky)
                piece_info = position.piece_at(rook_index)
                if piece_info is not None:
                    owner, pt = piece_info
                    if owner == whos_turn and pt.piece_type == PieceType.Rook:
                        west = self.attack_tables.masks.get_west(king_index)
                        occ = west & position.occupied
                        occ.set_bit(rook_index, False)
                        if occ.is_zero():
                            king_one_step_indx = to_index(kx - 1, ky)
                            if self.is_move_legal(Move.null(), position) and self.is_move_legal(
                                Move.new(king_index, king_one_step_indx, None, 'Quiet', None), position
                            ):
                                to_index_ = to_index(kx - 2, ky)
                                extra_moves.append(Move.new(king_index, to_index_, rook_index, 'QueensideCastle', None))

        return chain(*(iter(moves) for moves in iters), extra_moves)
        
    def get_custom_psuedo_moves(self, position: Position) -> Iterator[Move]:
        my_pieces = position.pieces[position.whos_turn]

        iters: List[BitboardMoves] = []
        moves = []

        if len(my_pieces.custom) == 0:
            return chain(*(iter(moves) for moves in iters), moves)

        enemies = position.occupied & ~my_pieces.occupied
        occ_or_not_in_bounds = position.occupied | ~position.bounds

        for p in my_pieces.custom:
            movement = position.get_movement_pattern(p.piece_type)
            if movement is None:
                continue

            bb = p.bitboard
            bb_copy = bb.copy()
            while not bb_copy.is_zero():
                index = bb_copy.lowest_one()
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
                    movement.promotion_squares.copy() if movement.promotion_squares else None,
                    movement.promo_vals.copy() if movement.promo_vals else None,
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
                    movement.promotion_squares.copy() if movement.promotion_squares else None,
                    movement.promo_vals.copy() if movement.promo_vals else None,
                ))

                x, y = from_index(index)
                for dx, dy in movement.translate_jump_deltas:
                    x2, y2 = x + dx, y + dy
                    if not (0 <= x2 < 16 and 0 <= y2 < 16):
                        continue
                    to = to_index(x2, y2)
                    if position.xy_in_bounds(x2, y2) and not position.occupied.bit(to):
                        if movement.promotion_at(to):
                            for c in movement.promo_vals:
                                moves.append(Move.new(index, to, None, 'Promotion', c))
                        else:
                            moves.append(Move.new(index, to, None, 'Quiet', None))

                for dx, dy in movement.attack_jump_deltas:
                    x2, y2 = x + dx, y + dy
                    if not (0 <= x2 < 16 and 0 <= y2 < 16):
                        continue
                    to = to_index(x2, y2)
                    if enemies.bit(to):
                        if movement.promotion_at(to):
                            for c in movement.promo_vals:
                                moves.append(Move.new(index, to, to, 'PromotionCapture', c))
                        else:
                            moves.append(Move.new(index, to, to, 'Capture', None))

                for run in movement.attack_sliding_deltas:
                    for dx, dy in run:
                        x2, y2 = x + dx, y + dy
                        if not (0 <= x2 < 16 and 0 <= y2 < 16):
                            break
                        to = to_index(x2, y2)
                        if not position.xy_in_bounds(x2, y2):
                            break
                        if enemies.bit(to):
                            if movement.promotion_at(to):
                                for c in movement.promo_vals:
                                    moves.append(Move.new(index, to, to, 'PromotionCapture', c))
                            else:
                                moves.append(Move.new(index, to, to, 'Capture', None))
                            break
                        if position.occupied.bit(to):
                            break

                for run in movement.translate_sliding_deltas:
                    for dx, dy in run:
                        x2, y2 = x + dx, y + dy
                        if not (0 <= x2 < 16 and 0 <= y2 < 16):
                            break
                        to = to_index(x2, y2)
                        if not position.xy_in_bounds(x2, y2) or position.occupied.bit(to):
                            break
                        if movement.promotion_at(to):
                            for c in movement.promo_vals:
                                moves.append(Move.new(index, to, None, 'Quiet', c))
                        else:
                            moves.append(Move.new(index, to, None, 'Quiet', None))

                bb_copy.set_bit(index, False)

        return chain(*(iter(moves) for moves in iters), moves)
    
    def get_num_moves_on_empty_board(self, index: int, position: Position, piece: Piece, bounds: Bitboard) -> int:
        x, y = from_index(index)
        if not position.xy_in_bounds(x, y):
            return 0
        zero = Bitboard.zero()
        not_in_bounds = ~position.bounds
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
        elif isinstance(piece.piece_type, PieceType.Custom):
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
            x, y = from_index(index)
            for dx, dy in chain(mp.translate_jump_deltas, mp.attack_jump_deltas):
                x2, y2 = x + dx, y + dy
                if not (0 <= x2 < 16 and 0 <= y2 < 16):
                    continue
                to = to_index(x2, y2)
                if bounds.bit(to):
                    slides.set_bit(to, True)
            for run in chain(mp.attack_sliding_deltas, mp.translate_sliding_deltas):
                for dx, dy in run:
                    x2, y2 = x + dx, y + dy
                    if not (0 <= x2 < 16 and 0 <= y2 < 16):
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

        if my_player_num == 0:
            patt = self.attack_tables.get_north_pawn_attack_masked(loc_index, occ_or_not_in_bounds, enemies)
        else:
            patt = self.attack_tables.get_south_pawn_attack_masked(loc_index, occ_or_not_in_bounds, enemies)

        if not (patt & enemy_pawns).is_zero():
            return True

        natt = self.attack_tables.get_knight_attack(loc_index, occ_or_not_in_bounds, enemies)
        if not (natt & enemy_knights).is_zero():
            return True

        katt = self.attack_tables.get_king_attack(loc_index, occ_or_not_in_bounds, enemies)
        if not (katt & enemy_kings).is_zero():
            return True

        ratt = self.attack_tables.get_rook_attack(loc_index, occ_or_not_in_bounds, enemies)
        if not (ratt & enemy_queens).is_zero() or not (ratt & enemy_rooks).is_zero():
            return True

        batt = self.attack_tables.get_bishop_attack(loc_index, occ_or_not_in_bounds, enemies)
        if not (batt & enemy_queens).is_zero() or not (batt & enemy_bishops).is_zero():
            return True

        return False

    def in_check(self, position: Position) -> bool:
        my_player_num = position.whos_turn
        in_check = False
        position.make_move(Move.null())
        if self.is_in_check_from_king(position, my_player_num):
            in_check = True
        for move_ in self.get_custom_psuedo_moves(position):
            if move_.get_is_capture() and position.piece_at(move_.get_target())[1] == PieceType.King:
                in_check = True
                break
        position.unmake_move()
        return in_check

    def is_move_legal(self, move_: Move, position: Position) -> bool:
        if move_.get_move_type() in ['PromotionCapture', 'Capture']:
            if position.piece_at(move_.get_target())[1] == PieceType.King:
                return False
        my_player_num = position.whos_turn
        legality = True
        position.make_move(move_)
        if self.is_in_check_from_king(position, my_player_num):
            legality = False
        for move_ in self.get_custom_psuedo_moves(position):
            if move_.get_is_capture() and position.piece_at(move_.get_target())[1] == PieceType.King:
                legality = False
                break
        position.unmake_move()
        return legality

    def count_legal_moves(self, position: Position) -> int:
        nodes = 0
        for move_ in self.get_pseudo_moves(position):
            print(position.piece_at(move_.get_from())[1].piece_type, move_, end=' ')
            if not self.is_move_legal(move_, position):
                print('is not legal')
                continue
            print('is legal')
            nodes += 1
        return nodes

# Testing
    
at = AttackTables()