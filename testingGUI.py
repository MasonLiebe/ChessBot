# tkinter gui that handles the playing of a custom game

from os import name
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


class CustomChessGUI(tk.Tk):
    def __init__(self, game, cell_size=60):
        super().__init__()
        # initialize variables
        self.game = game
        self.cell_size = cell_size

        # create the canvas and core gui elements
        self.canvas = tk.Canvas(self, height=self.game.rows * cell_size,
                                width=self.game.cols * cell_size)
        self.canvas.grid(row=0, column=0, columnspan=1)
        self.piece_images = {} # Stores the piece images due to tkinter garbage collection
        self.highlighted_squares = [] # Tracks the highlighted squares for valid moves
        self.game_state_label = tk.Label(self, text="Game State: " + self.game.game_state)
        self.game_state_label.grid(row=1, column=0, columnspan=1)
        self.move_count_label = tk.Label(self, text="Move Count: " + str(self.game.move_count))
        self.move_count_label.grid(row=1, column=1, columnspan=1)
        self.reset_game_button = tk.Button(self, text="Reset Game", command=self.reset_game)
        self.reset_game_button.grid(row=2, column=0, columnspan=1)
        self.undo_move_button = tk.Button(self, text="Undo Move", command=self.undo_move)
        self.undo_move_button.grid(row=3, column=0, columnspan=1)

        # load the piece images and draw the board
        self.load_piece_images()
        self.draw_board()
        self.update_board()

        # set the game state variables
        self.selected_piece_location = None # Tracks the selected piece's (row, col)

        # set the bindings for the canvas and buttons
        self.canvas.bind("<Button-1>", self.canvas_clicked) # left click returns the row and column clicked
    
    ### Methods for handling the board drawing and updating

    def draw_board(self):
        for row in range(self.game.rows):
            for col in range(self.game.cols):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                fill = "antique white" if (row + col) % 2 == 0 else "saddle brown"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline="black")
    
    def load_piece_images(self):
        pieces = ['white-pawn', 'white-bishop', 'white-knight', 'white-rook', 'white-queen', 'white-king',
                'black-pawn', 'black-bishop', 'black-knight', 'black-rook', 'black-queen', 'black-king']
        for piece in pieces:
            path = f'./assets/pieces/{piece}.png'
            img = Image.open(path)
            # Resize the image to 75x75 pixels using the LANCZOS filter
            img = img.resize((self.cell_size, self.cell_size), Image.LANCZOS)
            if img.mode != 'RGBA':
                img = img.convert('RGBA')

            self.piece_images[piece] = ImageTk.PhotoImage(img)
    
    def update_board(self):
        """Places the piece images on the board according to the game state."""
        self.canvas.delete("all")
        self.draw_board()

        for row in range(self.game.rows):
            for col in range(self.game.cols):
                piece = self.game.board[row][col]
                if not (isinstance(piece, Empty) or isinstance(piece, enPassant)):
                    piece_name = piece.__class__.__name__.lower()
                    color = 'white' if piece.color == 'w' else 'black'
                    self.canvas.create_image((col + .5) * self.cell_size, (row + .5) * self.cell_size, image=self.piece_images[f'{color}-{piece_name}'], anchor="c")

        self.game_state_label.config(text="Game State: " + self.game.game_state)

    
    ### Methods for handling the user inputs to the chess board
    
    def canvas_clicked(self, event):
        # get the row and column clicked and returns as a tuple
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        print(f"Clicked on row {row}, col {col}")
        print(f"Selected piece location: {self.selected_piece_location}")
        
        if self.selected_piece_location:
            self.game.execute_move(self.selected_piece_location, (row, col))
            self.selected_piece_location = None
            self.update_board()
        elif not(isinstance(self.game.board[row][col], Empty) or isinstance(self.game.board[row][col], enPassant)): # clicked on an actual piece
            self.selected_piece_location = (row, col)
            self.highlight_legal_moves(row, col)
        else:
            # Clicked on an empty square or outside legal moves
            self.selected_piece = None
            self.update_board()
    
    def highlight_legal_moves(self, row, col):
        """Highlights legal moves for the selected piece."""
        piece = self.game.board[row][col]
        self.highlight_square(row, col, color="green")
        if piece and piece.color == self.game.turn:
            legal_moves = piece.get_legal_moves(self.game)
            for move in legal_moves:
                self.highlight_square(move[0], move[1])

    def highlight_square(self, row, col, color="blue"):
        """Highlight a square to indicate it's a legal move."""
        x1 = col * self.cell_size
        y1 = row * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        # Create a rectangle with a specific color or outline to indicate highlight
        square = self.canvas.create_rectangle(x1, y1, x2, y2, outline=color, width=5, tags="highlight")
        self.highlighted_squares.append(square)
        
    # button functions
    def reset_game(self):
        self.game.reset_game()
        self.update_board()
    
    def undo_move(self):
        self.game.undo_move()
        self.update_board()

if __name__ == "__main__":
    # Example usage
    custom_game = CustomGame(8, 8, starting_board = ['rnbqkbnr',
                                                'pppppppp', 
                                                '········', 
                                                '········', 
                                                '········', 
                                                '········', 
                                                'PPPPPPPP',
                                                'RNBQKBNR'])
    app = CustomChessGUI(custom_game)
    app.mainloop()