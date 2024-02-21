from pieces import Piece, Empty, Pawn, Rook, Knight, Bishop, Queen, King

class Game:
    def __init__(self):
        """Initializes the chess board with pieces in their starting positions."""
        self.board = self.setup_board()
        self.current_player = "white" # The player who is to move
        self.en_passant_target = None  # A pawn that can be captured via en passant
        self.castle_rights = {"white": {"king_side": True, "queen_side": True},
                              "black": {"king_side": True, "queen_side": True}}

    def setup_board(self):
        """Sets up the board with pieces in their initial positions.
        This should return a 2D array (8x8) with each cell containing either
        a Piece instance or None."""
        # Initialize an 8x8 board with None
        board = [[None for _ in range(8)] for _ in range(8)]
        # Black's back rank is row 0
        board[0] = [Rook   ('black', (0, 0)),
                    Knight ('black', (0, 1)),
                    Bishop ('black', (0, 2)),
                    Queen  ('black', (0, 3)),
                    King   ('black', (0, 4)),
                    Bishop ('black', (0, 5)),
                    Knight ('black', (0, 6)),
                    Rook   ('black', (0, 7))]
        # Set black's pawns in row 1
        board[1] = [Pawn('black', (1, col)) for col in range(8)]
        # Next 4 ranks are empty
        for row in range(2, 6):
            board[row] = [Empty('', (row, col)) for col in range(8)]
        # Set white's pawns in row 6
        board[6] = [Pawn('white', (6, col)) for col in range(8)]
        # White's back rank is row 7
        board[7] = [Rook   ('white', (7, 0)),
                    Knight ('white', (7, 1)),
                    Bishop ('white', (7, 2)),
                    Queen  ('white', (7, 3)),
                    King   ('white', (7, 4)),
                    Bishop ('white', (7, 5)),
                    Knight ('white', (7, 6)),
                    Rook   ('white', (7, 7))]

        return board

    def reset_game(self):
        # resets to the standard initial game state
        self.board = self.setup_board()
        self.current_player = "white"
        self.en_passant_target = None
        self.castle_rights = {"white": {"king_side": True, "queen_side": True},
                              "black": {"king_side": True, "queen_side": True}}

    def move_piece(self, start_pos, end_pos):
        """Moves a piece from start_pos to end_pos if the move is legal.
        start_pos and end_pos should be tuples like (row, col)."""
        if self.is_move_legal(start_pos, end_pos):

            moving_piece = self.board[start_pos[0]][start_pos[1]]
            captured_piece = self.board[end_pos[0]][end_pos[1]] 

            # Perform the move
            self.board[end_pos[0]][end_pos[1]] = moving_piece
            self.board[start_pos[0]][start_pos[1]] = Empty('', start_pos)
            moving_piece.position = end_pos  # Update the piece's position
            
            # handle pawn behaviors
            if isinstance(moving_piece, Pawn):
                # tell the pawn it moved
                moving_piece.has_moved = True
                
                # check if pawn reached the end of the board
                if end_pos[0] == 0 or end_pos[0] == 7:
                    self.board[end_pos[0]][end_pos[1]] = Queen(moving_piece.color, end_pos)
                
                # check if en passant occured
                if end_pos == self.en_passant_target:
                    self.board[end_pos[0] + (1 if moving_piece.color == 'white' else -1)][end_pos[1]] = Empty('', (end_pos[0] + (1 if moving_piece.color == 'white' else -1), end_pos[1]))

                    print("you took en passant")
                    print("set board square {} to empty".format((end_pos[0] + (1 if moving_piece.color == 'black' else -1), end_pos[1])))
                
                self.en_passant_target = None  # Reset the en passant target
                # check if pawn moved 2 squares for en passant
                if abs(start_pos[0] - end_pos[0]) == 2:
                    self.en_passant_target = (start_pos[0] + (end_pos[0] - start_pos[0]) // 2, start_pos[1])
                    print('en passant target:', self.en_passant_target)
            else:
                self.en_passant_target = None
                
        
            # check if castling occured
            if isinstance(moving_piece, King) and abs(start_pos[1] - end_pos[1]) == 2:
                if end_pos[1] == 6:
                    rook = self.board[end_pos[0]][7]
                    self.board[end_pos[0]][5] = rook
                    self.board[end_pos[0]][7] = Empty('', (end_pos[0], 7))
                    rook.position = (end_pos[0], 5)
                else:
                    rook = self.board[end_pos[0]][0]
                    self.board[end_pos[0]][3] = rook
                    self.board[end_pos[0]][0] = Empty('', (end_pos[0], 0))
                    rook.position = (end_pos[0], 3)
            
            # check if castling rights are lost
            if isinstance(moving_piece, King):
                self.castle_rights[moving_piece.color]["king_side"] = False
                self.castle_rights[moving_piece.color]["queen_side"] = False
            if isinstance(moving_piece, Rook):
                if start_pos == (0, 0):
                    self.castle_rights["black"]["queen_side"] = False
                elif start_pos == (0, 7):
                    self.castle_rights["black"]["king_side"] = False
                elif start_pos == (7, 0):
                    self.castle_rights["white"]["queen_side"] = False
                elif start_pos == (7, 7):
                    self.castle_rights["white"]["king_side"] = False
            return True
        else:
            return False

    def get_attacked_positions(self, color):
        """Returns a set of positions that are attacked by the pieces of that color."""
        attacked_positions = []
        for row in self.board:
            for piece in row:
                if piece.color == color:
                    attacked_positions.extend(piece.attacked_positions(self))
        return attacked_positions
    
    def square_attacked(self, color, position):
        """Returns True if the square is attacked by a piece of the given color."""
        return position in self.get_attacked_positions(color)

    def is_move_legal(self, start_pos, end_pos):
        """Checks if a move is legal. This method should be called from move_piece."""
        # Check if the start position contains a piece
        if isinstance(self.board[start_pos[0]][start_pos[1]], Empty):
            return False
        # Check if the piece to move is of the correct color
        if self.board[start_pos[0]][start_pos[1]].color != self.current_player:
            return False
        # Check if the move is in the list of possible moves
        if end_pos in self.board[start_pos[0]][start_pos[1]].possible_moves(self):
            return True
        else:
            return False

    def check_status(self):
        """Checks the current status of the game (e.g., check, checkmate, stalemate)."""
        # if the player to move is in check, checkmate, or stalemate
        if self.is_in_check():
            if self.is_in_stalemate(): 
                return "Checkmate!"
            else:
                return "Check!"
        elif self.is_in_stalemate():
            return "Stalemate!"
        else:
            return "Normal"

    def is_in_check(self):
        """Returns True if the king of the player to move is in check, False otherwise."""
        for row in self.board:
            for piece in row:
                if isinstance(piece, King) and piece.color == self.current_player:
                    king_pos = piece.position
                    break
        opposite_color = "black" if self.current_player == "white" else "white"
        attacked_positions = self.get_attacked_positions(opposite_color)
        return king_pos in attacked_positions
    
    def is_in_stalemate(self):
        """Returns True if the player to move is in stalemate, False otherwise."""
        # if any piece has a possible move, it's not stalemate
        for row in self.board:
            for piece in row:
                if piece.color == self.current_player:
                    if piece.possible_moves(self):
                        return False
        return True

    def display(self):
        """Prints the board to the console (for debugging purposes) or
        updates the GUI representation of the board."""
        for row in self.board:
            print([piece.display for piece in row])

    def play(self):
        """Starts the game loop and handles user input."""
        while True:
            self.display()
            # Get user input and move a piece
            print(f"{self.current_player}'s turn.")
            print('Enter start position (row, col):')
            start_pos = tuple(map(int, input().split(',')))
            print('Enter end position (row, col):')
            end_pos = tuple(map(int, input().split(',')))
            
            did_move = self.move_piece(start_pos, end_pos)
            if not did_move:
                print("Illegal move!")
                continue
            
            self.current_player = "black" if self.current_player == "white" else "white"
            game_state = self.check_status()
            print(game_state)
            if game_state not in ("Normal", "Check!"):
                break
    
    # IMPLEMENTATION OF COMPUTER PLAYER BELOW
        
    def minimax(self, depth, alpha, beta, maximizing_player):
        """Returns the best move for the current player using the minimax algorithm."""
        if depth == 0:
            return self.evaluate_board()
        
        if maximizing_player:
            max_eval = float('-inf')
            for move in self.get_all_possible_moves():
                test_game = game.copy()
                test_game.move_piece(*move)
                eval = test_game.minimax(depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in self.get_all_possible_moves():
                test_game = game.copy()
                test_game.move_piece(*move)
                eval = test_game.minimax(depth - 1, alpha, beta, True)
                test_game.undo_move(move)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval
        
    def evaluate_board(self):
        """Returns a score for the current board position."""
        piece_values = {"Pawn": 1, "Knight": 3, "Bishop": 3, "Rook": 5, "Queen": 9}
        score = 0
        for row in self.board:
            for piece in row:
                if piece.color == "white":
                    score += piece.value
                else:
                    score -= piece.value
        return score

    def get_all_possible_moves(self):
        """Returns a list of all possible moves for the current player"""
        moves = []
        for row in range(8):
            for col in range(8):
                if self.board[row][col].color == self.current_player:
                    for move in self.board[row][col].possible_moves(self):
                        moves.append(((row, col), move))
        return moves

    

    
# if __name__ == "__main__":
#     game = Game()
#     game.display()
#     print(game.check_status())

#     for move in (((6, 4), (4, 4)), ((1, 3), (3, 3)), ((4, 4), (3, 4)), ((1, 5), (3, 5)), ((3, 4), (2, 5)), ((3, 3), (4, 3))):
#         print(move)
#         game.move_piece(*move)
#         print('piece that just moved:', type(game.board[move[1][0]][move[1][1]]).__name__)
#         print('color:', game.board[move[1][0]][move[1][1]].color)
#         print('position:', game.board[move[1][0]][move[1][1]].position)
#         print('possible moves:', game.board[move[1][0]][move[1][1]].possible_moves(game))
#         game.current_player = 'black' if game.current_player == 'white' else 'white'
#         game.display()
#         print(game.check_status())
    
#     game.board = game.setup_board()
#     game.display()
    
#     game.play()

