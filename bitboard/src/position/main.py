from position_properties import PositionProperties
from types.chess_move import MoveType, Move
from position.movement_pattern import MovementPattern, MovementPatternExternal,external_mp_to_internal, internal_mp_to_external
from types.bitboard import Bitboard, from_index, to_index
from types.mod import PieceType
from position.piece import Piece
from position.zobrist_table import ZobristTable
from constants import fen
from typing import List, Tuple

DEFAULT_WIDTH = 8
DEFAULT_HEIGHT = 8
ZOBRIST_TABLE = ZobristTable()
for c in "acdefghijlmostuvwxyz":
    ZOBRIST_TABLE.register_piecetype(0, PieceType.Custom(c))
    ZOBRIST_TABLE.register_piecetype(1, PieceType.Custom(c))

class Dimensions:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

class Position:
    def __init__(self):
        self.dimensions = Dimensions(0, 0)
        self.bounds = Bitboard()
        self.num_players = 0
        self.whos_turn = 0
        self.movement_rules = {}
        self.pieces = []
        self.occupied = Bitboard()
        self.properties = PositionProperties()

    @staticmethod
    def default() -> 'Position':
        return Position.from_fen(fen.STARTING_POS)

    @staticmethod
    def from_fen(fen: str) -> 'Position':
        dimensions = Dimensions(DEFAULT_WIDTH, DEFAULT_HEIGHT)
        bounds = Bitboard()
        num_players = 2
        whos_turn = 0
        movement_rules = {}
        pieces = set()
        occupied = Bitboard()
        properties = PositionProperties()

        position = Position()
        position.dimensions = dimensions
        position.bounds = bounds
        position.num_players = num_players
        position.whos_turn = whos_turn
        position.movement_rules = movement_rules
        position.pieces = pieces
        position.occupied = occupied
        position.properties = properties

        return position

    def register_piecetype(self, char_rep: str, mpe: MovementPatternExternal):
        movement_pattern = external_mp_to_internal(mpe)
        self.movement_rules[PieceType.Custom(char_rep)] = movement_pattern

        for i, p in enumerate(self.pieces):
            p.custom.append(Piece.blank_custom(i, char_rep))

    def get_char_movementpattern_map(self) -> dict:
        return_map = {}
        for pieceType, movement_pattern in self.movement_rules.items():
            if isinstance(pieceType, PieceType.Custom):
                return_map[pieceType.value] = internal_mp_to_external(movement_pattern)

        return return_map

    def get_movement_pattern(self, piece_type: PieceType) -> MovementPattern:
        return self.movement_rules.get(piece_type)

    def set_bounds(self, dims: Dimensions, bounds: Bitboard):
        self.dimensions = dims
        self.bounds = bounds

    def make_move(self, move_: Move):
        zobrist_table = ZOBRIST_TABLE
        my_player_num = self.whos_turn
        self.whos_turn = (self.whos_turn + 1) % self.num_players
        new_props = self.properties.clone()
        new_props.zobrist_key ^= zobrist_table.get_to_move_zobrist(self.whos_turn)

        if move_.get_move_type() == MoveType.Null:
            new_props.ep_square = None
            new_props.move_played = move_
            new_props.prev_properties = self.properties
            self.properties = new_props
            return

        if move_.get_move_type() in [MoveType.Capture, MoveType.PromotionCapture]:
            capt_index = move_.get_target()
            owner, captd = self.piece_at(capt_index)
            captd_piece_type = captd.piece_type
            captd_owner = captd.player_num
            new_props.zobrist_key ^= zobrist_table.get_zobrist_sq_from_pt(captd_piece_type, captd_owner, capt_index)
            new_props.captured_piece = (owner, captd_piece_type)
            self._remove_piece(capt_index)

        if move_.get_move_type() == MoveType.KingsideCastle:
            rook_from = move_.get_target()
            x, y = from_index(move_.get_to())
            rook_to = to_index(x - 1, y)
            new_props.zobrist_key ^= zobrist_table.get_zobrist_sq_from_pt(PieceType.Rook, my_player_num, rook_from)
            new_props.zobrist_key ^= zobrist_table.get_zobrist_sq_from_pt(PieceType.Rook, my_player_num, rook_to)
            self.move_piece(rook_from, rook_to)
            new_props.castling_rights.set_player_castled(my_player_num)

        if move_.get_move_type() == MoveType.QueensideCastle:
            rook_from = move_.get_target()
            x, y = from_index(move_.get_to())
            rook_to = to_index(x + 1, y)
            new_props.zobrist_key ^= zobrist_table.get_zobrist_sq_from_pt(PieceType.Rook, my_player_num, rook_from)
            new_props.zobrist_key ^= zobrist_table.get_zobrist_sq_from_pt(PieceType.Rook, my_player_num, rook_to)
            self.move_piece(rook_from, rook_to)
            new_props.castling_rights.set_player_castled(my_player_num)

        from_ = move_.get_from()
        to = move_.get_to()
        from_piece = self.piece_at(from_).piece
        from_piece_type = from_piece.piece_type
        new_props.zobrist_key ^= zobrist_table.get_zobrist_sq_from_pt(from_piece_type, my_player_num, from_)
        new_props.zobrist_key ^= zobrist_table.get_zobrist_sq_from_pt(from_piece_type, my_player_num, to)
        self.move_piece(from_, to)

        if move_.get_move_type() in [MoveType.PromotionCapture, MoveType.Promotion]:
            new_props.promote_from = from_piece_type
            new_props.zobrist_key ^= zobrist_table.get_zobrist_sq_from_pt(from_piece_type, my_player_num, to)
            self._remove_piece(to)
            promote_to_pt = PieceType.from_char(move_.get_promotion_char())
            new_props.zobrist_key ^= zobrist_table.get_zobrist_sq_from_pt(promote_to_pt, my_player_num, to)
            self._add_piece(my_player_num, promote_to_pt, to)

        (x1, y1) = from_index(from_)
        (x2, y2) = from_index(to)
        if self.properties.ep_square is not None:
            (epx, _) = from_index(self.properties.ep_square)
            new_props.zobrist_key ^= zobrist_table.get_ep_zobrist_file(epx)

        if from_piece_type == PieceType.Pawn and abs(y2 - y1) == 2 and x1 == x2:
            new_props.ep_square = (
                to_index(x1, y2 - 1)
                if y2 > y1
                else to_index(x1, y2 + 1)
            )
            new_props.zobrist_key ^= zobrist_table.get_ep_zobrist_file(x1)
        else:
            new_props.ep_square = None

        if new_props.castling_rights.can_player_castle(my_player_num):
            if from_piece_type == PieceType.King:
                new_props.zobrist_key ^= zobrist_table.get_castling_zobrist(my_player_num, True)
                new_props.zobrist_key ^= zobrist_table.get_castling_zobrist(my_player_num, False)
                new_props.castling_rights.disable_kingside_castle(my_player_num)
                new_props.castling_rights.disable_queenside_castle(my_player_num)
            elif from_piece_type == PieceType.Rook:
                if x1 >= self.dimensions.width / 2:
                    new_props.castling_rights.disable_kingside_castle(my_player_num)
                    new_props.zobrist_key ^= zobrist_table.get_castling_zobrist(my_player_num, True)
                else:
                    new_props.castling_rights.disable_queenside_castle(my_player_num)
                    new_props.zobrist_key ^= zobrist_table.get_castling_zobrist(my_player_num, False)

        new_props.move_played = move_
        new_props.prev_properties = self.properties
        self.properties = new_props
        self.update_occupied()

    def unmake_move(self):
        if self.whos_turn == 0:
            self.whos_turn = self.num_players - 1
        else:
            self.whos_turn = (self.whos_turn - 1) % self.num_players
        move_ = self.properties.move_played

        if move_.get_move_type() == MoveType.Null:
            self.properties = self.properties.prev_properties
            return

        from_ = move_.get_from()
        to = move_.get_to()

        self.move_piece(to, from_)

        if move_.get_move_type() in [MoveType.PromotionCapture, MoveType.Promotion]:
            self._remove_piece(from_)
            self._add_piece(
                self.whos_turn,
                self.properties.promote_from,
                from_
            )

        if move_.get_move_type() in [MoveType.Capture, MoveType.PromotionCapture]:
            capt = move_.get_target()
            owner, pt = self.properties.captured_piece
            self._add_piece(owner, pt, capt)

        if move_.get_move_type() == MoveType.KingsideCastle:
            rook_from = move_.get_target()
            x, y = from_index(move_.get_to())
            rook_to = to_index(x - 1, y)
            self.move_piece(rook_to, rook_from)

        if move_.get_move_type() == MoveType.QueensideCastle:
            rook_from = move_.get_target()
            x, y = from_index(move_.get_to())
            rook_to = to_index(x + 1, y)
            self.move_piece(rook_to, rook_from)

        self.properties = self.properties.prev_properties
        self.update_occupied()

    def to_string(self) -> str:
        return_str = ""
        for y in range(self.dimensions.height - 1, -1, -1):
            return_str += f" {y} "
            for x in range(self.dimensions.width):
                piece = self.piece_at(to_index(x, y))
                if piece is not None:
                    if piece.player_num == 0:
                        return_str += piece.char_rep.upper()
                    else:
                        return_str += piece.char_rep.lower()
                else:
                    return_str += "."
                return_str += " "
            return_str += "\n"
        return_str += "   "
        for x in range(self.dimensions.width):
            return_str += f"{x} "
        return f"{return_str}\nZobrist Key: {self.properties.zobrist_key}"

    def pieces_as_tuples(self) -> List[Tuple[int, int, int, str]]:
        tuples = []
        for i, ps in enumerate(self.pieces):
            for piece in ps.get_piece_refs():
                bb_copy = piece.bitboard
                while not bb_copy.is_zero():
                    indx = bb_copy.lowest_one()
                    x, y = from_index(indx)
                    tuples.append((i, x, y, piece.char_rep))
                    bb_copy.set_bit(indx, False)
        return tuples

    def tiles_as_tuples(self) -> List[Tuple[int, int, str]]:
        squares = []
        for x in range(self.dimensions.width):
            for y in range(self.dimensions.height):
                if self.xy_in_bounds(x, y):
                    char_rep = "b" if (x + y) % 2 == 0 else "w"
                    squares.append((x, y, char_rep))
                else:
                    squares.append((x, y, "x"))
        return squares

    @staticmethod
    def custom(dims: Dimensions, bounds: Bitboard,
               movement_patterns: dict, pieces: List[Tuple[int, int, PieceType]]) -> 'Position':
        pos = Position()
        pos.dimensions = dims
        pos.bounds = bounds

        for char_rep, mpe in movement_patterns.items():
            pos.register_piecetype(char_rep, mpe)

        for owner, index, piece_type in pieces:
            pos.add_piece(owner, piece_type, index)

        return pos
    
    def from_fen(fen):
        dims = {'width': 8, 'height': 8}
        wb_pieces = []
        w_pieces = {'king': {'bitboard': 0}, 'queen': {'bitboard': 0}, 'rook': {'bitboard': 0}, 'bishop': {'bitboard': 0}, 'knight': {'bitboard': 0}, 'pawn': {'bitboard': 0}}
        b_pieces = {'king': {'bitboard': 0}, 'queen': {'bitboard': 0}, 'rook': {'bitboard': 0}, 'bishop': {'bitboard': 0}, 'knight': {'bitboard': 0}, 'pawn': {'bitboard': 0}}
        x = 0
        y = 7
        field = 0
        whos_turn = 0
        _ep_sq = 0
        can_w_castle_k = False
        can_b_castle_k = False
        can_w_castle_q = False
        can_b_castle_q = False
        for c in fen:
            if c == ' ':
                field += 1
            if field == 0:
                if c == '/':
                    x = 0
                    y -= 1
                    continue
                elif c.isnumeric():
                    x += int(c)
                    continue
                index = x + y * dims['width']
                bitboard = None
                if c.lower() == 'k':
                    if c.isupper():
                        bitboard = w_pieces['king']['bitboard']
                    else:
                        bitboard = b_pieces['king']['bitboard']
                elif c.lower() == 'q':
                    if c.isupper():
                        bitboard = w_pieces['queen']['bitboard']
                    else:
                        bitboard = b_pieces['queen']['bitboard']
                elif c.lower() == 'r':
                    if c.isupper():
                        bitboard = w_pieces['rook']['bitboard']
                    else:
                        bitboard = b_pieces['rook']['bitboard']
                elif c.lower() == 'b':
                    if c.isupper():
                        bitboard = w_pieces['bishop']['bitboard']
                    else:
                        bitboard = b_pieces['bishop']['bitboard']
                elif c.lower() == 'n':
                    if c.isupper():
                        bitboard = w_pieces['knight']['bitboard']
                    else:
                        bitboard = b_pieces['knight']['bitboard']
                elif c.lower() == 'p':
                    if c.isupper():
                        bitboard = w_pieces['pawn']['bitboard']
                    else:
                        bitboard = b_pieces['pawn']['bitboard']
                if bitboard is not None:
                    bitboard |= 1 << index
                    if c.isupper():
                        w_pieces['occupied'] |= 1 << index
                    else:
                        b_pieces['occupied'] |= 1 << index
                    x += 1
            elif field == 1:
                if c == 'w':
                    whos_turn = 0
                else:
                    whos_turn = 1
            elif field == 2:
                if c == 'K':
                    can_w_castle_k = True
                elif c == 'Q':
                    can_w_castle_q = True
                elif c == 'k':
                    can_b_castle_k = True
                elif c == 'q':
                    can_b_castle_q = True
            elif field == 3:
                pass
        occupied = w_pieces['occupied'] | b_pieces['occupied']
        zobrist_key = 0
        if not can_w_castle_k:
            zobrist_key ^= ZOBRIST_TABLE.get_castling_zobrist(0, True)
        if not can_b_castle_k:
            zobrist_key ^= ZOBRIST_TABLE.get_castling_zobrist(1, True)
        if not can_w_castle_q:
            zobrist_key ^= ZOBRIST_TABLE.get_castling_zobrist(0, False)
        if not can_b_castle_q:
            zobrist_key ^= ZOBRIST_TABLE.get_castling_zobrist(1, False)
        for piece in [w_pieces['king'], w_pieces['queen'], w_pieces['rook'], w_pieces['bishop'], w_pieces['knight'], w_pieces['pawn'], b_pieces['king'], b_pieces['queen'], b_pieces['rook'], b_pieces['bishop'], b_pieces['knight'], b_pieces['pawn']]:
            bb_copy = piece['bitboard']
            while bb_copy != 0:
                indx = bb_copy & -bb_copy
                zobrist_key ^= ZOBRIST_TABLE.get_zobrist_sq(piece, indx)
                bb_copy &= bb_copy - 1
        properties = {'zobrist_key': zobrist_key}
        wb_pieces.append(w_pieces)
        wb_pieces.append(b_pieces)
        bounds = 0
        for x in range(8):
            for y in range(8):
                bounds |= 1 << (x + y * dims['width'])
        pos = {'whos_turn': whos_turn, 'num_players': 2, 'dimensions': dims, 'pieces': wb_pieces, 'occupied': occupied, 'bounds': bounds, 'properties': properties, 'movement_rules': {}}
        return pos

    def get_zobrist(self):
        return self['properties']['zobrist_key']

    def piece_at(self, index):
        for i, ps in enumerate(self['pieces']):
            if index in ps:
                return (i, ps[index])
        return None

    def piece_bb_at(self, index):
        piece = self.piece_at(index)
        if piece is not None:
            return piece[1]['bitboard']
        return None

    def xy_in_bounds(self, x, y):
        if x < self['dimensions']['width'] and y < self['dimensions']['height']:
            return bool(self['bounds'] & (1 << (x + y * self['dimensions']['width'])))
        return False

    def move_piece(self, from_, to):
        source_bb = self.piece_bb_at(from_)
        if source_bb is not None:
            source_bb &= ~(1 << from_)
            source_bb |= 1 << to
        else:
            print("nothing to move??")
            print("from {} {}".format(from_index(from_), from_index(from_)))
            print("to {} {}".format(from_index(to), from_index(to)))
            print("==")

    def _remove_piece(self, index):
        capd_bb = self.piece_bb_at(index)
        if capd_bb is not None:
            capd_bb &= ~(1 << index)

    def _add_piece(self, owner, pt, index):
        if pt == 'King':
            self['pieces'][owner]['king']['bitboard'] |= 1 << index
        elif pt == 'Queen':
            self['pieces'][owner]['queen']['bitboard'] |= 1 << index
        elif pt == 'Rook':
            self['pieces'][owner]['rook']['bitboard'] |= 1 << index
        elif pt == 'Bishop':
            self['pieces'][owner]['bishop']['bitboard'] |= 1 << index
        elif pt == 'Knight':
            self['pieces'][owner]['knight']['bitboard'] |= 1 << index
        elif pt == 'Pawn':
            self['pieces'][owner]['pawn']['bitboard'] |= 1 << index
        elif pt.startswith('Custom'):
            for c in self['pieces'][owner]['custom']:
                if pt == c['char_rep']:
                    c['bitboard'] |= 1 << index
                    break

    def update_occupied(self):
        self['occupied'] = self['pieces'][0]['occupied'] | self['pieces'][1]['occupied']

    def add_piece(self, owner, pt, index):
        new_props = self['properties'].copy()
        zobrist_table = ZOBRIST_TABLE
        new_props['zobrist_key'] ^= ZOBRIST_TABLE.get_zobrist_sq_from_pt(pt, owner, index)
        self._add_piece(owner, pt, index)
        self.update_occupied()
        new_props['prev_properties'] = self['properties'].copy()
        self['properties'] = new_props

    def remove_piece(self, index):
        self._remove_piece(index)
        self.update_occupied()


