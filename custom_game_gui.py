# tkinter gui that handles the playing of a custom game

from os import name
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from custom_game import CustomGame
from custom_pieces import *


class CustomChessGUI(tk.Tk):
    def __init__(self, game, cell_size=60):
        super().__init__()
        self.game = game
        self.cell_size = cell_size

        self.canvas = tk.Canvas(self, height=self.game.rows * cell_size,
                                width=self.game.cols * cell_size)
        self.canvas.grid(row=0, column=0, columnspan=1)
        self.piece_images = {} # Stores the piece images due to tkinter garbage collection
        self.highlighted_squares = [] # Tracks the highlighted squares for valid moves

        self.load_piece_images()
        self.draw_board()
        self.update_board()

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




## Example usage

test_game1 = CustomGame(8, 8, starting_board = ['rnbqkbnr',
                                                'pppppppp', 
                                                '········', 
                                                '········', 
                                                '········', 
                                                '········', 
                                                'PPPPPPPP',
                                                'RNBQKBNR'])

if __name__ == "__main__":
    # Example usage
    custom_game = CustomGame(8, 10, starting_board = ['rnbqkbnrrr',
                                                'pppppppprr', 
                                                '········rr', 
                                                '········rr', 
                                                '········rr', 
                                                '········rr', 
                                                'PPPPPPPPrr',
                                                'RNBQKBNRrr'])
    app = CustomChessGUI(custom_game)
    app.mainloop()