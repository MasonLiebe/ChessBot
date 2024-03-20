from typing import List
from bitboard import Bitboard, to_index, from_index

'''
This file handles the valid move generation for each piece. It uses the bitboard representation
of the board to generate the moves for each piece based on their movememnt patterns.
'''

'''
The MaskHandler class can be quite confusing.  The idea here is to map out the set of squares
That are in the same row, column, or diagonal as a given square.  This is done by creating lists
of bitboards that represent the squares in a certain direction FROM the index of the square in question.

For example, MaskHandler.north[16] will be a bitboard with all of the squares directly north of the 16th square
marked as a 1. In this case, the 16th square is the 1st square in the 2nd row.  So the bitboard will have
just the 0th square set to 1.
'''
class MaskHandler:
    # Handles the bitboard masks for use with the attack tables
    def __init__(self):
        self.north = [Bitboard.zero() for _ in range(256)]
        self.east = [Bitboard.zero() for _ in range(256)]
        self.south = [Bitboard.zero() for _ in range(256)]
        self.west = [Bitboard.zero() for _ in range(256)]
        self.northeast = [Bitboard.zero() for _ in range(256)]
        self.northwest = [Bitboard.zero() for _ in range(256)]
        self.southeast = [Bitboard.zero() for _ in range(256)]
        self.southwest = [Bitboard.zero() for _ in range(256)]
        self.diagonals = [Bitboard.zero() for _ in range(256)]
        self.antidiagonals = [Bitboard.zero() for _ in range(256)]
        self.left_masks = [Bitboard.zero() for _ in range(16)] # masks for the left side of a certain column, (exclusive)
        self.right_masks = [Bitboard.zero() for _ in range(16)]
        self.files = [Bitboard.zero() for _ in range(16)] # masks for just the file
        self.ranks = [Bitboard.zero() for _ in range(16)] # masks for just a rank
        self.main_diagonal = Bitboard.zero() # mask for the main diagonal
        self.zero = Bitboard.zero() # a zero bitboard
        
        # Create the left and right masks
        cumulative_left = Bitboard.zero()
        cumulative_right = Bitboard.zero()

        for i in range(16):
            new_left = Bitboard.zero()
            new_right = Bitboard.zero()
            new_left |= cumulative_left
            new_right |= cumulative_right

            for j in range(16):
                new_left.set_bit(to_index(i, j), True)
                new_right.set_bit(to_index(15 - i, j), True)

            cumulative_left |= new_left
            cumulative_right |= new_right
            self.right_masks[i] = new_right
            self.left_masks[i] = new_left

        # Iterate through indices and create the directional masks
        for x in range(16):
            for y in range(16):
                index = to_index(x, y)

                for j in range(y + 1, 16):
                    # set the bits to the north of the current square
                    self.north[index].set_bit(to_index(x, j), True)

                for j in range(y):
                    # set the bits to the south of the current square
                    self.south[index].set_bit(to_index(x, j), True)

                for j in range(x + 1, 16):
                    # set the bits to the east of the current square
                    self.east[index].set_bit(to_index(j, y), True)

                for j in range(x):
                    # set the bits to the west of the current square
                    self.west[index].set_bit(to_index(j, y), True)

                x2 = x + 1
                y2 = y + 1
                while x2 < 16 and y2 < 16:
                    # set the bits to the northeast of the current square
                    self.northeast[index].set_bit(to_index(x2, y2), True)
                    x2 += 1
                    y2 += 1

                x2 = x - 1
                y2 = y + 1
                while x2 >= 0 and y2 < 16:
                    # set the bits to the northwest of the current square
                    self.northwest[index].set_bit(to_index(x2, y2), True)
                    x2 -= 1
                    y2 += 1

                x2 = x + 1
                y2 = y - 1
                while x2 < 16 and y2 >= 0:
                    # set the bits to the southeast of the current square
                    self.southeast[index].set_bit(to_index(x2, y2), True)
                    x2 += 1
                    y2 -= 1

                x2 = x - 1
                y2 = y - 1
                while x2 >= 0 and y2 >= 0:
                    # set the bits to the southwest of the current square
                    self.southwest[index].set_bit(to_index(x2, y2), True)
                    x2 -= 1
                    y2 -= 1

                # set the bits to the diagonal of the current square
                self.diagonals[index] = self.northeast[index] ^ self.southwest[index]
                self.antidiagonals[index] = self.northwest[index] ^ self.southeast[index]

        # Create the main_diagonal mask
        self.main_diagonal = Bitboard.one() ^ self.northeast[0]

        # Create the file and rank masks
        for i in range(16):
            file = Bitboard.zero()
            for y in range(16):
                file.set_bit(to_index(i, y), True)
            self.files[i] = file

            rank = Bitboard.zero()
            for x in range(16):
                rank.set_bit(to_index(x, i), True)
            self.ranks[i] = rank

    # Mask getters
    def get_right_mask(self, num_cols):
        if num_cols == 0:
            return self.zero
        return self.right_masks[num_cols - 1]

    def get_left_mask(self, num_cols):
        if num_cols == 0:
            return self.zero
        return self.left_masks[num_cols - 1]

    def get_main_diagonal(self):
        return self.main_diagonal

    def get_diagonal(self, index):
        return self.diagonals[index]

    def get_north(self, index):
        return self.north[index]

    def get_south(self, index):
        return self.south[index]

    def get_east(self, index):
        return self.east[index]

    def get_west(self, index):
        return self.west[index]

    def get_northwest(self, index):
        return self.northwest[index]

    def get_northeast(self, index):
        return self.northeast[index]

    def get_southeast(self, index):
        return self.southeast[index]

    def get_southwest(self, index):
        return self.southwest[index]

    def get_antidiagonal(self, index):
        return self.antidiagonals[index]

    def get_file(self, n):
        return self.files[n]

    def get_rank(self, n):
        return self.ranks[n]

    # Shifters
    def shift_north(self, amt, bitboard):
        return bitboard << (amt * 16)

    def shift_south(self, amt, bitboard):
        return bitboard >> (amt * 16)

    def shift_east(self, amt, bitboard):
        return (bitboard << amt) & (~self.get_left_mask(amt))

    def shift_west(self, amt, bitboard):
        return (bitboard >> amt) & (~self.get_right_mask(amt))


'''
The AttackTables class is used to generate the attack tables for each piece.  It holds precomputed
attack tables for the pieces, assuming a 16x16 size board, only for the standard pieceset.
'''
class AttackTables:
    def __init__(self):
        self.slider_attacks: List[List[int]] = [[0] * 65536 for _ in range(16)] 
        self.knight_attacks: List[Bitboard] = [Bitboard.zero() for _ in range(256)]
        self.king_attacks: List[Bitboard] = [Bitboard.zero() for _ in range(256)]
        self.north_pawn_attacks: List[Bitboard] = [Bitboard.zero() for _ in range(256)]
        self.north_pawn_single_push: List[Bitboard] = [Bitboard.zero() for _ in range(256)]
        self.north_pawn_double_push: List[Bitboard] = [Bitboard.zero() for _ in range(256)]
        self.south_pawn_attacks: List[Bitboard] = [Bitboard.zero() for _ in range(256)]
        self.south_pawn_single_push: List[Bitboard] = [Bitboard.zero() for _ in range(256)]
        self.south_pawn_double_push: List[Bitboard] = [Bitboard.zero() for _ in range(256)]
        self.masks: MaskHandler = MaskHandler()

        for x in range(16):
            for y in range(16):
                index = to_index(x, y)
                if y != 15:
                    self.north_pawn_single_push[index].set_bit(to_index(x, y + 1), True)
                    self.north_pawn_double_push[index].set_bit(to_index(x, y + 1), True)
                    if y + 2 < 16:
                        self.north_pawn_double_push[index].set_bit(to_index(x, y + 2), True)
                    if x + 1 < 16:
                        self.north_pawn_attacks[index].set_bit(to_index(x + 1, y + 1), True)
                    if x - 1 >= 0:
                        self.north_pawn_attacks[index].set_bit(to_index(x - 1, y + 1), True)

                if y != 0:
                    self.south_pawn_single_push[index].set_bit(to_index(x, y - 1), True)
                    self.south_pawn_double_push[index].set_bit(to_index(x, y - 1), True)
                    if y - 2 >= 0:
                        self.south_pawn_double_push[index].set_bit(to_index(x, y - 2), True)
                    if x + 1 < 16:
                        self.south_pawn_attacks[index].set_bit(to_index(x + 1, y - 1), True)
                    if x - 1 >= 0:
                        self.south_pawn_attacks[index].set_bit(to_index(x - 1, y - 1), True)

                king_deltas = [(0, 1), (0, -1), (-1, 0), (1, 0),
                               (1, 1), (1, -1), (-1, 1), (-1, -1)]

                for delta in king_deltas:
                    x2 = delta[0] + x
                    y2 = delta[1] + y
                    if 0 <= x2 < 16 and 0 <= y2 < 16:
                        self.king_attacks[index].set_bit(to_index(x2, y2), True)

                knight_deltas = [(2, 1), (2, -1), (-2, 1), (-2, -1),
                                 (1, 2), (1, -2), (-1, 2), (-1, -2)]

                for delta in knight_deltas:
                    x2 = delta[0] + x
                    y2 = delta[1] + y
                    if 0 <= x2 < 16 and 0 <= y2 < 16:
                        self.knight_attacks[index].set_bit(to_index(x2, y2), True)

        for i in range(16):
            for occ in range(65536):
                sq = 1 << i

                def get_left_attack(src):
                    return src - 1 if src != 0 else 0

                def get_right_attack(src):
                    return ~src & ~get_left_attack(src)

                left_attack = get_left_attack(sq)
                left_blockers = occ & left_attack
                if left_blockers != 0:
                    msb_blockers = 1 << (15 - left_blockers.bit_length() + 1)
                    left_attack ^= get_left_attack(msb_blockers)

                right_attack = get_right_attack(sq)
                right_blockers = occ & right_attack
                if right_blockers != 0:
                    lsb_blockers = 1 << right_blockers.bit_length() - 1
                    right_attack ^= get_right_attack(lsb_blockers)

                self.slider_attacks[i][occ] = right_attack ^ left_attack

    def get_rank_attack(self, loc_index, occ):
        x, y = from_index(loc_index)
        rank_only = self.masks.shift_south(y, occ)
        first_byte = rank_only.byte(0)
        second_byte = rank_only.byte(1)
        occ_index = (second_byte << 8) ^ first_byte
        attack = self.slider_attacks[x][occ_index]
        return_bb = Bitboard.zero()
        return_bb ^= attack
        return self.masks.shift_north(y, return_bb)

    def get_file_attack(self, loc_index, occ):
        x, y = from_index(loc_index)
        a_shifted = self.masks.shift_west(x, occ) & self.masks.get_file(0)
        first_rank = self.masks.shift_south(15, a_shifted * self.masks.get_main_diagonal())
        occ_index = first_rank.byte(0) ^ (first_rank.byte(1) << 8)
        rank_index = 15 - y
        attack = self.slider_attacks[rank_index][occ_index]
        return_bb = Bitboard.zero()
        return_bb ^= attack
        last_file = self.masks.get_right_mask(1) & (return_bb * self.masks.get_main_diagonal())
        return self.masks.shift_west(15 - x, last_file)

    def get_diagonal_attack(self, loc_index, occ):
        x, _ = from_index(loc_index)
        masked_diag = occ & self.masks.get_diagonal(loc_index)
        last_rank_with_garbage = masked_diag * self.masks.get_file(0)
        first_rank = self.masks.shift_south(15, last_rank_with_garbage)
        occ_index = first_rank.byte(0) ^ (first_rank.byte(1) << 8)
        attack = self.slider_attacks[x][occ_index]
        return_bb = Bitboard.zero()
        return_bb ^= attack
        return return_bb * self.masks.get_file(0) & self.masks.get_diagonal(loc_index)

    def get_antidiagonal_attack(self, loc_index, occ):
        x, _ = from_index(loc_index)
        masked_diag = occ & self.masks.get_antidiagonal(loc_index)
        last_rank_with_garbage = masked_diag * self.masks.get_file(0)
        first_rank = self.masks.shift_south(15, last_rank_with_garbage)
        occ_index = first_rank.byte(0) ^ (first_rank.byte(1) << 8)
        attack = self.slider_attacks[x][occ_index]
        return_bb = Bitboard.zero()
        return_bb ^= attack
        return return_bb * self.masks.get_file(0) & self.masks.get_antidiagonal(loc_index)

    def get_knight_attack(self, loc_index, _occ, _enemies):
        return self.knight_attacks[loc_index].copy()

    def get_king_attack(self, loc_index, _occ, _enemies):
        return self.king_attacks[loc_index].copy()

    def get_north_pawn_attack(self, loc_index, occ, enemies):
        x, y = from_index(loc_index)
        if y == 1 and not occ.bit(to_index(x, y + 1)):
            return_bb = self.north_pawn_double_push[loc_index] & ~occ
        else:
            return_bb = self.north_pawn_single_push[loc_index] & ~occ
        return return_bb ^ (self.north_pawn_attacks[loc_index] & enemies)

    def get_south_pawn_attack(self, loc_index, occ, enemies):
        x, y = from_index(loc_index)
        if y == 6 and not occ.bit(to_index(x, y - 1)):
            return_bb = self.south_pawn_double_push[loc_index] & ~occ
        else:
            return_bb = self.south_pawn_single_push[loc_index] & ~occ
        return return_bb ^ (self.south_pawn_attacks[loc_index] & enemies)

    def get_south_pawn_attack_masked(self, loc_index, _occ, enemies):
        return self.south_pawn_attacks[loc_index] & enemies

    def get_north_pawn_attack_masked(self, loc_index, _occ, enemies):
        return self.north_pawn_attacks[loc_index] & enemies

    def get_north_pawn_attack_raw(self, loc_index):
        return self.north_pawn_attacks[loc_index]

    def get_south_pawn_attack_raw(self, loc_index):
        return self.south_pawn_attacks[loc_index]

    def get_sliding_moves_bb(self, loc_index, occ, north, east, south, west, northeast, northwest, southeast, southwest):
        raw_attacks = Bitboard.zero()
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

    def get_rook_attack(self, loc_index, occ, _enemies):
        return self.get_file_attack(loc_index, occ) ^ self.get_rank_attack(loc_index, occ)

    def get_bishop_attack(self, loc_index, occ, _enemies):
        return self.get_diagonal_attack(loc_index, occ) ^ self.get_antidiagonal_attack(loc_index, occ)

    def get_queen_attack(self, loc_index, occ, enemies):
        return self.get_rook_attack(loc_index, occ, enemies) ^ self.get_bishop_attack(loc_index, occ, enemies)