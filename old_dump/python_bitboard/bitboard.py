# declares a bitboard class and its methods
# A bitboard is a 256-bit integer that represents one bit of information
# for each square on a chess board. This is a very efficient way to store
# the state of a chess board and perform operations on it.

# A board class will consisist of a bitboard for each piece type, where
# a 1 in the bitboard represents the presence of a piece of that type
# in that square, a bitboard for each color, where a 1 in the bitboard

'''
[]
'''

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
        self.value |= ((1 << (16 * y)) - 1) ^ ((1 << 256) - 1) 
    
    def set_col_bound(self, x):
        # set all squares to the right of a certain column
        if not (0 <= x < 16):
            raise ValueError('Column out of range')
        for y in range(16):
            self.value |= (((1 << (16 - x)) - 1) << x) << (16 * y)

    def set_index(self, index):
        self.value |= 1 << index
    
    def clear_index(self, index):
        self.value &= ~(1 << index)
    
    def get_index(self, index):
        return (self.value >> index) & 1
    
    def zero(self):
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
    
    def __eq__(self, other):
        return self.value == other.value
    
    def __ne__(self, other):
        return self.value != other.value
    
    def __and__(self, other):
        return Bitboard(self.value & other.value)
    
    def __or__(self, other):
        return Bitboard(self.value | other.value)
    
    def __xor__(self, other):
        return Bitboard(self.value ^ other.value)
    
    def __invert__(self):
        return Bitboard(~self.value)
    
    def __lshift__(self, n):
        return Bitboard(self.value << n)
    
    def __rshift__(self, n):
        return Bitboard(self.value >> n)


def to_rank_file(x, y):
    return_string = ""
    return_string += chr(x + 65)
    return_string += str(y + 1)
    return return_string

def from_index(index):
    return (index % 16, index // 16)

def to_index(x, y):
    return 16 * y + x

# testing
if __name__ == '__main__':
    print (to_rank_file(0,0))
    print (to_rank_file(7,7))
    print (to_rank_file(15,15))
    print (from_index(0))
    print (from_index(37))
    print (to_index(0,0))


    # test_bitboard = Bitboard()
    # print("This should be clear:\n ",str(test_bitboard))
    # test_bitboard.set_coord(0,6) # set the 7th square to 1
    # test_bitboard.set_coord(4,2)
    # test_bitboard.set_coord(0,0)
    # print("This should have 3 squares set:\n",test_bitboard)

    # test_bitboard.clear_coord(0,6) # clear the 7th square
    # print("This should have 2 squares set:\n",test_bitboard)
    # test_bitboard.set_row_bound(3) # set all squares below the 4th row to 1
    # print("This should have all squares below the 4th row set:\n",test_bitboard)
    # test_bitboard.set_col_bound(3) # set all squares to the right of the 4th column to 1
    # print("This should have all squares to the right of the 4th column set:\n",test_bitboard)
    # test_bitboard.zero()

    # print("This should be clear:\n",test_bitboard) 
    # test_bitboard.fill()
    # print("This should be full:")
    # print(test_bitboard)
    # test_bitboard.zero()

    # for i in range(16):
    #     test_bitboard.set_coord(i, i)
    # print("This should have the main diagonal set:")
    # print(test_bitboard)

    # test_bitboard1 = Bitboard()
    # for i in range(16):
    #     test_bitboard1.set_coord(15-i, i)
    # print("This should have the other diagonal set:")
    # print(test_bitboard1)

    # print("This should have both diagonals set:")
    # print(test_bitboard | test_bitboard1)

    # print("This should be empty:")
    # print(test_bitboard & test_bitboard1)


    
