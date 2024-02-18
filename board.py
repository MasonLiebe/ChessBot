from pieces import Piece, Pawn, Knight, Bishop, Rook, Queen, King, CustomPiece1, CustomPiece2, CustomPiece3, Duck

class Board:
    # Class representing the board
    # Contains the board state and methods for checking game state and piece movement

    def __init__(self, rows, columns, board_state=None):
        self.rows = rows
        self.columns = columns
        if board_state is None:
            self.board_state = [[0] * columns for _ in range(rows)]
            self.board_pieces = [[None] * columns for _ in range(rows)]

        else:
            for i in range(rows):
                for j in range(columns):
                    self.board_state[i][j] = board_state[i][j]
                    match board_state[i][j]:
                        case 1:
                            self.board_pieces[i][j] = Pawn(i, j, "white")
                        case 2:
                            self.board_pieces[i][j] = Pawn(i, j, "black")
                        case 3:
                            self.board_pieces[i][j] = Knight(i, j, "white")
                        case 4:
                            self.board_pieces[i][j] = Knight(i, j, "black")
                        case 5:
                            self.board_pieces[i][j] = Bishop(i, j, "white")
                        case 6:
                            self.board_pieces[i][j] = Bishop(i, j, "black")
                        case 7:
                            self.board_pieces[i][j] = Rook(i, j, "white")
                        case 8:
                            self.board_pieces[i][j] = Rook(i, j, "black")
                        case 9:
                            self.board_pieces[i][j] = Queen(i, j, "white")
                        case 10:
                            self.board_pieces[i][j] = Queen(i, j, "black")
                        case 11:
                            self.board_pieces[i][j] = King(i, j, "white")
                        case 12:
                            self.board_pieces[i][j] = King(i, j, "black")
                        case 13:
                            self.board_pieces[i][j] = CustomPiece1(i, j, "white")
                        case 14:
                            self.board_pieces[i][j] = CustomPiece1(i, j, "black")
                        case 15:
                            self.board_pieces[i][j] = CustomPiece2(i, j, "white")
                        case 16:
                            self.board_pieces[i][j] = CustomPiece2(i, j, "black")
                        case 17:
                            self.board_pieces[i][j] = CustomPiece3(i, j, "white")
                        case 18:
                            self.board_pieces[i][j] = CustomPiece3(i, j, "black")
                        case 19:
                            self.board_pieces[i][j] = Duck(i, j, "yellow")

    def get_board(self):
        return self.board_state
    
    def get_pieces(self):
        return self.board_pieces
    
    def get_black_pieces(self):
        pieces = []
        for i in range(self.rows):
            for j in range(self.columns):
                if self.board_pieces[i][j].color == "black":
                    pieces.append(self.board_pieces[i][j])
        return pieces
    
    def get_white_pieces(self):
        pieces = []
        for i in range(self.rows):
            for j in range(self.columns):
                if self.board_pieces[i][j].color == "white":
                    pieces.append(self.board_pieces[i][j])
        return pieces

    def get_rows(self):
        return self.rows

    def get_columns(self):
        return self.columns

    def is_checkmate(self):
        # Add your checkmate logic here
        return False
    
    def is_stalemate(self):
        # Add your stalemate logic here
        return False
    
    def is_check(self, white):
        # Add your check logic here
        return False
