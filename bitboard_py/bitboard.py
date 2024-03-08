# declares a bitboard class and its methods
# A bitboard is a 256-bit integer that represents one bit of information
# for each square on a chess board. This is a very efficient way to store
# the state of a chess board and perform operations on it.

# A board class will consisist of a bitboard for each piece type, where
# a 1 in the bitboard represents the presence of a piece of that type
# in that square, a bitboard for each color, where a 1 in the bitboard

class Bitboard:

    def __init__(self, value=0):
        self.value = value
    
    def set_coord(self, x, y):
        if not (0 <= x < 16 and 0 <= y < 16):
            raise ValueError('Coordinates out of range')
        square = 16 * y + x
        self.value |= 1 << square
    
    def clear_coord(self, x, y):
        if not (0 <= x < 16 and 0 <= y < 16):
            raise ValueError('Coordinates out of range')
        square = 16 * y + x
        self.value &= ~(1 << square)
    
    def get_coord(self, x, y):
        if not (0 <= x < 16 and 0 <= y < 16):
            raise ValueError('Coordinates out of range')
        square = 16 * y + x
        return (self.value >> square) & 1
    
    def set_row_bound(self, y):
        # set all squares below a certain row to 1
        if not (0 <= y < 16):
            raise ValueError('Row out of range')
        self.value |= ((1 << (16*y)) - 1) ^ ((1 << 256) - 1) 
    
    def set_col_bound(self, x):
        # set all squares to the right of a certain column
        if not (0 <= x < 16):
            raise ValueError('Column out of range')
        for y in range(16):
            self.value |= ((((1 << (16 - x)) - 1)) << (16 * y))
    
    def clear(self):
        self.value = 0
    
    def fill(self):
        self.value = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF

    def __str__(self):
        binary = bin(self.value)[2:].zfill(256)
        lines = []
        for i in range(16):
            line = ' '.join(binary[i*16+j] for j in range(15, -1, -1))
            lines.append(line)
        return '\n'.join(reversed(lines))
    
    def __repr__(self):
        return f'Bitboard(value={bin(self.value)})'

# testing 
    
if __name__ == '__main__':
    test_bitboard = Bitboard()
    print("This should be clear:\n ",str(test_bitboard))
    test_bitboard.set_coord(0,6) # set the 7th square to 1
    test_bitboard.set_coord(3,8)
    test_bitboard.set_coord(0,0)
    print("This should have 3 squares set:\n",test_bitboard)

    test_bitboard.clear_coord(0,6) # clear the 7th square
    print("This should have 2 squares set:\n",test_bitboard)
    test_bitboard.set_row_bound(3) # set all squares below the 4th row to 1
    print("This should have all squares below the 4th row set:\n",test_bitboard)
    test_bitboard.set_col_bound(3) # set all squares to the right of the 4th column to 1
    print("This should have all squares to the right of the 4th column set:\n",test_bitboard)
