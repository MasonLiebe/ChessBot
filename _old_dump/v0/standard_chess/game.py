import copy
from pieces import Piece, Empty, Pawn, Rook, Knight, Bishop, Queen, King
import bot_configs

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

                self.en_passant_target = None  # Reset the en passant target
                # check if pawn moved 2 squares for en passant
                if abs(start_pos[0] - end_pos[0]) == 2:
                    self.en_passant_target = (start_pos[0] + (end_pos[0] - start_pos[0]) // 2, start_pos[1])
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
            # check if the king moved
            if isinstance(moving_piece, King):
                self.castle_rights[moving_piece.color]["king_side"] = False
                self.castle_rights[moving_piece.color]["queen_side"] = False
            
            # Check if a rook moved
            if isinstance(moving_piece, Rook):
                if start_pos == (0, 0):
                    self.castle_rights["black"]["queen_side"] = False
                elif start_pos == (0, 7):
                    self.castle_rights["black"]["king_side"] = False
                elif start_pos == (7, 0):
                    self.castle_rights["white"]["queen_side"] = False
                elif start_pos == (7, 7):
                    self.castle_rights["white"]["king_side"] = False

            # Check if a piece took the rook
            if end_pos == (0, 0):
                self.castle_rights["black"]["queen_side"] = False
            elif end_pos == (0, 7):
                self.castle_rights["black"]["king_side"] = False
            elif end_pos == (7, 0):
                self.castle_rights["white"]["queen_side"] = False
            elif end_pos == (7, 7):
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
    
    def play_bot(self):
        """Starts the game loop and handles user input."""
        while True:
            self.display()
            if self.current_player == "white":
                print(f"{self.current_player}'s turn.")
                print('Enter start position (row, col):')
                start_pos = tuple(map(int, input().split(',')))
                print('Enter end position (row, col):')
                end_pos = tuple(map(int, input().split(',')))
                did_move = self.move_piece(start_pos, end_pos)
            else:
                print(f"{self.current_player}'s turn.")
                move = self.minimax(3, float('-inf'), float('inf'), True)[1]
                print(f"Bot move: {move}")
                did_move = self.move_piece(*move)
            
            if not did_move:
                print("Illegal move!")
                continue
            
            self.current_player = "black" if self.current_player == "white" else "white"
            game_state = self.check_status()
            print(game_state)
            if game_state not in ("Normal", "Check!"):
                break
        
    def minimax(self, depth, alpha, beta, maximizing_player):
        """Returns the best move for the current player using the minimax algorithm."""
        # check game end states
        if depth == 0 or self.check_status() in ["Checkmate!", "Stalemate!"]:
            return (self.evaluate_board(), None)
        
        if maximizing_player:
            max_eval = float('-inf')
            for move in self.get_all_possible_moves():
                test_game = copy.deepcopy(self)
                test_game.move_piece(*move)
                eval = test_game.minimax(depth - 1, alpha, beta, False)[0]
                max_eval = max(max_eval, eval)
                if max_eval == eval:
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return (max_eval, best_move)
        else:
            min_eval = float('inf')
            for move in self.get_all_possible_moves():
                test_game = copy.deepcopy(self)
                test_game.move_piece(*move)
                eval = test_game.minimax(depth - 1, alpha, beta, True)[0]
                min_eval = min(min_eval, eval)
                if min_eval == eval:
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return (min_eval, best_move)
        
    def evaluate_board(self):
        """Returns a score for the current board position."""
        piece_values = bot_configs.piece_values
        location_scores = bot_configs.location_scores

        # check game-end states
        match self.check_status():
            case "Checkmate!":
                return float('-inf') if self.current_player == "white" else float('inf')
            case "Stalemate!":
                return 0
        
        # calculate the score if the game is not over
        
        # compute material score
        material_score = 0
        for row in self.board:
            for piece in row:
                if piece.is_empty():
                    continue
                if piece.color == "white":
                    material_score += piece_values[type(piece).__name__]
                else:
                    material_score -= piece_values[type(piece).__name__]
        
        # compute piece location scores
        location_score = 0
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if not piece.is_empty():
                    if piece.color == "white":
                        location_score += location_scores[type(piece).__name__][row][col]
                    else:
                        location_score -= location_scores[type(piece).__name__][7 - row][7-col]
                    # # add king safety score
                    # if isinstance(piece, King):
                    #     location_score += len(self.get_attacked_positions(piece.color)) * bot_configs.evaluation_params['king_safety_weight']
        
        # compute piece mobility score
        # Was removed for performance reasons - value added was minimal
        # mobility_score = 0
        # for row in range(8):
        #     for col in range(8):
        #         piece = self.board[row][col]
        #         if not piece.is_empty():
        #             if piece.color == "white":
        #                 mobility_score += len(piece.possible_moves(self))
        #             else:
        #                 mobility_score -= len(piece.possible_moves(self))

        return material_score * bot_configs.evaluation_params['material_weight'] + location_score * bot_configs.evaluation_params['location_weight']

    def get_all_possible_moves(self):
        """Returns a list of all possible moves for the current player"""
        moves = []
        for row in range(8):
            for col in range(8):
                if self.board[row][col].color == self.current_player:
                    for move in self.board[row][col].possible_moves(self):
                        moves.append(((row, col), move))
        return moves
    

# # test playing against a bot
# if __name__ == "__main__":
#     game = Game()
#     game.play_bot()
#     game.display()
#     print(game.check_status())

