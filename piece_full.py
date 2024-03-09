# This file contains the classes that represent the information about a piece, including its type,
# name, color, rules, promotion squares
from constants import *
from bitboard import Bitboard



# represents the set of movements for a piece
class Moveset:
    def __init__(self, n = False, s = False, e = False, w = False, ne = False, se = False,  sw = False, nw = False, capture_jumps = (), move_jumps = (), promotion = False, enpassant = False, castle = False):
        self.n = n # bools representing can slide in each direction (unlimited distance)
        self.s = s
        self.e = e
        self.w = w
        self.ne = ne
        self.se = se
        self.sw = sw
        self.nw = nw
        self.capture_jumps = capture_jumps # jumps that must capture, tuple of (x, y) tuples
        self.move_jumps = move_jumps # jumps that cannot capture, tuple of (x, y) tuples
        self.promotion = promotion # boolean for whether the piece can promote
        self.enpassant = enpassant # boolean for whether the piece can enpassant
        self.castle = castle # boolean for whether the piece can castle

# MOVESETS FOR STANDARD GAME PIECES
CHAR_TO_MOVESET = {
        'p': Moveset(capture_jumps = ((1, 1), (-1, 1)), move_jumps = ((0, 1), (0, 2)), promotion = True, enpassant = True),
        'z': Moveset(capture_jumps=((1, 1), (-1, 1)), move_jumps = ((0, 1)), enpassant=True, promotion = True),
        'r': Moveset(n = True, s = True, e = True, w = True),
        'n': Moveset(n = True, s = True, e = True, w = True, ne = True, se = True, sw = True, nw = True),
        'b': Moveset(ne = True, se = True, sw = True, nw = True),
        'q': Moveset(n = True, s = True, e = True, w = True, ne = True, se = True, sw = True, nw = True),
        'k': Moveset(move_jumps=((0, -1),(0, 1),(-1, -1),(-1, 0),(-1, 1),(1, -1),(1, 0),(1, 1)), castle = True)
    }

# represents the properties of a piece
class Properties:
    def __init__(self, takeable = True, landable = False, opponent_traversable = False, self_traversable = False):
        self.takeable = takeable # whether the piece can be taken
        self.landable = landable # whether the piece can be landed on
        self.opponent_traversable = opponent_traversable # whether the piece can be moved through by opponent
        self.self_traversable = self_traversable # whether the piece can be moved through by that player

class Piece:
    def __init__(self, char,  color, moveset, locations = Bitboard(0), properties = Properties()):
        self.color = color
        self.moveset = self.encode_moveset(moveset) # integer encoding of the moveset
        self.name = CHAR_TO_PIECE[char]
        self.locations = locations
        self.move_jumps = moveset.move_jumps
        self.capture_jumps = moveset.capture_jumps
        self.properties = self.encode_properties(properties)
        self.takeable = properties.takeable
        self.landable = properties.landable
        self.opponent_traverable = properties.opponent_traversable 
        self.self_traversable = properties.self_traversable

    def encode_moveset(self, moveset):
        # returns an integer encoding e of the moveset
        # e[0]: n, e[1]: s, e[2]: e, e[3]: w, e[4]: ne, e[5]: se, e[6]: sw, e[7]: nw
        # e[8]: capture_jumps (n/y), e[9]: move_jumps (n/y), e[10]: promotion, e[11]: enpassant, e[12]: castle

        e = 0
        if moveset.n:
            e |= 1
        if moveset.s:
            e |= 2
        if moveset.e:
            e |= 4
        if moveset.w:
            e |= 8
        if moveset.ne:
            e |= 16
        if moveset.se:
            e |= 32
        if moveset.sw:
            e |= 64
        if moveset.nw:
            e |= 128
        if moveset.capture_jumps:
            e |= 256
        if moveset.move_jumps:
            e |= 512
        if moveset.promotion:
            e |= 1024
        if moveset.enpassant:
            e |= 2048
        if moveset.castle:
            e |= 4096
        return e
    
    def encode_properties(self, properties):
        # returns an integer encoding of the properties
        # e[0]: takeable, e[1]: landable, e[2]: opponent_traversable, e[3]: self_traversable
        e = 0
        if properties.takeable:
            e |= 1
        if properties.landable:
            e |= 2
        if properties.opponent_traversable:
            e |= 4
        if properties.self_traversable:
            e |= 8
        return e
    
    def set_moveset(self, moveset):
        self.moveset = self.encode_moveset(moveset)
        self.move_jumps = moveset.move_jumps
        self.capture_jumps = moveset.capture_jumps
    
    def set_properties(self, properties):
        self.properties = self.encode_properties(properties)

    def __str__(self):
        return f'{self.color} {self.name}'

    def __repr__(self):
        return f'Piece(name={self.name}, color={self.color})'


