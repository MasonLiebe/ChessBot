
from board import Board

class Piece:
    # takes in a color, row, column, and type and creates an instance of the required piece
    def __init__(self, row, col, color):
        self.color = color
        self.row = row
        self.col = col
    
    def get_color(self):
        return self.color
    
    def get_row(self):
        return self.row
    
    def get_col(self):
        return self.col
    
    def is_capturable(self, piece, selfCapture = False):
        # @param piece: the piece that is attempting to capture this piece
        # @param selfCapture: a boolean representing whether selfCapture is enabled
        # @return: a boolean representing whether the piece can be captured

        if self.color == piece.get_color() and not selfCapture:
            return False
        return True

    def execute_move(self, row, col):
        # @param row: the row the piece will move to
        # @param col: the column the piece will move to
        # @return: None
        
        self.row = row
        self.col = col
        return

# Individual Piece Classes Below
class Pawn(Piece):
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.Type = "Pawn"

    def get_valid_moves(self, board, enPassant = None, overwrite = False, selfCapture = False, castlingState = (True, True, True, True)):
        # @param board: the board object representing the current board state
        # @param enPassant: the current enPassant state as a tuple (row, col)
        # @param overwrite: a boolean representing whether the move is an overwrite
        # @param selfCapture: a boolean representing whether the move is a selfCapture
        # @param castlingState: a tuple representing the castling state of the board
        # @return: a list of tuples representing the valid moves for the piece

        possibleMoves = []
        # check if pawn has moved based on rank based on color
        if self.color == "white":
            if self.row == board.get_rows() - 2:
                if board.get_board()[self.row - 1][self.col] == 0 and board.get_board()[self.row - 2][self.col] == 0:
                    possibleMoves.append((self.row - 2, self.col))
        else:
            if self.row == 1:
                if board[self.row + 1][self.col] == 0 and board[self.row + 2][self.col] == 0:
                    possibleMoves.append((self.row + 2, self.col))
        
        # check if pawn can move forward one square
        if self.color == "white":
            if board[self.row - 1][self.col] == 0:
                possibleMoves.append((self.row - 1, self.col))
        else:
            if board[self.row + 1][self.col] == 0:
                possibleMoves.append((self.row + 1, self.col))
        
        # check if pawn can capture
        if self.color == "white":
            if self.col > 0 and board[self.row - 1][self.col - 1] != 0:
                possibleMoves.append((self.row - 1, self.col - 1))
            if self.col < board.get_columns() - 1 and board[self.row - 1][self.col + 1] != 0:
                possibleMoves.append((self.row - 1, self.col + 1))
        else:
            if self.col > 0 and board[self.row + 1][self.col - 1] != 0:
                possibleMoves.append((self.row + 1, self.col - 1))
            if self.col < board.get_columns() - 1 and board[self.row + 1][self.col + 1] != 0:
                possibleMoves.append((self.row + 1, self.col + 1))
        
        # check if pawn can capture enPassant
        if enPassant != None:
            if self.color == "white":
                if self.col > 0 and enPassant[0] == self.row - 1 and enPassant[1] == self.col - 1:
                    possibleMoves.append((self.row - 1, self.col - 1))
                if self.col < board.get_columns() - 1 and enPassant[0] == self.row - 1 and enPassant[1] == self.col + 1:
                    possibleMoves.append((self.row - 1, self.col + 1))
            else:
                if self.col > 0 and enPassant[0] == self.row + 1 and enPassant[1] == self.col - 1:
                    possibleMoves.append((self.row + 1, self.col - 1))
                if self.col < board.get_columns() - 1 and enPassant[0] == self.row + 1 and enPassant[1] == self.col + 1:
                    possibleMoves.append((self.row + 1, self.col + 1))
        
        # return the list of possible moves
        return possibleMoves


class Knight(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.Type = "Knight"
    
    def get_valid_moves(self, board, enPassant, overwrite, selfCapture, castlingState):
        # @param board: the current board state as integer array
        # @param enPassant: the current enPassant state as a tuple (row, col)
        # @param overwrite: a boolean representing whether the move is an overwrite
        # @param selfCapture: a boolean representing whether the move is a selfCapture
        # @param castlingState: a tuple representing the castling state of the board
        # @return: a list of tuples representing the valid moves for the piece

        possibleMoves = []
        # check if knight can move to each of the 8 possible squares
        if self.row - 2 >= 0 and self.col - 1 >= 0 and (board[self.row - 2][self.col - 1] == 0 or board[self.row - 2][self.col - 1] * board[self.row][self.col] < 0):
            possibleMoves.append((self.row - 2, self.col - 1))
        if self.row - 2 >= 0 and self.col + 1 < board.get_columns() and (board[self.row - 2][self.col + 1] == 0 or board[self.row - 2][self.col + 1] * board[self.row][self.col] < 0):
            possibleMoves.append((self.row - 2, self.col + 1))
        if self.row + 2 < board.get_rows() and self.col - 1 >= 0 and (board[self.row + 2][self.col - 1] == 0 or board[self.row + 2][self.col - 1] * board[self.row][self.col] < 0):
            possibleMoves.append((self.row + 2, self.col - 1))
        if self.row + 2 < board.get_rows() and self.col + 1 < board.get_columns() and (board[self.row + 2][self.col + 1] == 0 or board[self.row + 2][self.col + 1] * board[self.row][self.col] < 0):
            possibleMoves.append((self.row + 2, self.col + 1))
        if self.row - 1 >= 0 and self.col - 2 >= 0 and (board[self.row - 1][self.col - 2] == 0 or board[self.row - 1][self.col - 2] * board[self.row][self.col] < 0):
            possibleMoves.append((self.row - 1, self.col - 2))
        if self.row - 1 >= 0 and self.col + 2 < board.get_columns() and (board[self.row - 1][self.col + 2] == 0 or board[self.row - 1][self.col + 2] * board[self.row][self.col] < 0):
            possibleMoves.append((self.row - 1, self.col + 2))
        if self.row + 1 < board.get_rows() and self.col - 2 >= 0 and (board[self.row + 1][self.col - 2] == 0 or board[self.row + 1][self.col - 2] * board[self.row][self.col] < 0):



    def capture(self):
        pass


class Bishop(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.Type = "Bishop"

    def move(self):
        pass

    def get_valid_moves(self, board, enPassant):
        pass

    def capture(self):
        pass


class Rook(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.Type = "Rook"

    def move(self):
        pass

    def get_valid_moves(self, board, enPassant):
        pass

    def capture(self):
        pass


class Queen(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.Type = "Queen"

    def move(self):
        pass

    def get_valid_moves(self, board, enPassant):
        pass

    def capture(self):
        pass


class King(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.Type = "King"

    def move(self):
        pass

    def get_valid_moves(self, board, enPassant):
        pass

    def capture(self):
        pass


class Duck(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.Type = "Duck"

    def move(self):
        pass

    def get_valid_moves(self, board, enPassant):
        pass

    def capture(self):
        pass

class CustomPiece1(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.Type = "CustomPiece1"

    def move(self):
        pass

    def get_valid_moves(self, board, enPassant):
        pass

    def capture(self):
        pass

class CustomPiece2(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.Type = "CustomPiece2"

    def move(self):
        pass

    def get_valid_moves(self, board, enPassant):
        pass

    def capture(self):
        pass

class CustomPiece3(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.Type = "CustomPiece3"

    def move(self):
        pass

    def get_valid_moves(self, board, enPassant):
        pass

    def capture(self):
        pass