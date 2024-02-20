from v1.pieces import Piece, Pawn, Knight, Bishop, Rook, Queen, King, CustomPiece1, CustomPiece2, CustomPiece3, Duck, Empty

class Board:
    # Class representing the chess game and board
    # Contains the board state and methods for checking game end state and piece movement

    def __init__(self, rows, columns, board_state=None, white = True):
        self.rows = rows
        self.columns = columns
        if board_state is None:
            self.board_state = [[0] * columns for _ in range(rows)]
            self.board_pieces = [[Empty(i, j, "yellow", self) for j in range(columns)] for i in range(rows)]
        else:
            self.set_board(board_state)
        
        for i in range(rows):
            for j in range(columns):
                if self.board_pieces[i][j].Type != "Empty":
                    self.board_pieces[i][j].attacking = self.board_pieces[i][j].squares_attacking(self)
        
        self.white = white # white is the player who moves first

    def get_board(self):
        return self.board_state
    
    def get_pieces(self):
        return self.board_pieces

    def get_rows(self):
        return self.rows

    def get_columns(self):
        return self.columns
    
    def set_board(self, board_state):
        self.board_state = board_state
        self.board_pieces = [[Empty(i, j, "yellow", self) for j in range(self.columns)] for i in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.columns):
                self.board_state[i][j] = board_state[i][j]
                match board_state[i][j]:
                    case 0:
                        self.board_pieces[i][j] = Empty(i, j, "yellow", self)
                    case 1:
                        self.board_pieces[i][j] = Pawn(i, j, "white", self)
                    case 2:
                        self.board_pieces[i][j] = Pawn(i, j, "black", self)
                    case 3:
                        self.board_pieces[i][j] = Knight(i, j, "white", self)
                    case 4:
                        self.board_pieces[i][j] = Knight(i, j, "black", self)
                    case 5:
                        self.board_pieces[i][j] = Bishop(i, j, "white", self)
                    case 6:
                        self.board_pieces[i][j] = Bishop(i, j, "black", self)
                    case 7:
                        self.board_pieces[i][j] = Rook(i, j, "white", self)
                    case 8:
                        self.board_pieces[i][j] = Rook(i, j, "black", self)
                    case 9:
                        self.board_pieces[i][j] = Queen(i, j, "white", self)
                    case 10:
                        self.board_pieces[i][j] = Queen(i, j, "black", self)
                    case 11:
                        self.board_pieces[i][j] = King(i, j, "white", self)
                    case 12:
                        self.board_pieces[i][j] = King(i, j, "black", self)
                    case 13:
                        self.board_pieces[i][j] = CustomPiece1(i, j, "white", self)
                    case 14:
                        self.board_pieces[i][j] = CustomPiece1(i, j, "black", self)
                    case 15:
                        self.board_pieces[i][j] = CustomPiece2(i, j, "white", self)
                    case 16:
                        self.board_pieces[i][j] = CustomPiece2(i, j, "black", self)
                    case 17:
                        self.board_pieces[i][j] = CustomPiece3(i, j, "white", self)
                    case 18:
                        self.board_pieces[i][j] = CustomPiece3(i, j, "black", self)
                    case 19:
                        self.board_pieces[i][j] = Duck(i, j, "yellow", self)
    
    def get_board_pieces(self):
        return self.board_pieces
        
    
    def get_black_pieces(self):
        pieces = []
        for i in range(self.rows):
            for j in range(self.columns):
                if self.board_pieces[i][j] and self.board_pieces[i][j].color == "black":
                    pieces.append(self.board_pieces[i][j])
        return pieces
    
    def get_white_pieces(self):
        pieces = []
        for i in range(self.rows):
            for j in range(self.columns):
                if self.board_pieces[i][j] and self.board_pieces[i][j].color == "white":
                    pieces.append(self.board_pieces[i][j])
        return pieces

    def is_checkmate(self, white):
        if self.is_check(white):
            if self.is_stalemate(white):
                return white
            return white
    
    def is_stalemate(self, white):
        # for each piece of the current player, check if there are any legal moves
        if white:
            pieces = self.get_white_pieces()
            for piece in pieces:
                if piece.get_legal_moves(self):
                    return False
            return True
        else:
            pieces = self.get_black_pieces()
            for piece in pieces:
                if piece.get_legal_moves(self):
                    return False
            return True
        
    
    def is_check(self, white):
        if white:
            for piece in self.get_white_pieces():
                if piece.isinstance(King):
                    if self.space_under_attack(piece.row, piece.col, white):
                        return True
        else:
            for piece in self.get_black_pieces():
                if piece.isinstance(King):
                    if self.space_under_attack(piece.row, piece.col, white):
                        return True
    
    def space_under_attack(self, row, col, white):
        # @param row: int
        # @param col: int
        # @param white: boolean
        # @return: boolean

        # iterate through opposing pieces and check if they can attack the space
        if white:
            pieces = self.get_black_pieces()
            for piece in pieces:
                if (row, col) in piece.squares_attacking(self):
                    return True
        else:
            pieces = self.get_white_pieces()
            for piece in pieces:
                if (row, col) in piece.squares_attacking(self):
                    return True
        return False
    
    def print_board(self):
        for i in range(self.rows):
            for j in range(self.columns):
                print(self.board_state[i][j], end=" ")
            print()

    def move_piece(self, piece, row, col):
        # @param piece: Piece
        # @param row: int
        # @param col: int
        # @return: None

        # move the piece to the new position and update the board state
        self.board_state[row][col] = self.board_state[piece.row][piece.col]
        self.board_state[piece.row][piece.col] = 0
        self.board_pieces[piece.row][piece.col] = Empty(piece.row, piece.col, "yellow", self)
        self.board_pieces[row][col] = piece
        piece.row = row
        piece.col = col
        piece.attacking = piece.squares_attacking(self)
    
    def can_move(self, piece, row, col):
        # @param piece: Piece
        # @param row: int
        # @param col: int
        # @return: boolean

        # check if the move is valid
        if (row, col) in piece.get_valid_moves(self):
            return True
        return False


#create a board with the starting position and print it
board_state = [[8, 4, 6, 10, 12, 6, 4, 8],
               [2, 2, 2,  2,  0, 2, 2, 2],
               [0, 0, 0,  0,  0, 0, 0, 0],
               [0, 0, 0,  0,  2, 0, 0, 0],
               [0, 0, 0,  0,  1, 0, 0, 0],
               [0, 0, 0,  0,  0, 0, 0, 0],
               [1, 1, 1,  1,  0, 1, 1, 1],
               [7, 3, 5,  9, 11, 5, 3, 7]]

board = Board(8, 8, board_state)

board.print_board()

for piece in board.get_white_pieces():
    print(piece.Type, (piece.row, piece.col))
    print(piece.get_valid_moves(board))
