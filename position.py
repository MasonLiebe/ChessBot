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
        self.bounds.set_col_bounds(self.dims.width)
        self.bounds.set_row_bounds(self.dims.height)
        self.num_players = 2

        # Set up the piece sets (these by default contain empty pieces)
        w_pieces = PieceSet(0) # player_num is 0
        b_pieces = PieceSet(1) # player_num is 1
        self.pieces = [w_pieces, b_pieces]
        self.occupied = Bitboard(0) # empty for now

        # parse the fen and construct the board state
        piece_placement, turn, castling, en_passant, half_move_clock, full_move_number = fen.split(' ')

        # add each piece to the board from the fen
        y = 7
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
            y -= 1
        
        # set occupied to be the union of all the pieceSet.occupied bitboards
        for pieceSet in self.pieces:
            self.occupied |= pieceSet.occupied

        # set the turn
        self.whos_turn = 0 if turn == 'w' else 1

        castle_rights = CastleRights()
        castle_rights.set_from_string(castling)

        ep_square = to_index(FILE_TO_INT[en_passant[0]], int(en_passant[1])) if en_passant != '-' else None

        # Compute the zobrist key
        self.zobrist_table = ZobristTable()
        zobrist_key = 0

        self.compute_zobrist()
        

        self.properties = PositionProperties(0, None, None, castle_rights, ep_square, None, None)
    
    def custom_board(self, dims: Dimensions, bounds: Bitboard, movement_patterns, pieces: list[tuple[int, int, str]] ):
        # Pieces tuples are (owner, index, piece_type)
        pass

    def register_piecetype(self, char_rep: str, mpe: MovementPatternExternal):
        pass

    def get_movement_pattern(self, piece_type: str) -> MovementPattern:
        pass

    def set_bounds(self, dims: Dimensions, bounds: Bitboard):
        self.dimensions = dims
        self.bounds - bounds
    
    def make_move(self, move: Move):
        # takes in a move object and modifies position to make the move
        pass

    def unmake_move(self):
        pass

    def to_string(self):
        pass

    def pieces_as_tuples(self):
        #
        pass

    def tiles_as_tuples(self):
        pass
    
    def get_zobrist(self):
        pass

    def compute_zobrist(self):
        # computes the zobrist key for the current position, from the position properties
        self.zobrist_key = 0
        # player to move
        self.zobrist_key ^= zob.get_to_move_zobrist(self.whos_turn)
        # castling rights
        if self.properties().castling_rights.king:
            self.zobrist_key ^= zob.get_castling_zobrist(0, True)

    def piece_at(self, index: int):
        pass

    def place_bb_at(self, index: int):
        pass

    def xy_in_bounds(self, x: int, y: int):
        pass

    def move_piece(self, from_index: int, to_index: int):
        pass

    def _remove_piece(self, index: int):
        pass

    def _add_piece(self, owner: int, index: int, piece_type: str):
        pass

    def update_occupied(self):
        pass

    def add_piece(self, owner: int, piece_type: str, index: int):
        pass

    def remove_piece(self, index: int):
        pass



# Testing for the Position class
    
p = Position()
print(p)
print('zobrist_key:', p.properties.zobrist_key)
print('Kingside_rights:', p.properties.castling_rights.kingside_rights)
print('Queenside_rights:',p.properties.castling_rights.queenside_rights)
print('ep square index:', p.properties.ep_square)
print('move_played:', p.properties.move_played)
print('promote_from:', p.properties.promote_from)
print('captured_piece:', p.properties.captured_piece)