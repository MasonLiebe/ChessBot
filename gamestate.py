# This class manages the game state, and holds the bitboards representing
# all facets of the game state. It also contains methods for updating the
# game state, and for generating moves

from bitboard import Bitboard
from piece_full import *
from constants import *

class CastleRights:
    """
    Castling rights for each player
    CastleRights.0 -- kingside rights
    CastleRights.1 -- Queenside rights
    CastleRights.2 -- 1 if the player actually castled
    Where each bit in the u8 represents the castling right for the player at that index
    Ex if CastleRights.0 == 1 then the 0th player can castle kingside
    """
    def __init__(self):
        self.kingside_rights = 255
        self.queenside_rights = 255
        self.has_castled = 0

    def can_player_castle_kingside(self, playernum):
        return (self.kingside_rights >> playernum) & 1 != 0

    def can_player_castle_queenside(self, playernum):
        return (self.queenside_rights >> playernum) & 1 != 0

    def can_player_castle(self, playernum):
        return self.can_player_castle_kingside(playernum) or self.can_player_castle_queenside(playernum)

    def did_player_castle(self, playernum):
        return (self.has_castled >> playernum) & 1 != 0

    def set_player_castled(self, playernum):
        self.has_castled |= 1 << playernum

    def disable_kingside_castle(self, playernum):
        self.kingside_rights &= ~(1 << playernum)

    def disable_queenside_castle(self, playernum):
        self.queenside_rights &= ~(1 << playernum)


class GameState:
    # represents the state of the game
    # has a total of 26 piece bitboards, 
    def __init__(self, fen = STARTING_FEN, white_promotion_squares = None, black_promotion_squares = None):
        if fen == None:
            # Initialize the board position using the FEN
            self.build_from_fen(STARTING_FEN)
        else:
            self.build_from_fen(fen)
        
        # Set the promotion squares
        if white_promotion_squares is None:
            # if no promotion squares are given, set the back rank as promotion squares
            self.white_promotion_squares = Bitboard(0)
            self.white_promotion_squares.set_row_bound(0)
        else:
            self.white_promotion_squares = white_promotion_squares

        if black_promotion_squares is None:
            # if no promotion squares are given, set the back rank as promotion squares
            self.black_promotion_squares = Bitboard(0)
            self.black_promotion_squares.set_row_bound(self.rows - 2)
        else:
            self.black_promotion_squares = black_promotion_squares
    
    # GAMESTATE MANAGEMENT METHODS
    def make_move(self, move):
        pass


    # INITIALIZATION METHODS
    def build_from_fen(self, fen):
        # builds the game state from a fen string
        
        # Get FEN components:
        board_config, turn, castle_rights, enpassant_square, halfmove_clock, fullmove_number = fen.split()

        # Build the board
        # get the rows and columns
        row_strings = board_config.split('/')
        self.rows = len(row_strings)
        # compute the number of columns
        self.cols = 0
        for c in row_strings[0]:
            if c.isdigit():
                self.cols += int(c)
            else:
                self.cols += 1
        
        # validate board shape:
        if self.rows not in range(1, 17) or self.cols not in range(1, 17):
            raise ValueError('Invalid board shape: must be between 1x1 and 16x16')
        
        # check if each row has the same number of squares as the first row
        for row in row_strings:
            current_cols = 0
            for c in row:
                if c.isdigit():
                    current_cols += int(c)
                else:
                    current_cols += 1
            if current_cols != self.cols:
                raise ValueError('Invalid board shape: rows have different numbers of squares')
        
        # INITIALIZE ALL BITBOARDS FOR THE GAME STATE
        # register the boundaries of gameboard to the top right 16x16 bitboard
        # 1 means the square is out of bounds
        self.board_boundaries = Bitboard(0)
        self.board_boundaries.set_row_bound(self.rows)
        self.board_boundaries.set_col_bound(self.cols)

        # create Piece objects for each piece type and color
        # Each Piece contains the following:
        # - a character representing the piece
        # - a color
        # - a Moveset object representing the moveset of the piece
        # - a Bitboard object representing the locations of the piece
        # - a Properties object representing the properties of the piece
        self.white_new_pawn = Piece('p', 'w', CHAR_TO_MOVESET['p'], Bitboard(0))
        self.white_old_pawn = Piece('z', 'w', CHAR_TO_MOVESET['z'], Bitboard(0))
        self.white_rook = Piece('r', 'w', CHAR_TO_MOVESET['r'], Bitboard(0))
        self.white_knight = Piece('n', 'w', CHAR_TO_MOVESET['n'], Bitboard(0))
        self.white_bishop = Piece('b', 'w', CHAR_TO_MOVESET['b'], Bitboard(0))
        self.white_queen = Piece('q', 'w', CHAR_TO_MOVESET['q'], Bitboard(0))
        self.white_king = Piece('k', 'w', CHAR_TO_MOVESET['k'], Bitboard(0))
        self.black_new_pawn = Piece('p', 'b', CHAR_TO_MOVESET['p'], Bitboard(0))
        self.black_old_pawn = Piece('z', 'b', CHAR_TO_MOVESET['z'], Bitboard(0))
        self.black_rook = Piece('r', 'b', CHAR_TO_MOVESET['r'], Bitboard(0))
        self.black_knight = Piece('n', 'b', CHAR_TO_MOVESET['n'], Bitboard(0))
        self.black_bishop = Piece('b', 'b', CHAR_TO_MOVESET['b'], Bitboard(0))
        self.black_queen = Piece('q', 'b', CHAR_TO_MOVESET['q'], Bitboard(0))
        self.black_king = Piece('k', 'b', CHAR_TO_MOVESET['k'], Bitboard(0))

        # custom piece objects
        self.white_custom1 = Piece('a', 'w', Moveset(), Bitboard(0))
        self.white_custom2 = Piece('c', 'w', Moveset(), Bitboard(0))
        self.white_custom3 = Piece('d', 'w', Moveset(), Bitboard(0))
        self.white_custom4 = Piece('e', 'w', Moveset(), Bitboard(0))
        self.white_custom5 = Piece('f', 'w', Moveset(), Bitboard(0))
        self.white_custom6 = Piece('g', 'w', Moveset(), Bitboard(0))
        self.black_custom1 = Piece('a', 'b', Moveset(), Bitboard(0))
        self.black_custom2 = Piece('c', 'b', Moveset(), Bitboard(0))
        self.black_custom3 = Piece('d', 'b', Moveset(), Bitboard(0))
        self.black_custom4 = Piece('e', 'b', Moveset(), Bitboard(0))
        self.black_custom5 = Piece('f', 'b', Moveset(), Bitboard(0))
        self.black_custom6 = Piece('g', 'b', Moveset(), Bitboard(0))

        # register takeable squares for each color
        self.white_takeable = Bitboard(0) # Squares with a piece that can be taken by each color
        self.black_takeable = Bitboard(0)

        # register traversable squares for each color
        self.white_traversable = Bitboard(0) # Squares that can be moved through by white but not landed on
        self.black_traversable = Bitboard(0)

        # register empty squares
        self.occupied = Bitboard(0) # Squares with a piece on them
        self.enpassant_square = 0 # Square where an enpassant capture can be made as a 8-bit integer

        # iterate through the fen and update the required bitboards
        for y, row in enumerate(row_strings):
            x = 0
            for c in row:
                if c.isdigit():
                    x += int(c)
                else:
                    # find which piece it is
                    piece = CHAR_TO_PIECE[c.lower()]
                    color = 'white' if c.isupper() else 'black'
                    # set the corresponding piece bitboard
                    piece = getattr(self, f'{color}_{piece}')
                    piece.locations.set_coord(x, y)
                    # update the occupied bitboard
                    self.occupied.set_coord(x, y)

                    # update the takeable bitboard
                    if piece.takeable:
                        if color == 'black':
                            self.white_takeable.set_coord(x, y)
                        else:
                            self.black_takeable.set_coord(x, y)
                    
                    # update the traversable bitboard
                    if piece.self_traversable:
                        if color == 'black':
                            self.white_traversable.set_coord(x, y)
                        else:
                            self.black_traversable.set_coord(x, y)
                    x += 1
        
        # update the enpassant square
        if enpassant_square != '-':
            x, y = FILE_TO_INT[enpassant_square[0]], int(enpassant_square[1]) - 1
            self.enpassant_square = 16 * y + x
        
        # update the turn
        self.turn = turn

        # update the castle rights as an 4-bit integer C where
        # C[0]: white kingside, C[1]: white queenside, C[2]: black kingside, C[3]: black queenside
        self.castle_rights = 0
        if 'K' in castle_rights:
            self.castle_rights |= 1
        if 'Q' in castle_rights:
            self.castle_rights |= 2
        if 'k' in castle_rights:
            self.castle_rights |= 4
        if 'q' in castle_rights:
            self.castle_rights |= 8
        
        # update the halfmove clock and fullmove number
        self.halfmove_clock = int(halfmove_clock)
        self.fullmove_number = int(fullmove_number)


# Test the GameState class
if __name__ == '__main__':
    game = GameState(E4E5_FEN)
    print('Rows:', game.rows)
    print('Cols:', game.cols)

    print('Enpassant_square:', game.enpassant_square)
    print('Castle Rights (KQkq):', bin(game.castle_rights))
    print('halfmove clock:', game.halfmove_clock)
    print('fullmove Number:', game.fullmove_number)
    print('Turn:', game.turn)
    print('---------BOUNDARIES---------')
    print(game.board_boundaries)
    print('---------WHITE NEW_PAWNS---------')
    print(game.white_new_pawn.locations)
    print('---------BLACK NEW_PAWNS---------')
    print(game.black_new_pawn.locations)
    print('---------WHITE OLD_PAWNS---------')
    print(game.white_old_pawn.locations)
    print('---------BLACK OLD_PAWNS---------')
    print(game.black_old_pawn.locations)
    print('---------WHITE ROOKS---------')
    print(game.white_rook.locations)
    print('---------BLACK ROOKS---------')
    print(game.black_rook.locations)
    print('---------WHITE KNIGHTS---------')
    print(game.white_knight.locations)
    print('---------BLACK KNIGHTS---------')
    print(game.black_knight.locations)
    print('---------WHITE BISHOPS---------')
    print(game.white_bishop.locations)
    print('---------BLACK BISHOPS---------')
    print(game.black_bishop.locations)
    print('---------WHITE QUEENS---------')
    print(game.white_queen.locations)
    print('---------BLACK QUEENS---------')
    print(game.black_queen.locations)
    print('---------WHITE KINGS---------')
    print(game.white_king.locations)
    print('---------BLACK KINGS---------')
    print(game.black_king.locations)
    print('---------OCCUPIED---------')
    print(game.occupied)
    print('---------WHITE TAKEABLE---------')
    print(game.white_takeable)
    print('---------BLACK TAKEABLE---------')
    print(game.black_takeable)
    print('---------WHITE TRAVERSABLE---------')
    print(game.white_traversable)
    print('---------BLACK TRAVERSABLE---------')
    print(game.black_traversable)