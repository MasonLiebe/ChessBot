
class Piece:
    def __init__(self, row, col, color, board):
        self.color = color
        self.row = row
        self.col = col
        self.Type = None
    
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

        if (self.color == piece.get_color() and not selfCapture) or self.get_color() == "yellow":
            return False
        return True

    def is_empty(self):
        return self.Type == "Empty"

    def execute_move(self, row, col):
        # @param row: the row the piece will move to
        # @param col: the column the piece will move to
        # @return: None
        
        self.row = row
        self.col = col
        return

class Empty(Piece):
    def __init__(self, row, col, color, board):
        super().__init__(row, col, color, board)
        self.Type = "Empty"
    
    def spaces_attacking(self, board):
        return []
    
    def valid_moves(self, board):
        return []

# Individual Piece Classes Below
class Pawn(Piece):
    def __init__(self, row, col, color, board):
        super().__init__(row, col, color, board)
        self.Type = "Pawn"
        self.attacking = self.squares_attacking(board)

    def squares_attacking(self, board):
        # @return: a list of tuples representing the spaces the piece is attacking
        if self.color == "white":
            return [(self.row - 1, self.col - 1), (self.row - 1, self.col + 1)]
        else:
            return [(self.row + 1, self.col - 1), (self.row + 1, self.col + 1)]
        
    def get_valid_moves(self, board, enPassant = None, overwrite = False, selfCapture = False, castlingState = (True, True, True, True)):
        # @param board: the board object representing the current board state
        # @param enPassant: the current enPassant state as a tuple (row, col)
        # @param overwrite: a boolean representing whether the move is an overwrite
        # @param selfCapture: a boolean representing whether the move is a selfCapture
        # @param castlingState: a tuple representing the castling state of the board
        # @return: a list of tuples representing the valid moves for the piece

        validMoves = []
        # check if pawn has moved based on rank based on color for 2-square jump
        if self.color == "white":
            if self.row == board.get_rows() - 2:
                if board.get_board()[self.row - 1][self.col] == 0 and board.get_board()[self.row - 2][self.col] == 0:
                    validMoves.append((self.row - 2, self.col))
        else:
            if self.row == 1:
                if board.get_board()[self.row + 1][self.col] == 0 and board.get_board()[self.row + 2][self.col] == 0:
                    validMoves.append((self.row + 2, self.col))
        
        # check if pawn can move forward one square
        if self.color == "white":
            if self.row > 0 and board.get_board()[self.row - 1][self.col] == 0:
                validMoves.append((self.row - 1, self.col))
        else:
            if self.row < board.get_rows() - 1 and board.get_board()[self.row + 1][self.col] == 0:
                validMoves.append((self.row + 1, self.col))
        
        # check if pawn can capture
        for move in self.attacking:
            if move[0] >= 0 and move[0] < board.get_rows() and move[1] >= 0 and move[1] < board.get_columns():
                if board.get_pieces()[move[0]][move[1]].is_capturable(self, selfCapture):
                    validMoves.append(move)
        return validMoves


class Knight(Piece):
    def __init__(self, color, row, col, board):
        super().__init__(color, row, col, board)
        self.Type = "Knight"
        self.attacking = self.squares_attacking(board)

    def squares_attacking(self, board):
        # @return: a list of tuples representing the spaces the piece is attacking
        validMoves = []
        # check if knight can move to each of the 8 possible squares
        for i in range(-2, 3):
            for j in range(-2, 3):
                if abs(i) + abs(j) == 3 and self.row + i >= 0 and self.row + i < board.get_rows() and self.col + j >= 0 and self.col + j < board.get_columns():
                    validMoves.append((self.row + i, self.col + j))
        return validMoves

    def get_valid_moves(self, board, enPassant = None, overwrite = False, selfCapture = False, castlingState = (True, True, True, True)):
        # @param board: the current board state as integer array
        # @param enPassant: the current enPassant state as a tuple (row, col)
        # @param overwrite: a boolean representing whether the move is an overwrite
        # @param selfCapture: a boolean representing whether the move is a selfCapture
        # @param castlingState: a tuple representing the castling state of the board
        # @return: a list of tuples representing the valid moves for the piece
        
        validMoves = []
        for move in self.attacking:
            if board.get_pieces()[move[0]][move[1]].Type == "Empty" or board.get_pieces()[move[0]][move[1]].is_capturable(self, selfCapture):
                validMoves.append(move)
        return validMoves


class Bishop(Piece):
    def __init__(self, color, row, col, board):
        super().__init__(color, row, col, board)
        self.Type = "Bishop"
        self.attacking = self.squares_attacking(board)
    
    def squares_attacking(self, board):
        # @return: a list of tuples representing the spaces the piece is attacking
        validMoves = []
        # find moves going up to the right
        for i in range(1, min(self.row, board.get_columns() - self.col)):
            if board.get_pieces()[self.row - i][self.col + i].Type != "Empty":
                validMoves.append((self.row - i, self.col + i))
                print(self.row - i, self.col + i)
                break
            else:
                # no piece encountered, add move
                print('no piece found', self.row - i, self.col + i)
                validMoves.append((self.row - i, self.col + i))

        # find moves going up to the left
        for i in range(1, min(self.row, self.col) + 1):
            if board.get_pieces()[self.row - i][self.col - i].Type != "Empty":
                validMoves.append((self.row - i, self.col - i))
                break
            else:
                # no piece encountered, add move
                validMoves.append((self.row - i, self.col - i))
        
        # find moves going down to the right
        if self.row < board.get_rows() - 1 and self.col < board.get_columns() - 1:
            for i in range(1, min(board.get_rows() - self.row, board.get_columns() - self.col)):
                if board.get_pieces()[self.row + i][self.col + i].Type != "Empty":
                    validMoves.append((self.row + i, self.col + i))
                    break
                else:
                    # no piece encountered, add move
                    validMoves.append((self.row + i, self.col + i))
        
        # find moves going down to the left
        if self.row < board.get_rows() - 1 and self.col > 0:
            for i in range(1, min(board.get_rows() - self.row, self.col) + 1):
                if board.get_pieces()[self.row + i][self.col - i].Type != "Empty":
                    validMoves.append((self.row + i, self.col - i))
                    break
                else:
                    # no piece encountered, add move
                    validMoves.append((self.row + i, self.col - i))
            
        return validMoves

    def get_valid_moves(self, board, enPassant = None, overwrite = False, selfCapture = False, castlingState = (True, True, True, True)):
        # @param board: the current board state as integer array
        # @param enPassant: the current enPassant state as a tuple (row, col)
        # @param overwrite: a boolean representing whether the move is an overwrite
        # @param selfCapture: a boolean representing whether the move is a selfCapture
        # @param castlingState: a tuple representing the castling state of the board
        # @return: a list of tuples representing the valid moves for the piece

        validMoves = []
        for move in self.attacking:
            if board.get_pieces()[move[0]][move[1]].Type == "Empty" or board.get_pieces()[move[0]][move[1]].is_capturable(self, selfCapture):
                validMoves.append(move)
        
        return validMoves
            

class Rook(Piece):
    def __init__(self, color, row, col, board):
        super().__init__(color, row, col, board)
        self.Type = "Rook"
        self.attacking = self.squares_attacking(board)
    
    def squares_attacking(self, board):
        # @return: a list of tuples representing the spaces the piece is attacking
        validMoves = []
        # find moves going up
        for i in range(1, self.row + 1):
            if board.get_pieces()[self.row - i][self.col].Type != "Empty":
                validMoves.append((self.row - i, self.col))
                break
            else:
                # no piece encountered, add move
                validMoves.append((self.row - i, self.col))
        
        # find moves going down
        for i in range(1, board.get_rows() - self.row):
            if board.get_pieces()[self.row + i][self.col].Type != "Empty":
                validMoves.append((self.row + i, self.col))
                break
            else:
                # no piece encountered, add move
                validMoves.append((self.row + i, self.col))
        
        # find moves going right
        for i in range(1, board.get_columns() - self.col):
            if board.get_pieces()[self.row][self.col + i].Type != "Empty":
                validMoves.append((self.row, self.col + i))
                break
            else:
                # no piece encountered, add move
                validMoves.append((self.row, self.col + i))
        
        # find moves going left
        for i in range(1, self.col + 1):
            if board.get_pieces()[self.row][self.col - i].Type != "Empty":
                validMoves.append((self.row, self.col - i))
                break
            else:
                # no piece encountered, add move
                validMoves.append((self.row, self.col - i))
        
        return validMoves

    def get_valid_moves(self, board, enPassant = None, overwrite = False, selfCapture = False, castlingState = (True, True, True, True)):
        # @param board: the current board state as integer array
        # @param enPassant: the current enPassant state as a tuple (row, col)
        # @param overwrite: a boolean representing whether the move is an overwrite
        # @param selfCapture: a boolean representing whether the move is a selfCapture
        # @param castlingState: a tuple representing the castling state of the board
        # @return: a list of tuples representing the valid moves for the piece

        validMoves = []
        for move in self.attacking:
            if board.get_pieces()[move[0]][move[1]].Type == "Empty" or board.get_pieces()[move[0]][move[1]].is_capturable(self, selfCapture):
                validMoves.append(move)
        
        return validMoves


class Queen(Piece):
    def __init__(self, color, row, col, board):
        super().__init__(color, row, col, board)
        self.Type = "Queen"
        self.attacking = self.squares_attacking(board)
    
    def squares_attacking(self, board):
        # @return: a list of tuples representing the spaces the piece is attacking
        validMoves = []
        # find moves going up to the right
        for i in range(1, min(self.row, board.get_columns() - self.col)):
            if board.get_pieces()[self.row - i][self.col + i].Type != "Empty":
                validMoves.append((self.row - i, self.col + i))
                break
            else:
                # no piece encountered, add move
                validMoves.append((self.row - i, self.col + i))

        # find moves going up to the left
        for i in range(1, min(self.row, self.col) + 1):
            if board.get_pieces()[self.row - i][self.col - i].Type != "Empty":
                validMoves.append((self.row - i, self.col - i))
                break
            else:
                # no piece encountered, add move
                validMoves.append((self.row - i, self.col - i))
        
        # find moves going down to the right
        if self.row < board.get_rows() - 1 and self.col < board.get_columns() - 1:
            for i in range(1, min(board.get_rows() - self.row, board.get_columns() - self.col)):
                if board.get_pieces()[self.row + i][self.col + i].Type != "Empty":
                    validMoves.append((self.row + i, self.col + i))
                    break
                else:
                    # no piece encountered, add move
                    validMoves.append((self.row + i, self.col + i))
        
        # find moves going down to the left
        if self.row < board.get_rows() - 1 and self.col > 0:
            for i in range(1, min(board.get_rows() - self.row, self.col) + 1):
                if board.get_pieces()[self.row + i][self.col - i].Type != "Empty":
                    validMoves.append((self.row + i, self.col - i))
                    break
                else:
                    # no piece encountered, add move
                    validMoves.append((self.row + i, self.col - i))
        
        # find moves going up
        for i in range(1, self.row + 1):
            if board.get_pieces()[self.row - i][self.col].Type != "Empty":
                validMoves.append((self.row - i, self.col))
                break
            else:
                # no piece encountered, add move
                validMoves.append((self.row - i, self.col))

        # find moves going down
        for i in range(1, board.get_rows() - self.row):
            if board.get_pieces()[self.row + i][self.col].Type != "Empty":
                validMoves.append((self.row + i, self.col))
                break
            else:
                # no piece encountered, add move
                validMoves.append((self.row + i, self.col))
        
        # find moves going right
        for i in range(1, board.get_columns() - self.col):
            if board.get_pieces()[self.row][self.col + i].Type != "Empty":
                validMoves.append((self.row, self.col + i))
                break
            else:
                # no piece encountered, add move
                validMoves.append((self.row, self.col + i))

        # find moves going left
        for i in range(1, self.col + 1):
            if board.get_pieces()[self.row][self.col - i].Type != "Empty":
                print("piece encountered at", self.row, self.col - i)
                validMoves.append((self.row, self.col - i))
                break
            else:
                # no piece encountered, add move
                validMoves.append((self.row, self.col - i))
        
        return validMoves

    def get_valid_moves(self, board, enPassant = None, overwrite = False, selfCapture = False, castlingState = (True, True, True, True)):
        # @param board: the current board state as integer array
        # @param enPassant: the current enPassant state as a tuple (row, col)
        # @param overwrite: a boolean representing whether the move is an overwrite
        # @param selfCapture: a boolean representing whether the move is a selfCapture
        # @param castlingState: a tuple representing the castling state of the board
        # @return: a list of tuples representing the valid moves for the piece

        validMoves = []
        for move in self.attacking:
            if board.get_pieces()[move[0]][move[1]].Type == "Empty" or board.get_pieces()[move[0]][move[1]].is_capturable(self, selfCapture):
                validMoves.append(move)

        return validMoves


class King(Piece):
    def __init__(self, color, row, col, board):
        super().__init__(color, row, col, board)
        self.Type = "King"
        self.attacking = self.squares_attacking(board)
    
    def squares_attacking(self, board):
        # @return: a list of tuples representing the spaces the piece is attacking
        validMoves = []
        # check if king can move to each of the 8 possible squares
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i != 0 or j != 0:
                    if self.row + i >= 0 and self.row + i < board.get_rows() and self.col + j >= 0 and self.col + j < board.get_columns():
                        validMoves.append((self.row + i, self.col + j))
        return validMoves

    def get_valid_moves(self, board, enPassant = None, overwrite = False, selfCapture = False, castlingState = (True, True, True, True)):
        # @param board: the current board state as integer array
        # @param enPassant: the current enPassant state as a tuple (row, col)
        # @param overwrite: a boolean representing whether the move is an overwrite
        # @param selfCapture: a boolean representing whether the move is a selfCapture
        # @param castlingState: a tuple representing the castling state of the board
        # @return: a list of tuples representing the valid moves for the piece

        validMoves = []
        # check if king can move to each of the 8 possible squares
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i != 0 or j != 0:
                    if self.row + i >= 0 and self.row + i < board.get_rows() and self.col + j >= 0 and self.col + j < board.get_columns():
                        if (board.get_pieces()[self.row + i][self.col + j].Type == "Empty" or board.get_pieces()[self.row + i][self.col + j].is_capturable(self, selfCapture)) and not board.space_under_attack(self.row + i, self.col + j, self.color):
                            validMoves.append((self.row + i, self.col + j))
        
        # check if castling is possible
        if self.color == 'white':
            if castlingState[0] and board.get_pieces()[7][1].Type == "Empty" and board.get_pieces()[7][2].Type == "Empty" and board.get_pieces()[7][3].Type == "Empty" and not board.space_under_attack(7, 2, self.color) and not board.space_under_attack(7, 3, self.color):
                validMoves.append((7, 2))
            if castlingState[1] and board.get_pieces()[7][5].Type == "Empty" and board.get_pieces()[7][6].Type == "Empty" and not board.space_under_attack(7, 5, self.color) and not board.space_under_attack(7, 6, self.color):
                validMoves.append((7, 6))
        else:
            if castlingState[2] and board.get_pieces()[0][1].Type == "Empty" and board.get_pieces()[0][2].Type == "Empty" and board.get_pieces()[0][3].Type == "Empty" and not board.space_under_attack(0, 2, self.color) and not board.space_under_attack(0, 3, self.color):
                validMoves.append((0, 2))
            if castlingState[3] and board.get_pieces()[0][5].Type == "Empty" and board.get_pieces()[0][6].Type == "Empty" and not board.space_under_attack(0, 5, self.color) and not board.space_under_attack(0, 6, self.color):
                validMoves.append((0, 6))
        
        return validMoves


    def is_in_check(self, board):
        if board.space_under_attack(self.row, self.col, self.color):
            return True


class Duck(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.Type = "Duck"

    def move(self):
        pass

    def get_valid_moves(self, board, enPassant = None, overwrite = False, selfCapture = False, castlingState = (True, True, True, True)):
        pass

    def capture(self):
        pass

class CustomPiece1(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.Type = "CustomPiece1"

    def get_valid_moves(self, board, enPassant = None, overwrite = False, selfCapture = False, castlingState = (True, True, True, True)):
        pass

class CustomPiece2(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.Type = "CustomPiece2"

    def get_valid_moves(self, board, enPassant = None, overwrite = False, selfCapture = False, castlingState = (True, True, True, True)):
        pass

class CustomPiece3(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.Type = "CustomPiece3"

    def get_valid_moves(self, board, enPassant = None, overwrite = False, selfCapture = False, castlingState = (True, True, True, True)):
        pass