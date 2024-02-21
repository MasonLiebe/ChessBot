import copy


class Piece:
    def __init__(self, color, position):
        self.color = color  # 'white' or 'black'
        self.position = position  # Position as a tuple (row, col)

    def possible_moves(self, game):
        """Returns a list of possible moves for this piece.
        To be implemented by each specific piece type."""
        raise NotImplementedError("This method should be overridden by subclasses")
    
    def king_in_check(self, game, move):
        """Returns True if the move puts the king in check, False otherwise."""
        # Make the move on a deep copy of the game
        game_copy = copy.deepcopy(game)
        start_pos, end_pos = move
        piece = game_copy.board[start_pos[0]][start_pos[1]]
        game_copy.board[end_pos[0]][end_pos[1]] = piece
        game_copy.board[start_pos[0]][start_pos[1]] = Empty('', start_pos)
        piece.position = end_pos
        # Check if the king is in check
        in_check = game_copy.is_in_check()
        # Undo the move
        game_copy.board[start_pos[0]][start_pos[1]] = piece
        game_copy.board[end_pos[0]][end_pos[1]] = Empty('', end_pos)
        piece.position = start_pos
        return in_check
    
    def is_empty(self):
        # returns true if the type of the piece is Empty
        return isinstance(self, Empty)

class Empty(Piece):

    def __init__(self, color, position):
        super().__init__(color, position)
        self.color = None
        self.display = "--"  # A string to display when printing the board

    def possible_moves(self, game):
        return []

class Pawn(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.has_moved = False # A flag to keep track of whether the pawn has moved
        self.display = self.color[0] + "P"
    
    def attacked_positions(self, game):
        # returns list of attacked positions for the pawn as tuples
        attacked_positions = []
        dir = 1 if self.color == "black" else -1
        if self.position[1] > 0:
            attacked_positions.append((self.position[0] + dir, self.position[1] - 1))
        if self.position[1] < 7:
            attacked_positions.append((self.position[0] + dir, self.position[1] + 1))
        return attacked_positions
    
    def possible_moves(self, game):
        # returns list of possible moves for the pawn as tuples
        possible_moves = []
        dir = 1 if self.color == "black" else -1

        # check if the pawn can move forward 1 or 2 squares
        if game.board[self.position[0] + dir][self.position[1]].color is None:
            possible_moves.append((self.position[0] + dir, self.position[1]))
            if not self.has_moved and game.board[self.position[0] + 2*dir][self.position[1]].color is None:
                possible_moves.append((self.position[0] + 2*dir, self.position[1]))
        
        # check if the pawn can capture diagonally
        opponent_color = "black" if self.color == "white" else "white"
        for position in self.attacked_positions(game):
            if game.board[position[0]][position[1]].color == opponent_color or position == game.en_passant_target:
                possible_moves.append(position)

        # if self.position[1] > 0 and game.board[self.position[0] + dir][self.position[1] - 1].color  is not None and game.board[self.position[0] + dir][self.position[1] - 1].color != self.color:
        #     possible_moves.append((self.position[0] + dir, self.position[1] - 1))
        # if self.position[1] < 7 and game.board[self.position[0] + dir][self.position[1] + 1].color  is not None and game.board[self.position[0] + dir][self.position[1] + 1].color != self.color:
        #     possible_moves.append((self.position[0] + dir, self.position[1] + 1))

        # # check if the pawn can capture en passant
        # if game.en_passant_target == (self.position[0] + dir, self.position[1] - 1):
        #     possible_moves.append((self.position[0] + dir, self.position[1] - 1))

        # remove moves that would put the king in check
        possible_moves = [move for move in possible_moves if not self.king_in_check(game, (self.position, move))]
        print(possible_moves)
        
        return possible_moves


class Knight(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.display = self.color[0] + "N"
    
    def attacked_positions(self, game):
        # returns list of attacked positions for the knight as tuples
        attacked_positions = []
        for dr, dc in [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]:
            r, c = self.position[0] + dr, self.position[1] + dc
            if 0 <= r < 8 and 0 <= c < 8:
                attacked_positions.append((r, c))
        return attacked_positions

    def possible_moves(self, game):
        # returns list of possible moves for the knight as tuples
        possible_moves = []

        for dr, dc in [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]:
            r, c = self.position[0] + dr, self.position[1] + dc
            if 0 <= r < 8 and 0 <= c < 8 and game.board[r][c].color != self.color:
                possible_moves.append((r, c))

        # remove moves that would put the king in check
        possible_moves = [move for move in possible_moves if not self.king_in_check(game, (self.position, move))]
        
        return possible_moves


class Bishop(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.display = self.color[0] + "B"
    
    def attacked_positions(self, game):
        # returns list of attacked positions for the bishop as tuples
        attacked_positions = []

        for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            r, c = self.position[0] + dr, self.position[1] + dc
            while 0 <= r < 8 and 0 <= c < 8:
                attacked_positions.append((r, c))
                if game.board[r][c].color is not None:
                    break
                r, c = r + dr, c + dc
        return attacked_positions

    def possible_moves(self, game):
        # returns list of possible moves for the bishop as tuples
        possible_moves = []

        for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            r, c = self.position[0] + dr, self.position[1] + dc
            while 0 <= r < 8 and 0 <= c < 8:
                if game.board[r][c].color == self.color:
                    break
                possible_moves.append((r, c))
                if game.board[r][c].color is not None:
                    break
                r, c = r + dr, c + dc
        
        # remove moves that would put the king in check
        possible_moves = [move for move in possible_moves if not self.king_in_check(game, (self.position, move))]
        
        return possible_moves

class Rook(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.display = self.color[0] + "R"
    
    def attacked_positions(self, game):
        # returns list of attacked positions for the rook as tuples
        attacked_positions = []

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            r, c = self.position[0] + dr, self.position[1] + dc
            while 0 <= r < 8 and 0 <= c < 8:
                attacked_positions.append((r, c))
                if game.board[r][c].color is not None:
                    break
                r, c = r + dr, c + dc
        return attacked_positions

    def possible_moves(self, game):
        # returns list of possible moves for the rook as tuples
        possible_moves = []

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            r, c = self.position[0] + dr, self.position[1] + dc
            while 0 <= r < 8 and 0 <= c < 8:
                if game.board[r][c].color == self.color:
                    break
                possible_moves.append((r, c))
                if game.board[r][c].color is not None:
                    break
                r, c = r + dr, c + dc
        
        # remove moves that would put the king in check
        possible_moves = [move for move in possible_moves if not self.king_in_check(game, (self.position, move))]

        return possible_moves

class Queen(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.display = self.color[0] + "Q"
    
    def attacked_positions(self, game):
        # returns list of attacked positions for the queen as tuples
        attacked_positions = []

        for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (1, 0), (0, -1), (0, 1)]:
            r, c = self.position[0] + dr, self.position[1] + dc
            while 0 <= r < 8 and 0 <= c < 8:
                attacked_positions.append((r, c))
                if game.board[r][c].color is not None:
                    break
                r, c = r + dr, c + dc
        return attacked_positions

    def possible_moves(self, game):
        # returns list of possible moves for the queen as tuples
        possible_moves = []

        for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (1, 0), (0, -1), (0, 1)]:
            r, c = self.position[0] + dr, self.position[1] + dc
            while 0 <= r < 8 and 0 <= c < 8:
                if game.board[r][c].color == self.color:
                    break
                possible_moves.append((r, c))
                if game.board[r][c].color is not None:
                    break
                r, c = r + dr, c + dc

        # remove moves that would put the king in check
        possible_moves = [move for move in possible_moves if not self.king_in_check(game, (self.position, move))]

        return possible_moves

class King(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.display = self.color[0] + "K"
    
    def attacked_positions(self, game):
        # returns list of attacked positions for the king as tuples
        attacked_positions = []

        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                r, c = self.position[0] + dr, self.position[1] + dc
                if 0 <= r < 8 and 0 <= c < 8:
                    attacked_positions.append((r, c))
        return attacked_positions

    def possible_moves(self, game):
        # returns possible moves for the king as tuples
        possible_moves = []

        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                r, c = self.position[0] + dr, self.position[1] + dc
                if 0 <= r < 8 and 0 <= c < 8 and game.board[r][c].color != self.color:
                    possible_moves.append((r, c))
        
        # check if the king can castle
        if self.color == "white":
            if game.castle_rights["white"]["king_side"] and game.board[7][5].color is None and game.board[7][6].color is None:
                if not game.king_in_check(game, (self.position, (7, 5))) and not game.king_in_check(game, (self.position, (7, 6))):
                    possible_moves.append((7, 6))
            if game.castle_rights["white"]["queen_side"] and game.board[7][1].color is None and game.board[7][2].color is None and game.board[7][3].color is None:
                if not game.king_in_check(game, (self.position, (7, 2))) and not game.king_in_check(game, (self.position, (7, 3))):
                    possible_moves.append((7, 2))
        else:
            if game.castle_rights["black"]["king_side"] and game.board[0][5].color is None and game.board[0][6].color is None:
                if not game.king_in_check(game, (self.position, (0, 5))) and not game.king_in_check(game, (self.position, (0, 6))):
                    possible_moves.append((0, 6))
            if game.castle_rights["black"]["queen_side"] and game.board[0][1].color is None and game.board[0][2].color is None and game.board[0][3].color is None:
                if not game.king_in_check(game, (self.position, (0, 2))) and not game.king_in_check(game, (self.position, (0, 3))):
                    possible_moves.append((0, 2))

        # remove moves that would put the king in check
        possible_moves = [move for move in possible_moves if not self.king_in_check(game, (self.position, move))]

        return possible_moves

