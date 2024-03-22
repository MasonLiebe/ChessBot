# declares a bitboard class and its methods
# A bitboard is a 256-bit integer that represents one bit of information
# for each square on a chess board. This is a very efficient way to store
# the state of a chess board and perform operations on it.

# A board class will consisist of a bitboard for each piece type, where
# a 1 in the bitboard represents the presence of a piece of that type
# in that square, a bitboard for each color, where a 1 in the bitboard

'''
For example, here are the indexes for a 16x16 board:
16 X 16 Board
      a   b   c   d   e   f   g   h   a   b   c   d   e   f   g   h
    -----------------------------------------------------------------
16 |   0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15
15 |  16  17  18  19  20  21  22  23  24  25  26  27  28  29  30  31
14 |  32  33  34  35  36  37  38  39  40  41  42  43  44  45  46  47
13 |  48  49  50  51  52  53  54  55  56  57  58  59  60  61  62  63
12 |  64  65  66  67  68  69  70  71  72  73  74  75  76  77  78  79
11 |  80  81  82  83  84  85  86  87  88  89  90  91  92  93  94  95
10 |  96  97  98  99 100 101 102 103 104 105 106 107 108 109 110 111
 9 | 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127
 8 | 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143
 7 | 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159
 6 | 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175
 5 | 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191
 4 | 192 193 194 195 196 197 198 199 200 201 202 203 204 205 206 207
 3 | 208 209 210 211 212 213 214 215 216 217 218 219 220 221 222 223
 2 | 224 225 226 227 228 229 230 231 232 233 234 235 236 237 238 239
 1 | 240 241 242 243 244 245 246 247 248 249 250 251 252 253 254 255
    -----------------------------------------------------------------
      a   b   c   d   e   f   g   h   a   b   c   d   e   f   g   h


When a smaller board is used, it just crops the 16x16 board to the desired size.
For example, here are the indexes for an 8x8 board:
8 x 8 board
      a   b   c   d   e   f   g   h
    -------------------------------
 8 |   0   1   2   3   4   5   6   7
 7 |  16  17  18  19  20  21  22  23
 6 |  32  33  34  35  36  37  38  39
 5 |  48  49  50  51  52  53  54  55
 4 |  64  65  66  67  68  69  70  71
 3 |  80  81  82  83  84  85  86  87
 2 |  96  97  98  99 100 101 102 103
 1 | 112 113 114 115 116 117 118 119
    -------------------------------
      a   b   c   d   e   f   g   h
'''

class Bitboard:

    def __init__(self, value=0):
        self.value = value & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
    
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
    
    def set_bit(self, index, value):
        if value:
            self.set_index(index)
        else:
            self.clear_index(index)

    def bit(self, index):
        return (self.value >> index) & 1
    
    def is_zero(self):
        return self.value == 0
    
    def lowest_one(self):
        # returns the index of the lowest 1 bit
        return (self.value & -self.value).bit_length() - 1

    @classmethod
    def zero(cls):
        return Bitboard(0)
    
    def copy(self):
        return Bitboard(self.value)
    
    def fill(self):
        self.value = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
    
    def byte(self, index):
        return (self.value >> (8 * index)) & 0xFF

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
        if isinstance(other, int):
            return Bitboard(self.value ^ other)
        return Bitboard(self.value ^ other.value)
    
    def __invert__(self):
        return Bitboard(~self.value)
    
    def __lshift__(self, n):
        return Bitboard(self.value << n )
    
    def __rshift__(self, n):
        return Bitboard(self.value >> n)
    
    def __mul__ (self, other):
        if isinstance(other, int):
            return Bitboard(self.value * other)
        return Bitboard(self.value * other.value)

def to_rank_file(x, y):
    return_string = ""
    return_string += chr(x + 65)
    return_string += str(y + 1)
    return return_string

def from_index(index):
    return (index % 16, index // 16)

def to_index(x, y):
    return (16 * y + x) & 0xFF

# # testing
# if __name__ == '__main__':
#     print (to_rank_file(0,0))
#     print (to_rank_file(7,7))
#     print (to_rank_file(15,15))
#     print (from_index(0))
#     print (from_index(37))
#     print (to_index(0,0))


#     # test_bitboard = Bitboard()
#     # print("This should be clear:\n ",str(test_bitboard))
#     # test_bitboard.set_coord(0,6) # set the 7th square to 1
#     # test_bitboard.set_coord(4,2)
#     # test_bitboard.set_coord(0,0)
#     # print("This should have 3 squares set:\n",test_bitboard)

#     # test_bitboard.clear_coord(0,6) # clear the 7th square
#     # print("This should have 2 squares set:\n",test_bitboard)
#     # test_bitboard.set_row_bound(3) # set all squares below the 4th row to 1
#     # print("This should have all squares below the 4th row set:\n",test_bitboard)
#     # test_bitboard.set_col_bound(3) # set all squares to the right of the 4th column to 1
#     # print("This should have all squares to the right of the 4th column set:\n",test_bitboard)
#     # test_bitboard.zero()

#     # print("This should be clear:\n",test_bitboard) 
#     # test_bitboard.fill()
#     # print("This should be full:")
#     # print(test_bitboard)
#     # test_bitboard.zero()

#     # for i in range(16):
#     #     test_bitboard.set_coord(i, i)
#     # print("This should have the main diagonal set:")
#     # print(test_bitboard)

#     # test_bitboard1 = Bitboard()
#     # for i in range(16):
#     #     test_bitboard1.set_coord(15-i, i)
#     # print("This should have the other diagonal set:")
#     # print(test_bitboard1)

#     # print("This should have both diagonals set:")
#     # print(test_bitboard | test_bitboard1)

#     # print("This should be empty:")
#     # print(test_bitboard & test_bitboard1)


    
