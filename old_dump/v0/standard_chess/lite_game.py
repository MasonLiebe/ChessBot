# this class implements a lighter implementation of the game
import re
import chess

class LiteGame:
    # much lighter implementation of the game to improve efficiency and performance
    # this class will be used for the game engine and the AI
    # self.board is a list of 8 strings, each string representing a rank on the board
    # self.turn is a string representing the current turn, either 'w' or 'b'
    # self.castling is a string representing the castling rights of the game
    # self.en_passant is a string representing the en passant square
    # self.halfmove is a string representing the halfmove clock
    # self.fullmove is a string representing the fullmove number
    # self.fens is a list of FENs representing the game state at each move

    # UNICODE_PIECE_SYMBOLS is a dictionary that maps the FEN piece symbols to their unicode representation
    UNICODE_PIECE_SYMBOLS = {
        "R": "♖", "r": "♜",
        "N": "♘", "n": "♞",
        "B": "♗", "b": "♝",
        "Q": "♕", "q": "♛",
        "K": "♔", "k": "♚",
        "P": "♙", "p": "♟",
        "-": "·"
    }

    def __init__(self, fen = None, pgn = None):
        # if neither fen nor pgn is provided, start a new game
        self.fens = []
        if not fen and not pgn:
            self.set_board_with_fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
        elif fen:
            self.set_board_with_fen(fen)
        elif pgn:
            self.set_board_with_pgn(pgn)

    def set_board_with_fen(self, fen):
        split_fen = fen.split()
        self.fens = [fen]
        self.board = self.fen_to_board(fen)
        self.turn = split_fen[1]
        self.castling = split_fen[2]
        self.en_passant = split_fen[3]
        self.halfmove = split_fen[4]
        self.fullmove = split_fen[5]
    
    def generate_fen(self):
        # generates an FEN from the current board
        # replace dots in board with numbers
        new_board = self.board.copy()
        for i in range(1, 9):
            for rank in new_board:
                rank = rank.replace('.' * i, str(i))

        return '/'.join(new_board) + ' ' + self.turn + ' ' + self.castling + ' ' + self.en_passant + ' ' + self.halfmove + ' ' + self.fullmove

    def 

    def perform_move(self, origin, destination, promotion = None):
        # performs a move given the origin and destination squares
            
    
    def set_board_with_pgn(self, pgn):
        # set's the board given a pgn
        # TODO: implement this after board is implemented
        pass
    
    def parse_pgn(self, pgn):
        # returns a list of FENs from the PGN
        # TODO: implement this after board is implemented
        pass

    def fen_to_board(self, fen):
        board = []
        for row in fen.split('/'):
            brow = ''
            for c in row:
                if c == ' ':
                    break
                elif c in '12345678':
                    brow += ('-' * int(c))
                else:
                    brow += c
            board.append( brow )
        return board

    def print_board(self):
        for rank in (self.board):
            for char in rank:
                if char.isdigit():
                    print('· ' * int(char), end='')
                else:
                    print(self.UNICODE_PIECE_SYMBOLS[char], end=' ')
            print()

new_game = LiteGame(fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
new_game.print_board()

new_game = LiteGame(fen = '8/BP6/2K5/5P2/8/8/3k4/8 w - - 0 1')
new_game.print_board()
