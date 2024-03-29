# This code incorporates all aspects of the piece sets and moves, to build the entire position
# Handle zobrist keys, castling rights, en passant squares, and previous positions, and moves
from collections import defaultdict

from position_properties import PositionProperties, CastleRights
from bitboard import Bitboard, from_index, to_index, to_rank_file
from moves import *
from zobrist_table import ZobristTable
from piece import Piece
from piece_set import PieceSet
from constants import *
import copy


class Position:
    # Represents a single position in chess
    # dimesnsion: Dimensions object
    # bounds: Bitboard representing the boundaries of the board
    # num_players: number of players in the game, u8
    # whos_turn: u8 representing the current player
    # movement_rules: Hashmap<PieceType, MovementPattern>
    # pieces: array of PieceSets representing each player
    # occupied: Bitboard representing all occupied squares
    # properties: PositionProperties object

    def __init__(self, fen = STARTING_FEN):
        self.width = None
        self.height = None
        self.bounds = None # Bitboard representing the boundaries of the board
        self.num_players = None # number of players in the game, u8
        self.whos_turn = None # u8 representing the current player
        self.movement_rules = None # Hashmap<PieceType, MovementPattern>
        self.pieces = None # array of PieceSets representing each player
        self.occupied = None # Bitboard representing all occupied squares
        self.properties = None # PositionProperties object
        self.zob = None # ZobristTable object
        self.king_indices = [None, None] # indices of the kings
        self.rook_origins = None # dict of rook origins for castling rights

        self.from_fen(fen)
        self.set_rook_origins()
    
    def from_fen(self, fen: str):
        # takes in a standard game fen and sets up the position

        # set dims to 8x8 and construct the bounds
        self.width = DEFAULT_WIDTH
        self.height = DEFAULT_HEIGHT
        self.bounds = Bitboard(0)
        self.bounds.set_col_bound(self.width)
        self.bounds.set_row_bound(self.height)
        self.num_players = 2

        # Set up the piece sets (these by default contain empty pieces)
        w_pieces = PieceSet(0) # player_num is 0
        b_pieces = PieceSet(1) # player_num is 1
        self.pieces = [w_pieces, b_pieces]
        self.occupied = Bitboard(0) # empty for now

        # parse the fen and construct the board state
        piece_placement, turn, castling, en_passant, half_move_clock, full_move_number = fen.split(' ')

        # add each piece to the board from the fen
        y = 0
        for row in piece_placement.split('/'):
            x = 0
            for c in row:
                if c.isdigit():
                    x += int(c)
                else:
                    index = to_index(x, y)
                    piece = CHAR_TO_PIECE[c.lower()]
                    if piece == 'King':
                        self.king_indices[int(not c.isupper())] = index
                    is_white = c.isupper()
                    pieceSet = self.pieces[0] if is_white else self.pieces[1]
                    pieceSet.place_piece_at_index(piece, index)
                    x += 1
            y += 1
        
        # set occupied to be the union of all the pieceSet.occupied bitboards
        for pieceSet in self.pieces:
            self.occupied |= pieceSet.occupied

        # set the turn
        self.whos_turn = 0 if turn == 'w' else 1

        castle_rights = CastleRights()
        castle_rights.set_from_string(castling)

        ep_square = to_index(FILE_TO_INT[en_passant[0]], self.height - int(en_passant[1])) if en_passant != '-' else None
        
        # set the Properties object
        self.properties = PositionProperties(0, None, None, castle_rights, ep_square, None, None)

        # Compute the zobrist key
        self.zob = ZobristTable()
        self.properties.zobrist_key = self.compute_zobrist()

        # Set the movement rules
        self.movement_rules = STANDARD_PATTERNS

    def set_rook_origins(self):
        # sets the rook origins for the castling rightes
        self.rook_origins = {'0q': None, '0k': None, '1q': None, '1k': None}
        for index in range(256):
            if self.pieces[0].King.bitboard.get_index(index):
                # find most distal queenside and kingside rooks
                current_rook = False
                for rook_index in range(index - index % 16, index - index % 16 + 16):
                    if self.pieces[0].Rook.bitboard.get_index(rook_index):
                        if current_rook:
                            self.rook_origins['0k'] = rook_index
                        else:
                            current_rook = True
                            # first rook found, if just one rook king can castle both sides
                            self.rook_origins['0q'] = rook_index
                            self.rook_origins['0k'] = rook_index
            if self.pieces[1].King.bitboard.get_index(index):
                # find most distal queenside and kingside rooks
                current_rook = False
                for rook_index in range(index - index % 16, index - index % 16 + 16):
                    if self.pieces[1].Rook.bitboard.get_index(rook_index):
                        if current_rook:
                            self.rook_origins['1k'] = rook_index
                        else:
                            current_rook = True
                            # first rook found, if just one rook king can castle both sides
                            self.rook_origins['1q'] = rook_index
                            self.rook_origins['1k'] = rook_index

    
    def custom_board(self, width, height, bounds: Bitboard, movement_patterns, pieces: list[tuple[int, int, str]] ):
        # Pieces tuples are (owner, index, piece_type)
        self.width = width
        self.height = height
        self.bounds = bounds
        self.num_players = 2
        self.whos_turn = 0
        self.movement_rules = movement_patterns
        self.pieces = [PieceSet(0), PieceSet(1)]
        self.occupied = Bitboard(0)

        for owner, index, piece_type in pieces:
            self.add_piece(owner, piece_type, index)
        
        self.properties = PositionProperties(0, None, None, CastleRights(), None, None, None)
        self.compute_zobrist()

    def register_piecetype(self, char_rep: str, mpe: MovementPattern):
        self.movement_rules[CHAR_TO_PIECE[char_rep]] = mpe

    def get_movement_pattern(self, piece_type: str) -> MovementPattern:
        return self.movement_rules.get(piece_type, None)

    def set_bounds(self, width, height, bounds: Bitboard):
        self.width = width
        self.height = height
        self.bounds - bounds
    
    def make_move(self, move: Move):

        # Before properties are changed, save the old_properties
        old_props = copy.deepcopy(self.properties)

        # Grab the move properties
        from_index = move.get_from_index()
        to_index = move.get_to_index()
        move_type = move.get_move_type_int()
        moving_piece_type = move.get_moving_piece_type()

        # match the move type and move the pieces on the bitboards
        match move_type:
            case 0: # quiet move
                self.move_known_piece(from_index, to_index, moving_piece_type, self.whos_turn)
            case 1: # capture
                opponent = (self.whos_turn + 1) % self.num_players
                self.move_known_piece(from_index, to_index, moving_piece_type, self.whos_turn)
                self.remove_known_piece(to_index, move.get_target_piece_type(), opponent)
                self.properties.captured_piece = (opponent, move.get_target_piece_type())
            case 2: # queenside castle
                self.move_known_piece(from_index, to_index, moving_piece_type, self.whos_turn) # move the king to its destination square
                # move the rook to its destination square
                rook_origin_index = self.rook_origins[str(self.whos_turn) + 'q']
                self.move_known_piece(rook_origin_index, to_index + 1, "Rook", self.whos_turn) # 1 square to the right of the king
            case 3: # kingside castle
                self.move_known_piece(from_index, to_index, moving_piece_type, self.whos_turn)
                # move the rook to its destination square
                rook_origin_index = self.rook_origins[str(self.whos_turn) + 'k']
                self.move_known_piece(rook_origin_index, to_index - 1, "Rook", self.whos_turn) # 1 square to the left of the king
            case 4: # promotion
                # remove the piece
                self.remove_known_piece(from_index, moving_piece_type, self.whos_turn)
                # add the promoted_piece
                self.place_known_piece(to_index, move.get_promotion_piece_type(), self.whos_turn)
                self.properties.promote_from = moving_piece_type
            case 5: # promotion capture
                # remove the moving piece and the captured piece
                opponent = (self.whos_turn + 1) % self.num_players
                self.remove_known_piece(from_index, moving_piece_type, self.whos_turn)
                self.remove_known_piece(to_index, move.get_target_piece_type(), opponent)
                # add the promoted piece
                self.place_known_piece(to_index, move.get_promotion_piece_type(), self.whos_turn)
                self.properties.promote_from = moving_piece_type
                self.properties.captured_piece = (self.whos_turn, move.get_target_piece_type())
            case 6: # null move
                pass
        
        # update all of the properties in the self.position_properties object
        # Zobrist key is handled incrementally
        # here are the easy ones
        self.properties.move_played = move
        self.properties.prev_properties = old_props

        # handle en passant capture:
        if moving_piece_type in ("Pawn", "NPawn") and move.get_to_index() == self.properties.ep_square:
            # remove the captured pawn
            self.remove_known_piece(self.properties.ep_square - 16, "Pawn", (self.whos_turn + 1) % self.num_players)

        # handle the new pawn move
        if self.properties.ep_square is not None: # revert the en passant square zobrist signature if needed
            self.properties.zobrist_key ^= self.zob.get_ep_zobrist_file(self.properties.ep_square % 16)
        if moving_piece_type == "NPawn":
            # if the pawn moved two squares, set the en passant square
            if abs(from_index - to_index) == 32:
                self.properties.ep_square = (from_index + to_index) // 2
                self.properties.zobrist_key ^= self.zob.get_ep_zobrist_file(from_index % 16)
            else:
                self.properties.ep_square = None
            # convert the piece type to a regular Pawn
            self.remove_known_piece(to_index, moving_piece_type, self.whos_turn)
            self.place_known_piece(to_index, "Pawn", self.whos_turn)
        else:
            self.properties.ep_square = None
        
        # update castling rights if needed
        if moving_piece_type == "King":
            self.king_indices[self.whos_turn] = to_index
            self.properties.castling_rights.disable_kingside_castle(self.whos_turn)
            self.properties.castling_rights.disable_queenside_castle(self.whos_turn)
        if moving_piece_type == "Rook":
            if from_index == self.rook_origins[str(self.whos_turn) + 'q']:
                self.properties.castling_rights.disable_queenside_castle(self.whos_turn)
                self.properties.zobrist_key ^= self.zob.get_castling_zobrist(self.whos_turn, False)
            if from_index == self.rook_origins[str(self.whos_turn) + 'k']:
                self.properties.castling_rights.disable_kingside_castle(self.whos_turn)
                self.properties.zobrist_key ^= self.zob.get_castling_zobrist(self.whos_turn, True)

        # Update the turn
        player = self.whos_turn
        self.whos_turn = (self.whos_turn + 1) % self.num_players
        self.properties.zobrist_key ^= self.zob.get_to_move_zobrist(player) # inverts the to_move zobrist signature

    def unmake_move(self):
        # reverts a move based on the current position_properties and
        # reverts exactly to the state before the last move was made
        if self.properties.prev_properties is None:
            return
        
        # revert the board position
        move = self.properties.move_played
        from_index = move.get_from_index()
        to_index = move.get_to_index()
        moving_piece_type = move.get_moving_piece_type()
        opponent = self.whos_turn
        self.whos_turn = (self.whos_turn + 1) % self.num_players

        match move.get_move_type_int():
            case 0: # quiet move
                self.move_known_piece(to_index, from_index, moving_piece_type, self.whos_turn)
            case 1: # capture
                self.move_known_piece(to_index, from_index, moving_piece_type, self.whos_turn)
                self.place_known_piece(to_index, move.get_target_piece_type(), opponent)
            case 2: # queenside castle
                self.move_known_piece(to_index, from_index, moving_piece_type, self.whos_turn)
                rook_origin_index = self.rook_origins[str(self.whos_turn) + 'q']
                self.move_known_piece(to_index + 1, rook_origin_index, "Rook", self.whos_turn)
            case 3: # kingside castle
                self.move_known_piece(to_index, from_index, moving_piece_type, self.whos_turn)
                rook_origin_index = self.rook_origins[str(self.whos_turn) + 'k']
                self.move_known_piece(to_index - 1, rook_origin_index, "Rook", self.whos_turn)
            case 4: # promotion
                self.remove_known_piece(to_index, move.get_promotion_piece_type(), self.whos_turn)
                self.place_known_piece(from_index, moving_piece_type, self.whos_turn)
            case 5: # promotion capture
                self.remove_known_piece(to_index, move.get_promotion_piece_type(), self.whos_turn)
                self.place_known_piece(to_index, move.get_target_piece_type(), opponent)
                self.place_known_piece(from_index, moving_piece_type, self.whos_turn)
            case 6: # null move
                pass
        
        if moving_piece_type == "King":
            self.king_indices[self.whos_turn] = from_index
        
        if moving_piece_type == 'NPawn':
            self.remove_known_piece(from_index, "Pawn", self.whos_turn)
        
        if self.properties.ep_square is not None:
            self.properties.zobrist_key ^= self.zob.get_ep_zobrist_file(self.properties.ep_square % 16)

        # revert the properties
        self.properties = self.properties.prev_properties

        if self.properties.ep_square is not None:
            self.properties.zobrist_key ^= self.zob.get_ep_zobrist_file(self.properties.ep_square % 16)


    def to_string(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.pieces[0].occupied.get_coord(x, y):
                    print(self.pieces[0].piece_at(y * 16 + x).char_rep.upper(), end=' ')
                elif self.pieces[1].occupied.get_coord(x, y):
                    print(self.pieces[1].piece_at(y * 16 + x).char_rep, end=' ')
                else:
                    print('·', end=' ')
            print()
    
    def get_zobrist(self):
        return self.properties.zobrist_key
    
    # INTERNAL MOVEMENT METHODS THAT MAINTAIN ZOBRIST KEY
    def move_known_piece(self, from_index: int, to_index: int, piece_type: str, player_num: int):
        # moves a piece given the from and to indices and piece type/owner
        # update the piece bitboard for the piece object
        self.pieces[player_num].place_piece_at_index(piece_type, to_index)
        self.pieces[player_num].remove_known_piece_at_index(piece_type, from_index)
        self.update_occupied()

        # update the zobrist key
        self.properties.zobrist_key ^= self.zob.get_zobrist_sq_from_pt(piece_type, player_num, from_index) # inverts the zobrist signature for the piece at the from index
        self.properties.zobrist_key ^= self.zob.get_zobrist_sq_from_pt(piece_type, player_num, to_index) # reverts the zobrist signature for the piece at the to index
    
    def place_known_piece(self, index: int, piece_type: str, player_num: int):
        # places a piece at the given index
        self.pieces[player_num].place_piece_at_index(piece_type, index)
        self.update_occupied()
        self.properties.zobrist_key ^= self.zob.get_zobrist_sq_from_pt(piece_type, player_num, index)
    
    def remove_known_piece(self, index: int, piece_type: str, player_num: int):
        # removes a piece at the given index
        self.pieces[player_num].remove_known_piece_at_index(piece_type, index)
        self.update_occupied()
        self.properties.zobrist_key ^= self.zob.get_zobrist_sq_from_pt(piece_type, player_num, index)
    
    # END INTERNAL MOVEMENT METHODS
        
    def compute_zobrist(self):
        # computes the zobrist key for the current position, from the position properties
        self.properties.zobrist_key = 0
        # player to move
        self.properties.zobrist_key ^= self.zob.get_to_move_zobrist(self.whos_turn)
        # castling rights
        if self.properties.castling_rights.can_player_castle_kingside(0):
            self.properties.zobrist_key ^= self.zob.get_castling_zobrist(0, True)
        if self.properties.castling_rights.can_player_castle_queenside(0):
            self.properties.zobrist_key ^= self.zob.get_castling_zobrist(0, False)
        if self.properties.castling_rights.can_player_castle_kingside(1):
            self.properties.zobrist_key ^= self.zob.get_castling_zobrist(1, True)
        if self.properties.castling_rights.can_player_castle_queenside(1):
            self.properties.zobrist_key ^= self.zob.get_castling_zobrist(1, False)
        # en passant square
        if self.properties.ep_square is not None:
            self.properties.zobrist_key ^= self.zob.get_ep_zobrist_file(self.properties.ep_square % 16)
        # pieces
        for pieceSet in self.pieces:
            for piece in [pieceSet.King, pieceSet.Queen, pieceSet.Bishop, pieceSet.Knight, pieceSet.Rook, pieceSet.Pawn, pieceSet.Custom1, pieceSet.Custom2, pieceSet.Custom3, pieceSet.Custom4, pieceSet.Custom5, pieceSet.Custom6, pieceSet.NPawn]:
                self.properties.zobrist_key ^= self.zob.get_zobrist_piece(piece, pieceSet.player_num)

        return self.properties.zobrist_key

    def piece_at(self, index: int):
        # returns tuple (player_num, piece_type)
        for pieceSet in self.pieces:
            if pieceSet.occupied.get_coord(from_index(index)):
                return (pieceSet.player_num, pieceSet.piece_at(index))
        return None

    def piece_bb_at(self, index: int):
        # returns bitboard of piece at index
        for pieceSet in self.pieces:
            if pieceSet.occupied.get_coord(from_index(index)):
                for piece in [pieceSet.King, pieceSet.Queen, pieceSet.Bishop, pieceSet.Knight, pieceSet.Rook, pieceSet.Pawn, pieceSet.Custom1, pieceSet.Custom2, pieceSet.Custom3, pieceSet.Custom4, pieceSet.Custom5, pieceSet.Custom6, pieceSet.NPawn]:
                    if piece.occupied.get_coord(from_index(index)):
                        return piece.occupied
        # There's no piece at this index, return none
        return None

    def xy_in_bounds(self, x: int, y: int):
        return not (x < 0 or x >= self.width or y < 0 or y >= self.height)

    def move_piece(self, from_index: int, to_index: int):
        # ONLY MOVES THIS PIECE, DOESN'T CAPTURE THE OTHER PIECE OR SET THE ZOBRIST KEY
        source_bitboard = self.piece_bb_at(from_index)
        if source_bitboard is None:
            return
        source_bitboard.clear_coord(from_index)
        source_bitboard.set_coord(to_index)
        self.update_occupied()

    def update_occupied(self):
        self.occupied.zero()
        self.occupied = self.pieces[0].occupied | self.pieces[1].occupied

    def add_piece(self, owner: int, piece_type: str, index: int):
        # adds a piece to the board
        pieceSet = self.pieces[owner]
        pieceSet.place_piece_at_index(piece_type, index)
        self.update_occupied()

    def remove_piece(self, index: int):
        # removes a piece from the board
        for pieceSet in self.pieces:
            pieceSet.remove_piece_at_index(index)
        self.update_occupied()

'''
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

# Testing for the Position class
import random
random.seed(6)
p = Position(E4E5_FEN)
print(p)
print('whos_turn:', p.whos_turn)
print('zobrist_key:', p.properties.zobrist_key)
print('Kingside_rights:', p.properties.castling_rights.kingside_rights)
print('Queenside_rights:',p.properties.castling_rights.queenside_rights)
print('ep square index:', p.properties.ep_square)
print('move_played:', p.properties.move_played)
print('promote_from:', p.properties.promote_from)
print('captured_piece:', p.properties.captured_piece)
print('rook_origins:', p.rook_origins)
print('castle_rights', p.properties.castling_rights)
print('king_indices:', p.king_indices)
p.to_string()

move1 = Move(115, 55, "Queen", move_type = "Quiet")
move2 = Move(99, 67, "NPawn", move_type = "Quiet") # Pawn Move
move3 = Move(116, 100, "King", move_type = "Quiet") # King move
move4 = Move(52, 67, "Pawn",target_piece_type="Pawn",  move_type="Capture") # Pawn Capture - AFTER MOVE 2



p.make_move(move2)
print('whos_turn:', p.whos_turn)
print('zobrist_key:', p.properties.zobrist_key)
print('Kingside_rights:', p.properties.castling_rights.kingside_rights)
print('Queenside_rights:',p.properties.castling_rights.queenside_rights)
print('ep square index:', p.properties.ep_square)
print('move_played:', p.properties.move_played)
print('promote_from:', p.properties.promote_from)
print('captured_piece:', p.properties.captured_piece)
print('rook_origins:', p.rook_origins)
print('castle_rights', p.properties.castling_rights)
print('king_indices:', p.king_indices)

p.compute_zobrist()
print("computed zobrist key:", p.properties.zobrist_key)
p.to_string()



p.make_move(move4)
print('whos_turn:', p.whos_turn)
print('zobrist_key:', p.properties.zobrist_key)
print('Kingside_rights:', p.properties.castling_rights.kingside_rights)
print('Queenside_rights:',p.properties.castling_rights.queenside_rights)
print('ep square index:', p.properties.ep_square)
print('move_played:', p.properties.move_played)
print('promote_from:', p.properties.promote_from)
print('captured_piece:', p.properties.captured_piece)
print('rook_origins:', p.rook_origins)
print('castle_rights', p.properties.castling_rights)
print('king_indices:', p.king_indices)


p.compute_zobrist()
print("computed zobrist key:", p.properties.zobrist_key)

p.to_string()

p.unmake_move()

print('whos_turn:', p.whos_turn)
print('zobrist_key:', p.properties.zobrist_key)
print('Kingside_rights:', p.properties.castling_rights.kingside_rights)
print('Queenside_rights:',p.properties.castling_rights.queenside_rights)
print('ep square index:', p.properties.ep_square)
print('move_played:', p.properties.move_played)
print('promote_from:', p.properties.promote_from)
print('captured_piece:', p.properties.captured_piece)
print('rook_origins:', p.rook_origins)
print('castle_rights', p.properties.castling_rights)
print('king_indices:', p.king_indices)

# Test if zobrist hash computed is the same:
p.compute_zobrist()
print("computed zobrist key:", p.properties.zobrist_key)


p.to_string()

# Here are all of the bitboards for the pieces

print('-----------------WHITE PIECES-----------------')

print('KING:\n',p.pieces[0].King.bitboard)
print('PAWN:\n',p.pieces[0].Pawn.bitboard)
print('NPawn:\n',p.pieces[0].NPawn.bitboard)

print('-----------------Black PIECES-----------------')

print('KING:\n',p.pieces[1].King.bitboard)
print('PAWN:\n',p.pieces[1].Pawn.bitboard)
print('NPawn:\n',p.pieces[1].NPawn.bitboard)






