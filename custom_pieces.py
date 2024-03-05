class Piece:
    # general class representing a piece, gracefully handles the movement of all pieces
    directions = {'n': (1,0), 's': (-1,0), 'e': (0,1), 'w': (0,-1), 'ne': (1,1), 'nw': (1,-1), 'se': (-1,1), 'sw': (-1,-1)}
    opposite_direction = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e', 'ne': 'sw', 'nw': 'se', 'se': 'nw', 'sw': 'ne'}

    def __init__(self, color, position = (-1, -1), n = False, s = False, e = False, w = False, ne = False, nw = False, se = False, sw = False, attack_jumps = [], move_jumps = [], traversable = False, landable = False, takeable = True):
        self.color = color
        self.position = position
        self.n = n
        self.s = s
        self.e = e
        self.w = w
        self.ne = ne
        self.nw = nw
        self.se = se
        self.sw = sw
        self.attack_jumps = attack_jumps # a list of tuples representing the jumps a piece can make to attack
        self.move_jumps = move_jumps # a list of tuples representing the jumps a piece can make to move
        self.traversable = traversable # a piece that can be passed through, but taken when landed on
        self.takeable = takeable # a piece that can be taken, empty squares and en passant squares are not takeable
        self.landable = landable # a piece that can be landed on, empty squares and en passant squares are landable

    def get_legal_moves(self, game):
        # parameters: game object
        # returns a set of legal moves for the piece
        legal_moves = set()

        pin_directions = self.is_pinned(game)
        print('pin directions: ', pin_directions)

        # check if the piece is pinned to the king
        if pin_directions: # if the piece is pinned, it can only move toward and away from the king
            # iterate through moves that are toward and away from the king
            for direction in pin_directions[:2]:
                if getattr(self, direction, False):
                    i, j = self.position
                    while True:
                        # iterate through the direction until an untraversable space is reached
                        i += jump[0]
                        j += jump[1]
                        if i < 0 or i >= game.rows or j < 0 or j >= game.cols:
                            break
                        if game.board[i][j].traversable: # traversable piece
                            if self.can_take(game, game.board[i][j]) or game.board[i][j].landable: # can take or land on this piece
                                legal_moves.add((i,j))
                            else: # cannot take or land on this piece, but can move beyond it
                                continue

                        else: # non-traversable piece
                            if self.can_take(game, game.board[i][j]): # can take this piece
                                legal_moves.add((i,j))
                            break
            
            # iterate through the attack jumps and add legal moves
            if self.attack_jumps:
                for jump in self.attack_jumps:
                    i, j = self.position
                    i += jump[0]
                    j += jump[1]
                    if (i, j) not in pin_directions[2]: # space is not in the direction of the pin or past the pin
                        continue
                    if self.can_take(game, game.board[i][j]): #takeable piece
                        legal_moves.add((i,j))

            # iterate through the move jumps and add legal moves
            if self.move_jumps:
                for jump in self.move_jumps:
                    i, j = self.position
                    i += jump[0]
                    j += jump[1]
                    if (i, j) not in pin_directions[2]: # space is not in the direction of the pin or past the pin
                        continue
                    if game.board[i][j].landable: # piece can be landed on
                        legal_moves.add((i,j))
        
        else: # piece is not pinned
            # iterate through directions and add legal moves
            for direction, jump in self.directions.items():
                if getattr(self, direction, False):
                    i, j = self.position
                    while True:
                        # iterate through the direction until an untraversable space is reached
                        i += jump[0]
                        j += jump[1]
                        if i < 0 or i >= game.rows or j < 0 or j >= game.cols:
                            break
                        if game.board[i][j].traversable: # traversable piece
                            if self.can_take(game, game.board[i][j]) or game.board[i][j].landable: # can take or land on this piece
                                legal_moves.add((i,j))
                            else: # cannot take or land on this piece, but can move beyond it
                                continue

                        else: # non-traversable piece
                            if self.can_take(game, game.board[i][j]): # can take this piece
                                legal_moves.add((i,j))
                            break
            
            # iterate through the attack jumps and add legal moves
            if self.attack_jumps:
                for jump in self.attack_jumps:
                    i, j = self.position
                    i += jump[0]
                    j += jump[1]
                    if i < 0 or i >= game.rows or j < 0 or j >= game.cols: # space is off the board
                        continue
                    if self.can_take(game, game.board[i][j]): #takeable piece
                        legal_moves.add((i,j))
            
            # iterate through the move jumps and add legal moves
            if self.move_jumps:
                for jump in self.move_jumps:
                    i, j = self.position
                    i += jump[0]
                    j += jump[1]
                    if i < 0 or i >= game.rows or j < 0 or j >= game.cols: # space is off the board
                        continue
                    if game.board[i][j].landable: # piece can be landed on
                        legal_moves.add((i,j))
        
        # check if king can castle:
        if isinstance(self, King):
            if self.color == 'w':
                #implement
                pass
        return legal_moves

    def can_take(self, game, piece):
        # parameters: piece object attempting to be taken
        # returns True if the piece can be taken, False otherwise
        if (isinstance(piece, enPassant) and isinstance(self,Pawn)) or piece.takeable:
            return (self.color != piece.color or game.self_capture)
        return False

    def move(self, game, move):
        # parameters: game object, move as a destination tuple
        # updates the game board with the move
        game.board[self.position[0]][self.position[1]] = Empty(self.position)
        game.board[move[0]][move[1]] = self
        self.position = move

    def is_pinned(self, game):
        # parameters: game object
        # returns the direction and location of attacking piece if the piece is pinned to the king, False otherwise
        if game.king_capture: # if king capture is allowed, pieces cannot be pinned
            return False
        
        valid_locations = set() # set of valid locations for the piece to move to

        # identify if king is in the same row, column, or diagonal as the piece
        king_location = (-1, -1)
        king_direction = False
        for direction, jump in self.directions.items():
            i, j = self.position
            print(i, j, type(i), type(j))
            while True:
                # iterate through the direction until an untraversable space is reached
                i += jump[0]
                j += jump[1]
                if i < 0 or i >= game.rows or j < 0 or j >= game.cols:
                    break
                if isinstance(game.board[i][j], King):
                    king_location = (i, j)
                    king_direction = direction
                    break
                if not game.board[i][j].traversable: # non-traversable piece
                    valid_locations.add((i, j))
                    break
                valid_locations.add((i, j))

            if king_location != (-1, -1): # king is found
                break
        
        if king_location == (-1, -1): # no king found
            return False
        
        # check if the piece is pinned to the king
        opposite_direction = self.opposite_direction[king_direction]
        i, j = self.position
        while True:
            # iterate through the direction until an untraversable space is reached
            i += self.directions[opposite_direction][0]
            j += self.directions[opposite_direction][1]
            if i < 0 or i >= game.rows or j < 0 or j >= game.cols:
                break
            if not (isinstance(game.board[i][j], Empty) or isinstance(game.board[i][j], enPassant)): # non-empty piece
                # check if piece pins the king
                if game.board[i][j].color != self.color and getattr(game.board[i][j], king_direction, False):
                    valid_locations.add((i, j))
                    return (king_direction, opposite_direction, valid_locations)
                if not game.board[i][j].traversable:
                    break
            valid_locations.add((i, j))

        return False # piece is not pinned


class Queen(Piece):
    # standard queen piece
    def __init__(self, color, position = (-1, -1)):
        super().__init__(color, position, n = True, s = True, e = True, w = True, ne = True, nw = True, se = True, sw = True)

class King(Piece):
    # standard king piece
    def __init__(self, color, position = (-1, -1)):
        super().__init__(color, position, move_jumps=[(1,0), (-1,0), (0,1), (0,-1), (1,1), (1,-1), (-1,1), (-1,-1)], attack_jumps=[(1,0), (-1,0), (0,1), (0,-1), (1,1), (1,-1), (-1,1), (-1,-1)])

    #TODO: override move method to handle castling
        
class Rook(Piece):
    # standard rook piece
    def __init__(self, color, position = (-1, -1)):
        super().__init__(color, position, n = True, s = True, e = True, w = True)
    
class Bishop(Piece):
    # standard bishop piece
    def __init__(self, color, position = (-1, -1)):
        super().__init__(color, position, ne = True, nw = True, se = True, sw = True)

class Knight(Piece):
    # standard knight piece
    def __init__(self, color, position = (-1, -1)):
        super().__init__(color, position, attack_jumps = [(1,2), (2,1), (-1,2), (-2,1), (1,-2), (2,-1), (-1,-2), (-2,-1)], move_jumps = [(1,2), (2,1), (-1,2), (-2,1), (1,-2), (2,-1), (-1,-2), (-2,-1)])
                         
class Pawn(Piece):
    # standard pawn piece
    def __init__(self, color, position = (-1, -1)):
        if color == "w":
            super().__init__(color, position, attack_jumps = [(-1,1), (-1,-1)], move_jumps = [(-1,0), (-2,0)])
        else:
            super().__init__(color, position, attack_jumps = [(1,1), (1,-1)], move_jumps = [(1,0), (2,0)])
    
    # override legal moves to handle 2-square move and promotion
    def move(self, game, move):
        # parameters: game object, move as a destination tuple
        if abs(self.position[0] - move[0]) == 2: # 2 square move
            if self.color == "w":
                game.board[move[0]+1][move[1]] = enPassant('w', (move[0]+1, move[1]))
            else:
                game.board[move[0]-1][move[1]] = enPassant('b', (move[0]-1, move[1]))
        
        # update move jumps so that it can only move one square
        if self.color == 'w':
            self.move_jumps = [(-1, 0)]
        else:
            self.move_jumps = [(1, 0)]

        # updates the game board with the move
        game.board[self.position[0]][self.position[1]] = Empty(self.position)
        game.board[move[0]][move[1]] = self
        self.position = move
    

class Empty(Piece):
    # empty space
    def __init__(self, position = (-1, -1)):
        super().__init__('e',  position, traversable=True, takeable=False, landable=True)

class enPassant(Piece):
    # empty square that can be taken by en passant
    def __init__(self, color, position):
        super().__init__(color, position, traversable=True, takeable=False, landable=True)

        # mark the pawn that can be taken by en passant
        if color == "w":
            self.removable_pawn = (position[0]-1, position[1])
        else:
            self.removable_pawn = (position[0]+1, position[1])
        
