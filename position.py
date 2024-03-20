from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from bitboard import *
from piece_set import PieceSet
from position_properties import PositionProperties
from movement_pattern import MovementPattern, MovementPatternExternal, external_mp_to_internal, internal_mp_to_external
from piece import Piece
from move import PieceType, Dimensions, Move, MoveType
from zobrist_table import ZobristTable
from constants import *



@dataclass
class Position:
    dimensions: Dimensions
    bounds: Bitboard
    num_players: int
    whos_turn: int
    movement_rules: Dict[PieceType, MovementPattern]
    pieces: List[PieceSet]
    occupied: Bitboard
    properties: PositionProperties
    ZOBRIST_TABLE: ZobristTable

    @classmethod
    def default(cls) -> 'Position':
        return cls.from_fen(STARTING_FEN)

    def register_piecetype(self, char_rep: str, mpe: MovementPatternExternal):
        mp = external_mp_to_internal(mpe)

        for i, p in enumerate(self.pieces):
            match len(p.custom):
                case 0:
                    p.custom.append(Piece.blank_custom1(i))
                    self.movement_rules[PieceType.Custom1] = mp
                case 1:
                    p.custom.append(Piece.blank_custom2(i))
                    self.movement_rules[PieceType.Custom2] = mp
                case 2:
                    p.custom.append(Piece.blank_custom3(i))
                    self.movement_rules[PieceType.Custom3] = mp
                case 3:
                    p.custom.append(Piece.blank_custom4(i))
                    self.movement_rules[PieceType.Custom4] = mp
                case 4:
                    p.custom.append(Piece.blank_custom5(i))
                    self.movement_rules[PieceType.Custom5] = mp
                case 5:
                    p.custom.append(Piece.blank_custom6(i))
                    self.movement_rules[PieceType.Custom6] = mp
                case _:
                    raise ValueError("Too many custom pieces")

    def get_char_movementpattern_map(self) -> Dict[str, MovementPatternExternal]:
        return_map = {}
        for piece_type, movement_pattern in self.movement_rules.items():
            if isinstance(piece_type, PieceType.Custom):
                return_map[piece_type.value] = internal_mp_to_external(movement_pattern)
        return return_map

    def get_movement_pattern(self, piece_type: PieceType) -> Optional[MovementPattern]:
        return self.movement_rules.get(piece_type)

    def set_bounds(self, dims: Dimensions, bounds: Bitboard):
        self.dimensions = dims
        self.bounds = bounds

    def make_move(self, move_: Move):
        zobrist_table = self.ZOBRIST_TABLE
        my_player_num = self.whos_turn
        self.whos_turn = (self.whos_turn + 1) % self.num_players

        new_props = self.properties.copy()
        new_props.zobrist_key ^= zobrist_table.get_to_move_zobrist(self.whos_turn)

        move_type = move_.get_move_type()

        if move_type == 'Null':
            new_props.ep_square = None
            new_props.move_played = move_
            new_props.prev_properties = self.properties
            self.properties = new_props
            return

        if move_type in ['Capture', 'PromotionCapture']:
            capt_index = move_.get_target()
            owner, captd = self.piece_at(capt_index)
            captd_piece_type = captd.piece_type
            captd_owner = captd.player_num
            new_props.zobrist_key ^= zobrist_table.get_zobrist_sq_from_pt(captd_piece_type, captd_owner, capt_index)
            new_props.captured_piece = (owner, captd_piece_type)
            self._remove_piece(capt_index)

        elif move_type == 'KingsideCastle':
            rook_from = move_.get_target()
            x, y = from_index(move_.get_to())
            rook_to = to_index(x - 1, y)
            new_props.zobrist_key ^= zobrist_table.get_zobrist_sq_from_pt(PieceType.Rook, my_player_num, rook_from)
            new_props.zobrist_key ^= zobrist_table.get_zobrist_sq_from_pt(PieceType.Rook, my_player_num, rook_to)
            self.move_piece(rook_from, rook_to)
            new_props.castling_rights.set_player_castled(my_player_num)

        elif move_type == 'QueensideCastle':
            rook_from = move_.get_target()
            x, y = from_index(move_.get_to())
            rook_to = to_index(x + 1, y)
            new_props.zobrist_key ^= zobrist_table.get_zobrist_sq_from_pt(PieceType.Rook, my_player_num, rook_from)
            new_props.zobrist_key ^= zobrist_table.get_zobrist_sq_from_pt(PieceType.Rook, my_player_num, rook_to)
            self.move_piece(rook_from, rook_to)
            new_props.castling_rights.set_player_castled(my_player_num)

        from_ = move_.get_from()
        to = move_.get_to()
        from_piece = self.piece_at(from_)[1]
        from_piece_type = from_piece.piece_type
        new_props.zobrist_key ^= zobrist_table.get_zobrist_sq_from_pt(from_piece_type, my_player_num, from_)
        new_props.zobrist_key ^= zobrist_table.get_zobrist_sq_from_pt(from_piece_type, my_player_num, to)

        self.move_piece(from_, to)

        if move_type in ['PromotionCapture', 'Promotion']:
            new_props.promote_from = from_piece_type
            new_props.zobrist_key ^= zobrist_table.get_zobrist_sq_from_pt(from_piece_type, my_player_num, to)
            self._remove_piece(to)
            promote_to_pt = PieceType.from_char(move_.get_promotion_char())
            new_props.zobrist_key ^= zobrist_table.get_zobrist_sq_from_pt(promote_to_pt, my_player_num, to)
            self._add_piece(my_player_num, promote_to_pt, to)

        x1, y1 = from_index(from_)
        x2, y2 = from_index(to)

        if self.properties.ep_square is not None:
            epx, _ = from_index(self.properties.ep_square)
            new_props.zobrist_key ^= zobrist_table.get_ep_zobrist_file(epx)

        if from_piece_type == PieceType.Pawn and abs(y2 - y1) == 2 and x1 == x2:
            if y2 > y1:
                new_props.ep_square = to_index(x1, y2 - 1)
            else:
                new_props.ep_square = to_index(x1, y2 + 1)
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
                if x1 >= self.dimensions.width // 2:
                    new_props.castling_rights.disable_kingside_castle(my_player_num)
                    new_props.zobrist_key ^= zobrist_table.get_castling_zobrist(my_player_num, True)
                else:
                    new_props.castling_rights.disable_queenside_castle(my_player_num)
                    new_props.zobrist_key ^= zobrist_table.get_castling_zobrist(my_player_num, False)

        new_props.prev_properties = self.properties
        new_props.move_played = move_
        self.properties = new_props
        self.update_occupied()

    def unmake_move(self):
        if self.whos_turn == 0:
            self.whos_turn = self.num_players - 1
        else:
            self.whos_turn = (self.whos_turn - 1) % self.num_players

        my_player_num = self.whos_turn
        move_ = self.properties.move_played
        move_type = move_.get_move_type()

        if move_type == 'Null':
            self.properties = self.properties.get_prev()
            return

        from_ = move_.get_from()
        to = move_.get_to()

        self.move_piece(to, from_)

        if move_type in ['PromotionCapture', 'Promotion']:
            self._remove_piece(from_)
            self._add_piece(my_player_num, self.properties.promote_from, from_)

        if move_type in ['Capture', 'PromotionCapture']:
            capt = move_.get_target()
            owner, pt = self.properties.captured_piece
            self._add_piece(owner, pt, capt)

        elif move_type == 'KingsideCastle':
            rook_from = move_.get_target()
            x, y = from_index(move_.get_to())
            rook_to = to_index(x - 1, y)
            self.move_piece(rook_to, rook_from)

        elif move_type == 'QueensideCastle':
            rook_from = move_.get_target()
            x, y = from_index(move_.get_to())
            rook_to = to_index(x + 1, y)
            self.move_piece(rook_to, rook_from)

        self.properties = self.properties.get_prev()
        self.update_occupied()

    def to_string(self) -> str:
        return_str = ""
        for y in range(self.dimensions.height - 1, -1, -1):
            return_str = f"{return_str} {y} "
            for x in range(self.dimensions.width):
                piece_info = self.piece_at(to_index(x, y))
                if piece_info:
                    player_num, piece = piece_info
                    if player_num == 0:
                        return_str += piece.char_rep.upper()
                    else:
                        return_str += piece.char_rep.lower()
                else:
                    return_str += "."
                return_str += " "
            return_str += "\n"
        return_str += " "
        for x in range(self.dimensions.width):
            return_str = f"{return_str} {x}"
        return f"{return_str} \nZobrist Key: {self.properties.zobrist_key}"

    def pieces_as_tuples(self) -> List[Tuple[int, int, int, str]]:
        tuples = []
        for i, ps in enumerate(self.pieces):
            for piece in ps.get_piece_refs():
                bb_copy = piece.bitboard.copy()
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
    
    @classmethod
    def custom(cls, dims: Dimensions, bounds: Bitboard, movement_patterns: Dict[str, MovementPatternExternal], pieces: List[Tuple[int, int, PieceType]]):
        pos = Position.from_fen(EMPTY_FEN)
        pos.dimensions = dims
        pos.bounds = bounds
        
        for chr, mpe in movement_patterns.items():
            pos.register_piecetype(chr, mpe)
        
        for owner, index, piece_type in pieces:
            pos.add_piece(owner, piece_type, index)
        
        return pos  
    
    @classmethod
    def from_fen(cls, fen: str) -> 'Position':
        dims = Dimensions(width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT)

        wb_pieces = []
        w_pieces = PieceSet.new(0)
        b_pieces = PieceSet.new(1)

        x = 0
        y = 7
        field = 0

        whos_turn = 0
        can_w_castle_k = False
        can_b_castle_k = False
        can_w_castle_q = False
        can_b_castle_q = False

        for c in fen:
            if c == ' ':
                field += 1
            elif field == 0:  # position
                if c == '/':
                    x = 0
                    y -= 1
                    continue
                elif c.isdigit():
                    x += int(c)
                    continue

                index = to_index(x, y)
                piece_map = {
                    'k': (w_pieces.king.bitboard, b_pieces.king.bitboard),
                    'q': (w_pieces.queen.bitboard, b_pieces.queen.bitboard),
                    'r': (w_pieces.rook.bitboard, b_pieces.rook.bitboard),
                    'b': (w_pieces.bishop.bitboard, b_pieces.bishop.bitboard),
                    'n': (w_pieces.knight.bitboard, b_pieces.knight.bitboard),
                    'p': (w_pieces.pawn.bitboard, b_pieces.pawn.bitboard)
                }
                if c.lower() in piece_map:
                    bitboard = piece_map[c.lower()][0] if c.isupper() else piece_map[c.lower()][1]
                    bitboard.set_bit(index, True)
                    if c.isupper():
                        w_pieces.occupied.set_bit(index, True)
                    else:
                        b_pieces.occupied.set_bit(index, True)
                    x += 1

            elif field == 1:  # next to move
                if c == 'w':
                    whos_turn = 0
                else:
                    whos_turn = 1
            elif field == 2:  # Castling rights
                if c == 'K':
                    can_w_castle_k = True
                elif c == 'Q':
                    can_w_castle_q = True
                elif c == 'k':
                    can_b_castle_k = True
                elif c == 'q':
                    can_b_castle_q = True
            elif field == 3:  # EP square
                # TODO: Implement EP square
                continue


        occupied = Bitboard.zero()
        occupied |= w_pieces.occupied
        occupied |= b_pieces.occupied
        zobrist_table = ZobristTable()
        zobrist_key = 0

        properties = PositionProperties.default()
        zobrist_key ^= zobrist_table.get_castling_zobrist(0, True)
        zobrist_key ^= zobrist_table.get_castling_zobrist(0, False)
        zobrist_key ^= zobrist_table.get_castling_zobrist(1, True)
        zobrist_key ^= zobrist_table.get_castling_zobrist(1, False)

        if not can_w_castle_k:
            properties.castling_rights.disable_kingside_castle(0)
            zobrist_key ^= zobrist_table.get_castling_zobrist(0, True)
        if not can_b_castle_k:
            properties.castling_rights.disable_kingside_castle(1)
            zobrist_key ^= zobrist_table.get_castling_zobrist(1, True)
        if not can_w_castle_q:
            properties.castling_rights.disable_queenside_castle(0)
            zobrist_key ^= zobrist_table.get_castling_zobrist(0, False)
        if not can_b_castle_q:
            properties.castling_rights.disable_queenside_castle(1)
            zobrist_key ^= zobrist_table.get_castling_zobrist(1, False)

        for piece in w_pieces.get_piece_refs() + b_pieces.get_piece_refs():
            bb_copy = piece.bitboard.copy()
            while not bb_copy.is_zero():
                indx = bb_copy.lowest_one()
                zobrist_key ^= zobrist_table.get_zobrist_sq(piece, indx)
                bb_copy.set_bit(indx, False)

        properties.zobrist_key = zobrist_key

        wb_pieces.append(w_pieces)
        wb_pieces.append(b_pieces)

        bounds = Bitboard.zero()
        for x in range(8):
            for y in range(8):
                bounds.set_bit(to_index(x, y), True)

        pos = cls(
            whos_turn=whos_turn,
            num_players=2,
            dimensions=dims,
            pieces=wb_pieces,
            occupied=occupied,
            bounds=bounds,
            properties=properties,
            movement_rules={},
            ZOBRIST_TABLE=zobrist_table
        )

        return pos

    def get_zobrist(self) -> int:
        return self.properties.zobrist_key

    def piece_at(self, index: int) -> Optional[Tuple[int, Piece]]:
        for i, ps in enumerate(self.pieces):
            piece = ps.piece_at(index)
            if piece:
                return (i, piece)
        return None

    def piece_bb_at(self, index: int) -> Optional[Bitboard]:
        piece_info = self.piece_at(index)
        if piece_info:
            _, piece = piece_info
            return piece.bitboard
        return None

    def xy_in_bounds(self, x: int, y: int) -> bool:
        if x < self.dimensions.width and y < self.dimensions.height:
            return self.bounds.bit(to_index(x, y))
        return False

    def move_piece(self, from_: int, to: int):
        source_bb = self.piece_bb_at(from_)
        if source_bb:
            source_bb.set_bit(from_, False)
            source_bb.set_bit(to, True)
        else:
            print("nothing to move??")
            print(f"from {from_index(from_)[0]} {from_index(from_)[1]}")
            print(f"to {from_index(to)[0]} {from_index(to)[1]}")
            print("==")

    def _remove_piece(self, index: int):
        capd_bb = self.piece_bb_at(index)
        if capd_bb:
            capd_bb.set_bit(index, False)

    def _add_piece(self, owner: int, pt: PieceType, index: int):
        piece_map = {
            PieceType.King: self.pieces[owner].king.bitboard,
            PieceType.Queen: self.pieces[owner].queen.bitboard,
            PieceType.Rook: self.pieces[owner].rook.bitboard,
            PieceType.Bishop: self.pieces[owner].bishop.bitboard,
            PieceType.Knight: self.pieces[owner].knight.bitboard,
            PieceType.Pawn: self.pieces[owner].pawn.bitboard,
        }
        if pt in piece_map:
            piece_map[pt].set_bit(index, True)
            return

        try:
            match pt:
                case PieceType.Custom1:
                    self.pieces[owner].custom[0].bitboard.set_bit(index, True)
                case PieceType.Custom2:
                    self.pieces[owner].custom[1].bitboard.set_bit(index, True)
                case PieceType.Custom3:
                    self.pieces[owner].custom[2].bitboard.set_bit(index, True)
                case PieceType.Custom4:
                    self.pieces[owner].custom[3].bitboard.set_bit(index, True)
                case PieceType.Custom5:
                    self.pieces[owner].custom[4].bitboard.set_bit(index, True)
                case PieceType.Custom6:
                    self.pieces[owner].custom[5].bitboard.set_bit(index, True)
                case _:
                    raise ValueError("Invalid PieceType")
        except IndexError as e:
            print("Unregistered Custom PieceType")
            

    def update_occupied(self):
        self.occupied = Bitboard.zero()
        for ps in self.pieces:
            ps.update_occupied()
            self.occupied |= ps.occupied

    def add_piece(self, owner: int, pt: PieceType, index: int):
        new_props = self.properties.copy()
        zobrist_table = self.ZOBRIST_TABLE
        new_props.zobrist_key ^= zobrist_table.get_zobrist_sq_from_pt(pt, owner, index)
        self._add_piece(owner, pt, index)
        self.update_occupied()
        new_props.prev_properties = self.properties
        self.properties = new_props

    def remove_piece(self, index: int):
        self._remove_piece(index)
        self.update_occupied()



## Testing
        
pos = Position.default()
print(pos.to_string())

test_moves = {
    1: Move.new(to_index(4, 1), to_index(4,3),move_type='Quiet'), # e4
    2: Move.new(to_index(4, 6), to_index(4,4),move_type='Quiet'), # e5
}

for i in range(1, 3):
    pos.make_move(test_moves[i])
    print(pos.to_string())

for i in range(1, 3):
    pos.unmake_move()
    print(pos.to_string())

# dims = Dimensions(width=10, height=10)
# pos = Position.custom(dims, Bitboard.zero(), {}, [(0, to_index(5, 0), PieceType.King), (1, to_index(5, 9), PieceType.King)])

# print(pos.to_string())

# # create a custom piece
# pos.register_piecetype('a', MovementPatternExternal())

# print("LOOK HERE")
# print(str(pos.movement_rules[PieceType.Custom1]))

# pos.add_piece(1,PieceType.Rook,  to_index(5, 5))
# pos.add_piece(0,PieceType.Custom1, to_index(5, 7))

# print(pos.to_string())

# print(pos.pieces[0].custom[0].bitboard)
# print(pos.pieces[0].custom[0].char_rep)
