class Piece:
    # general class representing a piece, gracefully handles the movement of all pieces
    directions = {'n': (1,0), 's': (-1,0), 'e': (0,1), 'w': (0,-1), 'ne': (1,1), 'nw': (1,-1), 'se': (-1,1), 'sw': (-1,-1)}
    opposite_direction = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e', 'ne': 'sw', 'nw': 'se', 'se': 'nw', 'sw': 'ne'}

    def __init__(self, color, position = (-1, -1), n = False, s = False, e = False, w = False, ne = False, nw = False, se = False, sw = False, attack_jumps = [], move_jumps = [], traversable = False, landable = False, takeable = True, new = True):
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
        # returns a set of legal moves for the piece given the game state
        legal_moves = set()
        vision = self.get_vision(game)
        mobility = self.get_mobility(game)

        # check if the piece is the right color
        if self.color != game.turn:
            return legal_moves
        
        # handle case where player is in check
        if game.game_state == 'check':
            checking_pieces = set() # dictionary saying jump or direction-based checks
            # find the king that is in check
            king = game.white_king if self.color == 'w' else game.black_king
            
            # iterate through board to find pieces checking the king
            for row in game.board:
                for piece in row:
                    if piece.color != game.turn:
                        for move in piece.get_vision(game):
                            if move == king.position:
                                checking_pieces.add(piece)
            print([piece.position for piece in checking_pieces])
            
            if len(checking_pieces) == 1:
                checking_piece = checking_pieces.pop()
                # check if piece is attacking via attack jumps
                for jump in checking_piece.attack_jumps:
                    i, j = checking_piece.position
                    i += jump[0]
                    j += jump[1]
                    if (i, j) == king.position:
                        # king must move or the checking piece must be taken
                        if isinstance(self, King):
                            for move in vision:
                                opposite_color = 'b' if game.turn == 'w' else 'w'
                                if (not game.square_is_attacked(move, opposite_color)) and self.can_move_to(game, move):
                                    legal_moves.add(move)
                        else:
                            # piece must be taken
                            if checking_piece.position in vision:
                                legal_moves.add(checking_piece.position)
                
                # check if piece is attacking via direction
                for direction, jump in checking_piece.directions.items():
                    if getattr(checking_piece, direction, False):
                        i, j = checking_piece.position
                        blocking_squares = set() # squares that can block a potential attack
                        while True:
                            # iterate through the direction until an untraversable space is reached
                            i += jump[0]
                            j += jump[1]
                            blocking_squares.add((i, j))
                            if i < 0 or i >= game.rows or j < 0 or j >= game.cols:
                                break
                            if (i, j) == king.position: # piece sees the king
                                # king must move or the checking piece must be taken or blcocked
                                if isinstance(self, King):
                                    for move in vision:
                                        opposite_color = 'b' if game.turn == 'w' else 'w'
                                        if (not game.square_is_attacked(move, opposite_color)) and self.can_move_to(game, move):
                                            legal_moves.add(move)
                                else:
                                    # checking piece can be taken
                                    if checking_piece.position in vision:
                                        legal_moves.add(checking_piece.position)
                                    # or piece can be blocked
                                    for square in blocking_squares:
                                        if square in mobility:
                                            legal_moves.add(square) # piece can block the attack
                                break
            else:
                # king must move
                if isinstance(self, King):
                    for move in vision:
                        if move not in checking_pieces:
                            legal_moves.add(move)
            return legal_moves

        pin_directions = self.is_pinned(game)

        # check if the piece is pinned to the king
        if pin_directions: # if the piece is pinned, it can only move toward and away from the king
            # iterate through moves that are toward and away from the king
            for direction in pin_directions[:2]:
                if getattr(self, direction, False):
                    i, j = self.position
                    jump = self.directions[direction]
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
        
        # check if king can castle or if it moves into check:
        if isinstance(self, King):
            if self.color == 'w':
                # check if player can queenside castle
                if 'Q' in game.castle_rights:
                    rook_col = game.castle_rooks['Q'][1]
                    can_castle = True
                    # check that the squares between the king and rook are traversable
                    for col in range(rook_col + 1, self.position[1]):
                        if not game.board[self.position[0]][col].traversable:
                            print('cannot castle queenside', (self.position[0], col), 'is not traversable')
                            can_castle = False
                            break
                    # check that the 2 squares left of the king are not attacked
                    if can_castle:
                        for col in range(self.position[1] - 1, self.position[1] - 3, -1):
                            if game.square_is_attacked((self.position[0], col), 'b'):
                                print('cannot castle queenside', (self.position[0], col), 'is attacked')
                                can_castle = False
                                break
                        if can_castle:
                            legal_moves.add((self.position[0], self.position[1] - 2))
                if 'K' in game.castle_rights:
                    rook_col = game.castle_rooks['K'][1]
                    can_castle = True
                    # check that the squares between the king and rook are traversable
                    for col in range(self.position[1] + 1, rook_col):
                        if not game.board[self.position[0]][col].traversable:
                            print('cannot castle kingside', (self.position[0], col), 'is not traversable')
                            can_castle = False
                            break
                    # check that the 2 squares right of the king are not attacked
                    if can_castle:
                        for col in range(self.position[1] + 1, self.position[1] + 3):
                            if game.square_is_attacked((self.position[0], col), 'b'):
                                print('cannot castle kingside', (self.position[0], col), 'is attacked')
                                can_castle = False
                                break
                        if can_castle:
                            legal_moves.add((self.position[0], self.position[1] + 2))
                        
            else:
                # check if player can queenside castle
                if 'q' in game.castle_rights:
                    rook_col = game.castle_rooks['q'][1]
                    can_castle = True
                    # check that the squares between the king and rook are traversable
                    for col in range(rook_col + 1, self.position[1]):
                        if not game.board[self.position[0]][col].traversable:
                            print('cannot castle queenside', (self.position[0], col), 'is not traversable')
                            can_castle = False
                            break
                    # check that the 2 squares left of the king are not attacked
                    if can_castle:
                        for col in range(self.position[1] - 1, self.position[1] - 3, -1):
                            if game.square_is_attacked((self.position[0], col), 'w'):
                                print('cannot castle queenside', (self.position[0], col), 'is attacked')
                                can_castle = False
                                break
                        if can_castle:
                            legal_moves.add((self.position[0], self.position[1] - 2))

                if 'k' in game.castle_rights:
                    rook_col = game.castle_rooks['k'][1]
                    can_castle = True
                    # check that the squares between the king and rook are traversable
                    for col in range(self.position[1] + 1, rook_col):
                        if not game.board[self.position[0]][col].traversable:
                            print('cannot castle kingside', (self.position[0], col), 'is not traversable')
                            can_castle = False
                            break
                    # check that the 2 squares right of the king are not attacked
                    if can_castle:
                        for col in range(self.position[1] + 1, self.position[1] + 3):
                            if game.square_is_attacked((self.position[0], col), 'w'):
                                print('cannot castle kingside', (self.position[0], col), 'is attacked')
                                can_castle = False
                                break
                        if can_castle:
                            legal_moves.add((self.position[0], self.position[1] + 2))
            
            # check if the king moves into check
            for move in list(legal_moves):
                if game.square_is_attacked(move, 'b' if self.color == 'w' else 'w'):
                    legal_moves.remove(move)

        # check if pawn is trying to jump over a piece:
        if isinstance(self, Pawn):
            for move in list(legal_moves):
                if abs(self.position[0] - move[0]) == 2:
                    # if the move is 2 squares, check if the square in between is a legal move
                    if self.color == 'w':
                        if (move[0] + 1, move[1]) not in legal_moves:
                            legal_moves.remove(move)
                    else:
                        if (move[0] - 1, move[1]) not in legal_moves:
                            legal_moves.remove(move)

        return legal_moves
    
    def get_vision(self, game):
        # parameters: game object
        # returns a set of all the squares that the piece can see, disregarding pins and checks
        vision = set()
        for direction, jump in self.directions.items():
            if getattr(self, direction, False):
                i, j = self.position
                while True:
                    # iterate through the direction until an untraversable space is reached
                    i += jump[0]
                    j += jump[1]
                    if i < 0 or i >= game.rows or j < 0 or j >= game.cols:
                        break
                    vision.add((i, j))
                    if not game.board[i][j].traversable:
                        break
        
        for jump in self.attack_jumps:
            i, j = self.position
            i += jump[0]
            j += jump[1]
            if i < 0 or i >= game.rows or j < 0 or j >= game.cols:
                continue
            vision.add((i, j))
        
        return vision
    
    def get_mobility(self, game):
        # parameters: game object
        # returns a set of all the squares that the piece can move to, disregarding pins and checks
        mobility = set()
        for direction, jump in self.directions.items():
            if getattr(self, direction, False):
                i, j = self.position
                while True:
                    # iterate through the direction until an untraversable space is reached
                    i += jump[0]
                    j += jump[1]
                    if i < 0 or i >= game.rows or j < 0 or j >= game.cols:
                        break
                    if game.board[i][j].traversable:
                        mobility.add((i, j))
                    else:
                        if self.can_take(game, game.board[i][j]):
                            mobility.add((i, j))
                        break

        # iterate through the attack jumps and add legal moves
        for jump in self.attack_jumps:
            i, j = self.position
            i += jump[0]
            j += jump[1]
            if i < 0 or i >= game.rows or j < 0 or j >= game.cols:
                continue
            if self.can_take(game, game.board[i][j]):
                mobility.add((i,j))

        # iterate through the move jumps and add legal moves
        for jump in self.move_jumps:
            i, j = self.position
            i += jump[0]
            j += jump[1]
            if i < 0 or i >= game.rows or j < 0 or j >= game.cols:
                continue
            if game.board[i][j].landable:
                mobility.add((i,j))

        return mobility

    def can_take(self, game, piece):
        # parameters: piece object attempting to be taken
        # returns True if the piece can be taken, False otherwise
        if (isinstance(piece, enPassant) and isinstance(self,Pawn)) or piece.takeable:
            return (self.color != piece.color or game.self_capture)
        return False
    
    def can_move_to(self, game, move):
        # if it's a king, check if it moves into check
        if isinstance(self, King):
            if game.square_is_attacked(move, 'b' if self.color == 'w' else 'w'):
                print(move, "is into check")
                return False
        # otherwise, check if it can take or land on the piece 
            print('still in can move to: ', game.board[move[0]][move[1]].landable or self.can_take(game, game.board[move[0]][move[1]]))
        return game.board[move[0]][move[1]].landable or self.can_take(game, game.board[move[0]][move[1]])

    def move(self, game, move):
        # parameters: game object, move as a destination tuple
        # updates the game board with the move
        game.board[self.position[0]][self.position[1]] = Empty(self.position)
        game.board[move[0]][move[1]] = self
        self.position = move

        # check if rook is taken for castle rights
        if move in game.castle_rooks.values():
            if move == game.castle_rooks['Q']:
                game.castle_rights = game.castle_rights.replace('Q', '')
            elif move == game.castle_rooks['K']:
                game.castle_rights = game.castle_rights.replace('K', '')
            elif move == game.castle_rooks['q']:
                game.castle_rights = game.castle_rights.replace('q', '')
            elif move == game.castle_rooks['k']:
                game.castle_rights = game.castle_rights.replace('k', '')

    
    def force_move(self, game, move):
        # parameters: game object, move as a destination tuple
        # updates the game board with the move - DOESN'T CHECK IF THE MOVE IS LEGAL OR EN PASSANT
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

    def move(self, game, move):
        # parameters: game object, move as a destination tuple
        # update castle rights if the king moves
        if self.color == 'w':
            game.castle_rights = game.castle_rights.replace('Q', '').replace('K', '')
            # check if the king is castling
            if self.position[1] - move[1] == 2: # castiling queenside
                # move king to the move square
                game.board[self.position[0]][self.position[1]] = Empty(self.position)
                game.board[move[0]][move[1]] = self
                self.position = move
                # move the rook one to the right of the move square
                game.board[self.position[0]][self.position[1]+1] = Rook('w', (self.position[0], self.position[1]+1))
                game.board[self.position[0]][game.castle_rooks['Q'][1]] = Empty((self.position[0], game.castle_rooks['Q'][1]))
            elif move[1] - self.position[1] == 2: # castling kingside
                # move king to the move square
                game.board[self.position[0]][self.position[1]] = Empty(self.position)
                game.board[move[0]][move[1]] = self
                self.position = move
                # move the rook one to the left of the move square
                game.board[self.position[0]][self.position[1]-1] = Rook('w', (self.position[0], self.position[1]-1))
                game.board[self.position[0]][game.castle_rooks['K'][1]] = Empty((self.position[0], game.castle_rooks['K'][1]))
            else: # normal move
                game.board[self.position[0]][self.position[1]] = Empty(self.position)
                game.board[move[0]][move[1]] = self
                self.position = move
        else:
            game.castle_rights = game.castle_rights.replace('q', '').replace('k', '')
            # check if the king is castling
            if self.position[1] - move[1] == 2: # castiling queenside
                # move king to the move square
                game.board[self.position[0]][self.position[1]] = Empty(self.position)
                game.board[move[0]][move[1]] = self
                self.position = move
                # move the rook one to the right of the move square
                game.board[self.position[0]][self.position[1]+1] = Rook('b', (self.position[0], self.position[1]+1))
                game.board[self.position[0]][game.castle_rooks['q'][1]] = Empty((self.position[0], game.castle_rooks['q'][1]))
            elif move[1] - self.position[1] == 2: # castling kingside
                # move king to the move square
                game.board[self.position[0]][self.position[1]] = Empty(self.position)
                game.board[move[0]][move[1]] = self
                self.position = move
                # move the rook one to the left of the move square
                game.board[self.position[0]][self.position[1]-1] = Rook('b', (self.position[0], self.position[1]-1))
                game.board[self.position[0]][game.castle_rooks['k'][1]] = Empty((self.position[0], game.castle_rooks['k'][1]))
            else: # normal move
                game.board[self.position[0]][self.position[1]] = Empty(self.position)
                game.board[move[0]][move[1]] = self
                self.position = move
        
        if move in game.castle_rooks.values():
            if move == game.castle_rooks['Q']:
                game.castle_rights = game.castle_rights.replace('Q', '')
            elif move == game.castle_rooks['K']:
                game.castle_rights = game.castle_rights.replace('K', '')
            elif move == game.castle_rooks['q']:
                game.castle_rights = game.castle_rights.replace('q', '')
            elif move == game.castle_rooks['k']:
                game.castle_rights = game.castle_rights.replace('k', '')
        

        
class Rook(Piece):
    # standard rook piece
    def __init__(self, color, position = (-1, -1)):
        super().__init__(color, position, n = True, s = True, e = True, w = True)
    
    # override move to update castle rights
    def move(self, game, move):
        # parameters: game object, move as a destination tuple
        # update castle rights if the rook moves
        if self.color == 'w':
            if self.position == game.castle_rooks['Q']:
                game.castle_rights = game.castle_rights.replace('Q', '')
            elif self.position == game.castle_rooks['K']:
                game.castle_rights = game.castle_rights.replace('K', '')
        else:
            if self.position == game.castle_rooks['q']:
                game.castle_rights = game.castle_rights.replace('q', '')
            elif self.position == game.castle_rooks['k']:
                game.castle_rights = game.castle_rights.replace('k', '')
        game.board[self.position[0]][self.position[1]] = Empty(self.position)
        game.board[move[0]][move[1]] = self
        self.position = move

        if move in game.castle_rooks.values():
            if move == game.castle_rooks['Q']:
                game.castle_rights = game.castle_rights.replace('Q', '')
            elif move == game.castle_rooks['K']:
                game.castle_rights = game.castle_rights.replace('K', '')
            elif move == game.castle_rooks['q']:
                game.castle_rights = game.castle_rights.replace('q', '')
            elif move == game.castle_rooks['k']:
                game.castle_rights = game.castle_rights.replace('k', '')
    
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
        
        # if the pawn is at the end of the board, promote it to a queen
        if move[0] == 0 or move[0] == game.rows-1:
            game.board[self.position[0]][self.position[1]] = Empty(self.position)
            game.board[move[0]][move[1]] = Queen(self.color, move)
        else:
            # updates the game board with the move
            game.board[self.position[0]][self.position[1]] = Empty(self.position)
            game.board[move[0]][move[1]] = self
            self.position = move
        
        if move in game.castle_rooks.values():
            if move == game.castle_rooks['Q']:
                game.castle_rights = game.castle_rights.replace('Q', '')
            elif move == game.castle_rooks['K']:
                game.castle_rights = game.castle_rights.replace('K', '')
            elif move == game.castle_rooks['q']:
                game.castle_rights = game.castle_rights.replace('q', '')
            elif move == game.castle_rooks['k']:
                game.castle_rights = game.castle_rights.replace('k', '')


    
    def remove_double_move(self):
        # parameters: game object, move as a destination tuple
        # remove en passant square if the pawn moves to the square
        if (-2, 0) in self.move_jumps:
            self.move_jumps.remove((-2, 0))
        if (2, 0) in self.move_jumps:
            self.move_jumps.remove((2, 0))
    

class Empty(Piece):
    # empty space
    def __init__(self, position = (-1, -1)):
        super().__init__('e',  position, traversable=True, takeable=False, landable=True)

class enPassant(Piece):
    # empty square that can be taken by en passant
    def __init__(self, color, position):
        super().__init__(color, position, traversable=True, takeable=False, landable=True)
