from typing import Tuple

def to_index(x: int, y: int) -> int:
    return 16 * y + x

def from_index(index: int) -> Tuple[int, int]:
    return (index % 16, index // 16)

def to_string(bitboard: int) -> str:
    return_str = ""
    for y in range(15, -1, -1):
        for x in range(16):
            if bitboard & (1 << to_index(x, y)):
                return_str += '1'
            else:
                return_str += '.'
            return_str += ' '
        return_str += '\n'
    return return_str