import tkinter as tk
from board import Board
import os
from PIL import Image, ImageTk

class BoardGUI:
    def __init__(self, root, board):
        # Set initial values and event listeners
        self.root = root
        self.root.title("Custom Chess GUI - Mason Liebe")
        self.board = board
        
        # Create the board canvas and event listeners
        self.board_canvas = tk.Canvas(self.root, width=400, height=400)
        self.board_canvas.pack(side = tk.LEFT)
        self.board_canvas.bind("<Button-1>", self.on_canvas_click)

        # Store for the image references to prevent garbage collection        
        self.image_refs = []

        # Draw the board
        self.draw_board()
        self.add_buttons()
        
    def draw_board(self):
        self.board_canvas.delete("all")  # Clear the canvas before redrawing
        self.image_refs = []  # Clear previous image references

        for row in range(8):
            for col in range(8):
                x1 = col * 50
                y1 = row * 50
                x2 = x1 + 50
                y2 = y1 + 50
                color = "white" if (row + col) % 2 == 0 else "black"
                self.board_canvas.create_rectangle(x1, y1, x2, y2, fill=color)
        
        for row in range(8):
            for col in range(8):
                piece = self.board.get_board()[row][col]
                if piece != 0:
                    self.draw_piece(piece, row, col)

        # Add more code to draw the rest of the board
    
    def draw_piece(self, piece_number, row, col):
        fileDict = {1: "w_pawn", 2: "b_pawn", 3: "w_knight", 4: "b_knight", 5: "w_bishop", 6: "b_bishop", 7: "w_rook", 8: "b_rook", 9: "w_queen", 10: "b_queen", 11: "w_king", 12: "b_king"}

        piece_name = fileDict[piece_number]
        path = f"assets/{piece_name}.png"
        # Open the image with PIL
        pil_image = Image.open(path)
        # Resize the image
        pil_image = pil_image.resize((40, 40), Image.Resampling.LANCZOS)
        # Convert the PIL image to a PhotoImage
        image = ImageTk.PhotoImage(pil_image)
        
        # Adjusting the position for the image to be centered in the square
        self.board_canvas.create_image(col * 50 + 26, row * 50 + 25, anchor="center", image=image)
        
        # Keep a reference to the image
        self.image_refs.append(image)
    
    def add_buttons(self):
        # Create a frame to hold the buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Reset button
        reset_button = tk.Button(button_frame, text="Reset Board", command=self.reset_board)
        reset_button.pack(pady=10)
        
        # Clear button
        clear_button = tk.Button(button_frame, text="Clear Board", command=self.clear_board)
        clear_button.pack(pady=10)
    
    def reset_board(self):
        # Set the board state to the initial configuration and redraw the board
        initial_state = [[8, 4, 6, 10, 12, 6, 4, 8],
                         [2, 2, 2,  2,  2, 2, 2, 2],
                         [0, 0, 0,  0,  0, 0, 0, 0],
                         [0, 0, 0,  0,  0, 0, 0, 0],
                         [0, 0, 0,  0,  0, 0, 0, 0],
                         [0, 0, 0,  0,  0, 0, 0, 0],
                         [1, 1, 1,  1,  1, 1, 1, 1],
                         [7, 3, 5,  9, 11, 5, 3, 7]]
        self.board.set_board(initial_state)
        self.draw_board()
    
    def clear_board(self):
        # Clear the board except for the kings
        clear_state = [[0]*8 for _ in range(8)]
        clear_state[0][4] = 12  # White King
        clear_state[7][4] = 6   # Black King
        self.board.set_board(clear_state)
        self.draw_board()

    def on_canvas_click(self, event):
        col = event.x // 50  # Calculate column from x coordinate
        row = event.y // 50  # Calculate row from y coordinate
        
        piece = self.board.get_board()[row][col]  # Get the piece at the click location
        if piece != 0:  # If there is a piece at the click location
            valid_moves = piece.get_valid_moves(self.board)  # Get valid moves for the piece
            
            self.highlight_moves(valid_moves)  # Highlight valid moves
    
    def highlight_moves(self, moves):
        for row, col in moves:  # Loop through each valid move
            x1 = col * 50
            y1 = row * 50
            x2 = x1 + 50
            y2 = y1 + 50
            self.board_canvas.create_rectangle(x1, y1, x2, y2, fill="green", outline="")
            # Redraw the piece on top if needed
            piece = self.board.get_board()[row][col]
            if piece != 0:
                self.draw_piece(piece, row, col)

            
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    board_state = [[8, 4, 6, 10, 12, 6, 4, 8],
                   [2, 2, 2,  2,  2, 2, 2, 2],
                   [0, 0, 0,  0,  0, 0, 0, 0],
                   [0, 0, 0,  0,  0, 0, 0, 0],
                   [0, 0, 0,  0,  0, 0, 0, 0],
                   [0, 0, 0,  0,  0, 0, 0, 0],
                   [1, 1, 1,  1,  1, 1, 1, 1],
                   [7, 3, 5,  9, 11, 5, 3, 7]]
    
    board = Board(8, 8, board_state)
    
    # Create the root window
    root = tk.Tk()
    board_gui = BoardGUI(root, board)
    board_gui.run()
