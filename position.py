# This code incorporates all aspects of the piece sets and moves, to build the entire position
# Handle zobrist keys, castling rights, en passant squares, and previous positions, and moves
from collections import defaultdict

from position_properties import PositionProperties, CastleRights
from bitboard import Bitboard, from_index, to_index, to_rank_file
from moves import *
from zobrist_table import ZobristTable
from piece import Piece, PieceType
from piece_set import PieceSet
from constants import *


# create the zobrist table that will be used the entirety of the game
zob = ZobristTable() # ONLY CREATES AND CONTAINS ZOBRIST KEYS

class Dimensions():
    # Represents the dimensions of the board
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

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
        self.from_fen(fen)
    
    def from_fen(self, fen: str):
        # takes in a standard game fen and sets up the position

        # set dims to 8x8 and construct the bounds
        self.dims = Dimensions(DEFAULT_WIDTH, DEFAULT_HEIGHT)
        self.bounds = Bitboard(0)
        self.bounds.set_col_bound(self.dims.width)
        self.bounds.set_row_bound(self.dims.height)
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

        ep_square = to_index(FILE_TO_INT[en_passant[0]], self.dims.height - int(en_passant[1])) if en_passant != '-' else None
        
        # set the Properties object
        self.properties = PositionProperties(0, None, None, castle_rights, ep_square, None, None)

        # Compute the zobrist key
        self.zobrist_table = ZobristTable()
        self.properties.zobrist_key = self.compute_zobrist()

        # Set the movement rules
        self.movement_rules = STANDARD_PATTERNS

    
    def custom_board(self, dims: Dimensions, bounds: Bitboard, movement_patterns, pieces: list[tuple[int, int, str]] ):
        # Pieces tuples are (owner, index, piece_type)
        self.dims = dims
        self.bounds = bounds
        self.num_players = 2
        self.whos_turn = 0
        self.movement_rules = movement_patterns
        self.pieces = [PieceSet(0), PieceSet(1)]
        self.occupied = Bitboard(0)

        for owner, index, piece_type in pieces:
            self.add_piece(owner, piece_type, index)
        
        self.properties = PositionProperties(0, None, None, CastleRights(), None, None, None)
        self.properties.zobrist_key = self.compute_zobrist()

    def register_piecetype(self, char_rep: str, mpe: MovementPatternExternal):
        self.movement_rules[CHAR_TO_PIECE[char_rep]] = mpe

    def get_movement_pattern(self, piece_type: str) -> MovementPattern:
        return self.movement_rules.get(piece_type, None)

    def set_bounds(self, dims: Dimensions, bounds: Bitboard):
        self.dimensions = dims
        self.bounds - bounds
    
    def make_move(self, move: Move):
        # takes in a move object and modifies position to make the move
        # move is a Move object, info can be retrieved with these methods::
        # move.get_from() - index
        # move.get_to() - index
        # move.get_is_capture() - bool
        # move.get_move_type() - MoveType
        # move.get_target - index
        # get_promotion_char
        # 0: "Quiet",
        # 1: "Capture",
        # 2: "QueensideCastle",
        # 3: "KingsideCastle",
        # 4: "Promotion",
        # 5: "PromotionCapture",
        # 6: "Null"

        # Update the turn
        player = self.whos_turn
        self.whos_turn = (self.whos_turn + 1) % self.num_players

        # Before properties are changed, save the old_properties
        new_props = self.properties.copy()

        # match the move type and update the position properties
        match move.get_move_type():
            case 0: # quiet move
                self.move_piece(move.get_from(), move.get_to())
                pass
            case 1: # capture
                pass
            case 2: # queenside castle
                pass
            case 3: # kingside castle
                pass
            case 4: # promotion
                pass
            case 5: # promotion capture
                pass
            case 6: # null move
                pass

    def unmake_move(self):
        pass

    def to_string(self):
        for y in range(self.dims.height):
            for x in range(self.dims.width):
                if self.pieces[0].occupied.get_coord(x, y):
                    print(self.pieces[0].piece_at(y * 16 + x).char_rep.upper(), end=' ')
                elif self.pieces[1].occupied.get_coord(x, y):
                    print(self.pieces[1].piece_at(y * 16 + x).char_rep, end=' ')
                else:
                    print('·', end=' ')
            print()
    
    def get_zobrist(self):
        return self.properties.zobrist_key

    def compute_zobrist(self):
        # computes the zobrist key for the current position, from the position properties
        self.zobrist_key = 0
        # player to move
        self.zobrist_key ^= zob.get_to_move_zobrist(self.whos_turn)
        # castling rights
        if self.properties.castling_rights.can_player_castle_kingside(0):
            self.zobrist_key ^= zob.get_castling_zobrist(0, True)
        if self.properties.castling_rights.can_player_castle_queenside(0):
            self.zobrist_key ^= zob.get_castling_zobrist(0, False)
        if self.properties.castling_rights.can_player_castle_kingside(1):
            self.zobrist_key ^= zob.get_castling_zobrist(1, True)
        if self.properties.castling_rights.can_player_castle_queenside(1):
            self.zobrist_key ^= zob.get_castling_zobrist(1, False)
        # en passant square
        if self.properties.ep_square is not None:
            self.zobrist_key ^= zob.get_ep_zobrist_file(self.properties.ep_square % 16)
        else:
            self.zobrist_key ^= zob.get_ep_zobrist_file(16)
        # pieces
        for pieceSet in self.pieces:
            for piece in [pieceSet.King, pieceSet.Queen, pieceSet.Bishop, pieceSet.Knight, pieceSet.Rook, pieceSet.Pawn, pieceSet.Custom1, pieceSet.Custom2, pieceSet.Custom3, pieceSet.Custom4, pieceSet.Custom5, pieceSet.Custom6, pieceSet.NPawn]:
                self.zobrist_key ^= zob.get_zobrist_piece(piece, pieceSet.player_num)

        return self.zobrist_key

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
        return None

    def xy_in_bounds(self, x: int, y: int):
        return not (x < 0 or x >= self.dims.width or y < 0 or y >= self.dims.height)

    def move_piece(self, from_index: int, to_index: int):
        # ONLY MOVES THIS PIECE, DOESN'T CAPTURE THE OTHER PIECE
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



# Testing for the Position class
    
p = Position(E4E5_FEN)
print(p)
print('zobrist_key:', p.properties.zobrist_key)
print('Kingside_rights:', p.properties.castling_rights.kingside_rights)
print('Queenside_rights:',p.properties.castling_rights.queenside_rights)
print('ep square index:', p.properties.ep_square)
print('move_played:', p.properties.move_played)
print('promote_from:', p.properties.promote_from)
print('captured_piece:', p.properties.captured_piece)

p.to_string()