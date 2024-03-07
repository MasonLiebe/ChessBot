import array
from typing import List
from mask_handler import MaskHandler

from bitboard.src.types.bitboard import Bitboard, to_index, from_index

class AttackTables:
    def __init__(self):
        self.slider_attacks: List[List[int]] = [[0] * 65536 for _ in range(16)]
        self.knight_attacks = array.array('Q', [0] * 256)
        self.king_attacks = array.array('Q', [0] * 256)
        self.north_pawn_attacks = array.array('Q', [0] * 256)
        self.north_pawn_single_push = array.array('Q', [0] * 256)
        self.north_pawn_double_push = array.array('Q', [0] * 256)
        self.south_pawn_attacks = array.array('Q', [0] * 256)
        self.south_pawn_single_push = array.array('Q', [0] * 256)
        self.south_pawn_double_push = array.array('Q', [0] * 256)
        self.masks = MaskHandler()

    def new(self) -> None:
        knight_attacks = array.array('Q', [0] * 256)
        king_attacks = array.array('Q', [0] * 256)
        north_pawn_attacks = array.array('Q', [0] * 256)
        north_pawn_single_push = array.array('Q', [0] * 256)
        north_pawn_double_push = array.array('Q', [0] * 256)
        south_pawn_attacks = array.array('Q', [0] * 256)
        south_pawn_single_push = array.array('Q', [0] * 256)
        south_pawn_double_push = array.array('Q', [0] * 256)
        for x in range(16):
            for y in range(16):
                index = self.to_index(x, y)
                # PAWN
                if y != 15:
                    north_pawn_single_push[index] |= 1 << self.to_index(x, y + 1)
                    north_pawn_double_push[index] |= 1 << self.to_index(x, y + 1)
                    if y + 2 < 16:
                        north_pawn_double_push[index] |= 1 << self.to_index(x, y + 2)
                    if x + 1 < 16:
                        north_pawn_attacks[index] |= 1 << self.to_index(x + 1, y + 1)
                    if x - 1 >= 0:
                        north_pawn_attacks[index] |= 1 << self.to_index(x - 1, y + 1)
                if y != 0:
                    south_pawn_single_push[index] |= 1 << self.to_index(x, y - 1)
                    south_pawn_double_push[index] |= 1 << self.to_index(x, y - 1)
                    if y - 2 >= 0:
                        south_pawn_double_push[index] |= 1 << self.to_index(x, y - 2)
                    if x + 1 < 16:
                        south_pawn_attacks[index] |= 1 << self.to_index(x + 1, y - 1)
                    if x - 1 >= 0:
                        south_pawn_attacks[index] |= 1 << self.to_index(x - 1, y - 1)
                # KING LOOKUP TABLE
                king_deltas = [(0, 1), (0, -1), (-1, 0), (1, 0),
                               (1, 1), (1, -1), (-1, 1), (-1, -1)]
                for delta in king_deltas:
                    x2 = delta[0] + x
                    y2 = delta[1] + y
                    if 0 <= x2 < 16 and 0 <= y2 < 16:
                        king_attacks[index] |= 1 << self.to_index(x2, y2)
                # KNIGHT LOOKUP TABLE
                knight_deltas = [(2, 1), (2, -1), (-2, 1), (-2, -1),
                                 (1, 2), (1, -2), (-1, 2), (-1, -2)]
                for delta in knight_deltas:
                    x2 = delta[0] + x
                    y2 = delta[1] + y
                    if 0 <= x2 < 16 and 0 <= y2 < 16:
                        knight_attacks[index] |= 1 << self.to_index(x2, y2)
        # 16 * 2^16 possible states; 16 squares in 1 rank, 2^16 possible occupancies per rank
        slider_attacks = [[0] * 65536 for _ in range(16)]
        for i in range(16):
            for occ in range(65536):
                sq = 1 << i
                def get_left_attack(src):
                    if src == 0:
                        return 0
                    else:
                        return src - 1
                def get_right_attack(src):
                    return ~src & ~get_left_attack(src)
                left_attack = get_left_attack(sq)
                left_blockers = occ & left_attack
                if left_blockers != 0:
                    msb_blockers = 1 << (15 - left_blockers.bit_length())
                    left_attack ^= get_left_attack(msb_blockers)
                right_attack = get_right_attack(sq)
                right_blockers = occ & right_attack
                if right_blockers != 0:
                    lsb_blockers = 1 << right_blockers.bit_length() - 1
                    right_attack ^= get_right_attack(lsb_blockers)
                slider_attacks[i][occ] = right_attack ^ left_attack
        self.slider_attacks = slider_attacks
        self.knight_attacks = knight_attacks
        self.king_attacks = king_attacks
        self.north_pawn_attacks = north_pawn_attacks
        self.north_pawn_single_push = north_pawn_single_push
        self.north_pawn_double_push = north_pawn_double_push
        self.south_pawn_attacks = south_pawn_attacks
        self.south_pawn_single_push = south_pawn_single_push
        self.south_pawn_double_push = south_pawn_double_push
        self.masks = MaskHandler()

    def to_index(self, x: int, y: int) -> int:
        return y * 16 + x

    def get_rank_attack(self, loc_index: int, occ: Bitboard) -> Bitboard:
        x, y = self.from_index(loc_index)
        rank_only = self.masks.shift_south(y, occ)
        first_byte = rank_only & 0xFF
        second_byte = (rank_only >> 8) & 0xFF
        occ_index = second_byte << 8 ^ first_byte
        attack = self.slider_attacks[x][occ_index]
        return_bb = attack
        return_bb ^= self.masks.shift_north(y, return_bb)
        return return_bb

    def get_file_attack(self, loc_index: int, occ: Bitboard) -> Bitboard:
        x, y = self.from_index(loc_index)
        a_shifted = self.masks.shift_west(x, occ) & self.masks.get_file(0)
        first_rank = self.masks.shift_south(15, a_shifted * self.masks.get_main_diagonal())
        occ_index = first_rank & 0xFF ^ (first_rank >> 8) & 0xFF
        rank_index = 15 - y
        attack = self.slider_attacks[rank_index][occ_index]
        return_bb = attack
        last_file = self.masks.get_right_mask(1) & (return_bb * self.masks.get_main_diagonal())
        return self.masks.shift_west(15 - x, last_file)

    def get_diagonal_attack(self, loc_index: int, occ: Bitboard) -> Bitboard:
        x, _y = self.from_index(loc_index)
        masked_diag = occ & self.masks.get_diagonal(loc_index)
        last_rank_with_garbage = masked_diag * self.masks.get_file(0)
        first_rank = self.masks.shift_south(15, last_rank_with_garbage)
        occ_index = first_rank & 0xFF ^ (first_rank >> 8) & 0xFF
        attack = self.slider_attacks[x][occ_index]
        return_bb = attack
        return_bb *= self.masks.get_file(0)
        return_bb &= self.masks.get_diagonal(loc_index)
        return return_bb

    def get_antidiagonal_attack(self, loc_index: int, occ: Bitboard) -> Bitboard:
        x, _y = self.from_index(loc_index)
        masked_diag = occ & self.masks.get_antidiagonal(loc_index)
        last_rank_with_garbage = masked_diag * self.masks.get_file(0)
        first_rank = self.masks.shift_south(15, last_rank_with_garbage)
        occ_index = first_rank & 0xFF ^ (first_rank >> 8) & 0xFF
        attack = self.slider_attacks[x][occ_index]
        return_bb = attack
        return_bb *= self.masks.get_file(0)
        return_bb &= self.masks.get_antidiagonal(loc_index)
        return return_bb

    def get_knight_attack(self, loc_index: int, _occ: Bitboard, _enemies: Bitboard) -> Bitboard:
        return self.knight_attacks[loc_index]

    def get_king_attack(self, loc_index: int, _occ: Bitboard, _enemies: Bitboard) -> Bitboard:
        return self.king_attacks[loc_index]

    def get_north_pawn_attack(self, loc_index: int, occ: Bitboard, enemies: Bitboard) -> Bitboard:
        x, y = self.from_index(loc_index)
        if y == 1 and not occ.bit(self.to_index(x, y + 1)):
            return_bb = self.north_pawn_double_push[loc_index] & ~occ
        else:
            return_bb = self.north_pawn_single_push[loc_index] & ~occ
        return_bb ^= self.north_pawn_attacks[loc_index] & enemies
        return return_bb

    def get_south_pawn_attack(self, loc_index: int, occ: Bitboard, enemies: Bitboard) -> Bitboard:
        x, y = self.from_index(loc_index)
        if y == 6 and not occ.bit(self.to_index(x, y - 1)):
            return_bb = self.south_pawn_double_push[loc_index] & ~occ
        else:
            return_bb = self.south_pawn_single_push[loc_index] & ~occ
        return_bb ^= self.south_pawn_attacks[loc_index] & enemies
        return return_bb

    def get_south_pawn_attack_masked(self, loc_index: int, _occ: Bitboard, enemies: Bitboard) -> Bitboard:
        return self.south_pawn_attacks[loc_index] & enemies

    def get_north_pawn_attack_masked(self, loc_index: int, _occ: Bitboard, enemies: Bitboard) -> Bitboard:
        return self.north_pawn_attacks[loc_index] & enemies

    def get_north_pawn_attack_raw(self, loc_index: int) -> Bitboard:
        return self.north_pawn_attacks[loc_index]

    def get_south_pawn_attack_raw(self, loc_index: int) -> Bitboard:
        return self.south_pawn_attacks[loc_index]

    def get_sliding_moves_bb(self, loc_index: int, occ: Bitboard, north: bool, east: bool, south: bool, west: bool, northeast: bool, northwest: bool, southeast: bool, southwest: bool) -> Bitboard:
        raw_attacks = Bitboard()
        if north or south:
            raw_attacks |= self.get_file_attack(loc_index, occ)
            if not north:
                raw_attacks &= ~self.masks.get_north(loc_index)
            elif not south:
                raw_attacks &= ~self.masks.get_south(loc_index)
        if east or west:
            raw_attacks |= self.get_rank_attack(loc_index, occ)
            if not east:
                raw_attacks &= ~self.masks.get_east(loc_index)
            elif not west:
                raw_attacks &= ~self.masks.get_west(loc_index)
        if northeast or southwest:
            raw_attacks |= self.get_diagonal_attack(loc_index, occ)
            if not northeast:
                raw_attacks &= ~self.masks.get_northeast(loc_index)
            elif not southwest:
                raw_attacks &= ~self.masks.get_southwest(loc_index)
        if northwest or southeast:
            raw_attacks |= self.get_antidiagonal_attack(loc_index, occ)
            if not northwest:
                raw_attacks &= ~self.masks.get_northwest(loc_index)
            elif not southeast:
                raw_attacks &= ~self.masks.get_southeast(loc_index)
        return raw_attacks

    def get_rook_attack(self, loc_index: int, occ: Bitboard, _enemies: Bitboard) -> Bitboard:
        return self.get_file_attack(loc_index, occ) ^ self.get_rank_attack(loc_index, occ)

    def get_bishop_attack(self, loc_index: int, occ: Bitboard, _enemies: Bitboard) -> Bitboard:
        return self.get_diagonal_attack(loc_index, occ) ^ self.get_antidiagonal_attack(loc_index, occ)

    def get_queen_attack(self, loc_index: int, occ: Bitboard, enemies: Bitboard) -> Bitboard:
        return self.get_rook_attack(loc_index, occ, enemies) ^ self.get_bishop_attack(loc_index, occ, enemies)

    def from_index(self, loc_index: int) -> tuple:
        return loc_index % 16, loc_index // 16

    def test(self) -> None:
        attacktb = AttackTables()
        bb = Bitboard()
        bb |= 9252345218324798
        print(f"occ \n{bb.to_string()}")
        # rankatt = attacktb.get_rank_attack(2,&bb)
        # print(f"{rankatt.to_string()}")

attacktb = AttackTables()
attacktb.new()
attacktb.test()


