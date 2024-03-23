
from os import name
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from engine import Engine
from bitboard import to_index


class EngineGameGUI(tk.Tk):
    def __init__(self, engine, cell_size=60):
        super().__init__()
        # initialize variables
        self.engine = engine
        self.rows = engine.current_position.dimensions.height
        self.cols = engine.current_position.dimensions.width
        self.users_turn = True

        # create the canvas and core gui elements
        self.cell_size = cell_size
        self.canvas = tk.Canvas(self, height=self.rows * cell_size,
                                width=self.cols * cell_size)
        self.canvas.grid(row=0, column=0, columnspan=1)
        self.piece_images = {} # Stores the piece images due to tkinter garbage collection
        self.highlighted_squares = [] # Tracks the highlighted squares for valid moves
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
        for row in range(self.rows):
            for col in range(self.cols):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                fill = "antique white" if (row + col) % 2 == 0 else "saddle brown"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline="black")
    
    def load_piece_images(self):
        pieces = ['white-pawn', 'white-bishop', 'white-knight', 'white-rook', 'white-queen', 'white-king',
                  'black-pawn', 'black-bishop', 'black-knight', 'black-rook', 'black-queen', 'black-king',
                  'white-custom1', 'white-custom2', 'white-custom3', 'white-custom4', 'white-custom5', 'white-custom6',
                  'black-custom1', 'black-custom2', 'black-custom3', 'black-custom4', 'black-custom5', 'black-custom6']
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
        for piece in self.engine.get_pieces():
            owner, x, y, piece_type = piece
            piece_name = f'{owner}-{piece_type.lower()}'
            img = self.piece_images[piece_name]
            x1 = x * self.cell_size
            y1 = y * self.cell_size
            self.canvas.create_image(x1, y1, image=img, anchor="nw")
    
    ### Methods for handling the user inputs to the chess board
    
    def canvas_clicked(self, event):
        # get the row and column clicked and returns as a tuple
        if not self.users_turn:
            return
        col = event.x // self.cell_size
        row = event.y // self.cell_size

        if self.selected_piece:
            # If a piece is already selected, have the engine move the piece
            if (row, col) in self.valid_moves:
                self.engine.make_move(self.selected_piece[0], self.selected_piece[1], row, col)
                self.update_board()
                self.users_turn = False
            else:
                self.selected_piece = False
                self.valid_moves = []
                self.clear_highlights()
        
        #  otherwise select the piece, and have the engine highlight the legal moves
        if engine.current_position.get_piece_at(to_index(row, col)).owner == engine.current_position.to_move:
            self.selected_piece = (row, col)
            self.highlight_legal_moves(row, col)

        return
    
    def highlight_legal_moves(self, row, col):
        """Highlights legal moves for the selected piece."""
        self.clear_highlights()
        self.valid_moves = self.engine.moves_from(row, col)
        for move in self.valid_moves:
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

    def play_bot(self, row, col):
        """Loop that alternates between the player and the bot."""
        while True:
            if self.users_turn:
                self.selected_piece = False
                self.users_turn = False
            else:
                self.engine_move()
                self.users_turn = True
            
            if self.engine.current_position.is_game_over():
                messagebox.showinfo("Game Over", f"{self.engine.current_position.get_winner()} wins!")
                break

    def engine_move(self):
        """Makes the engine move and updates the board."""
        self.engine.play_best_move(4)
        self.update_board()
        
    # button functions
    def undo_move(self):
        self.engine.undo()
        self.update_board()


if __name__ == "__main__":
    # Example usage
    engine = Engine()
    app = EngineGameGUI(engine)
    app.mainloop()