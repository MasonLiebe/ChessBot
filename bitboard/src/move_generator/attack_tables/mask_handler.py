from bitboard.src.types.bitboard import to_index

class MaskHandler:
    def __init__(self):
        self.north = [0] * 256
        self.east = [0] * 256
        self.south = [0] * 256
        self.west = [0] * 256
        self.northeast = [0] * 256
        self.northwest = [0] * 256
        self.southeast = [0] * 256
        self.southwest = [0] * 256
        self.diagonals = [0] * 256
        self.antidiagonals = [0] * 256
        self.left_masks = [0] * 16
        self.right_masks = [0] * 16
        self.files = [0] * 16
        self.ranks = [0] * 16
        self.main_diagonal = 1
        self.zero = 0

        cumulative_left = 0
        cumulative_right = 0
        for i in range(16):
            new_left = 0
            new_right = 0
            new_left |= cumulative_left
            new_right |= cumulative_right
            for j in range(16):
                new_left |= (1 << to_index(i, j))
                new_right |= (1 << to_index(16 - i - 1, j))
            cumulative_left |= new_left
            cumulative_right |= new_right
            self.right_masks[i] = new_right
            self.left_masks[i] = new_left

        for x in range(16):
            for y in range(16):
                index = to_index(x, y)
                # NORTH LOOKUP TABLE
                for j in range(y + 1, 16):
                    self.north[index] |= (1 << to_index(x, j))
                # SOUTH LOOKUP TABLE
                for j in range(y):
                    self.south[index] |= (1 << to_index(x, j))
                # EAST LOOKUP TABLE
                for j in range(x + 1, 16):
                    self.east[index] |= (1 << to_index(j, y))
                # WEST LOOKUP TABLE
                for j in range(x):
                    self.west[index] |= (1 << to_index(j, y))
                # NORTHEAST LOOKUP TABLE
                x2 = x + 1
                y2 = y + 1
                while x2 < 16 and y2 < 16:
                    self.northeast[index] |= (1 << to_index(x2, y2))
                    x2 += 1
                    y2 += 1
                # NORTHWEST LOOKUP TABLE
                x2 = x - 1
                y2 = y + 1
                while x2 >= 0 and y2 < 16:
                    self.northwest[index] |= (1 << to_index(x2, y2))
                    x2 -= 1
                    y2 += 1
                # SOUTHEAST LOOKUP TABLE
                x2 = x + 1
                y2 = y - 1
                while x2 < 16 and y2 >= 0:
                    self.southeast[index] |= (1 << to_index(x2, y2))
                    x2 += 1
                    y2 -= 1
                # SOUTHWEST LOOKUP TABLE
                x2 = x - 1
                y2 = y - 1
                while x2 >= 0 and y2 >= 0:
                    self.southwest[index] |= (1 << to_index(x2, y2))
                    x2 -= 1
                    y2 -= 1
                self.diagonals[index] = self.northeast[index] ^ self.southwest[index]
                self.antidiagonals[index] = self.northwest[index] ^ self.southeast[index]

        self.main_diagonal ^= self.northeast[0]

        for i in range(16):
            file = 0
            for y in range(16):
                file |= (1 << to_index(i, y))
            self.files[i] = file

            rank = 0
            for x in range(16):
                rank |= (1 << to_index(x, i))
            self.ranks[i] = rank

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

    def shift_north(self, amt, bitboard):
        return bitboard << (amt * 16)

    def shift_south(self, amt, bitboard):
        return bitboard >> (amt * 16)

    def shift_east(self, amt, bitboard):
        return (bitboard << amt) & (~self.get_left_mask(amt))

    def shift_west(self, amt, bitboard):
        return (bitboard >> amt) & (~self.get_right_mask(amt))


