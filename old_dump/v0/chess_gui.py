import tkinter as tk
from main import Board
from v1.pieces import Empty, Pawn, Knight, Bishop, Rook, Queen, King, Piece
import os
from PIL import Image, ImageTk

class BoardGUI:
    def __init__(self, root, board):
        # Set initial values and event listeners
        self.root = root
        self.root.title("Custom Chess GUI - Mason Liebe")
        self.board = board
        self.white = True # White is the player who moves first
        self.selected_piece = None  # Track the selected piece (row, col)
        self.valid_moves = []  # Track valid moves for the selected piece
        
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
        empty_state = [[0, 0, 0, 0, 12, 0, 0, 0],
                       [0, 0, 0, 0,  0, 0, 0, 0],
                       [0, 0, 0, 0,  0, 0, 0, 0],
                       [0, 0, 0, 0,  0, 0, 0, 0],
                       [0, 0, 0, 0,  0, 0, 0, 0],
                       [0, 0, 0, 0,  0, 0, 0, 0],
                       [0, 0, 0, 0,  0, 0, 0, 0],
                       [0, 0, 0, 0, 11, 0, 0, 0]]
        self.board.set_board(empty_state)
        self.draw_board()

    def on_canvas_click(self, event):
        col = event.x // 50
        row = event.y // 50

        selected_piece = self.board.board_pieces[row][col]
        if (row, col) in self.valid_moves:  # If a valid move square is clicked
            self.move_piece(selected_piece, row, col)
            self.selected_piece = None
            self.valid_moves = []
        elif not selected_piece.is_empty():  # Check if the selected square is not empty
            self.selected_piece = selected_piece
            self.valid_moves = selected_piece.get_valid_moves(self.board)
            self.draw_board()
            self.highlight_moves(self.valid_moves)

    def move_piece(self, piece, to_row, to_col):
        if self.selected_piece:
            from_row, from_col = self.selected_piece.row, self.selected_piece.col
            # Update board state and pieces array
            self.board.board_state[from_row][from_col] = 0  # Set the original square to empty
            self.board.board_pieces[from_row][from_col] = Empty(from_row, from_col, "yellow", self.board)
            self.board.board_state[to_row][to_col] = piece.piece_number
            self.board.board_pieces[to_row][to_col] = piece
            piece.move(to_row, to_col)  # Update piece's position

            self.draw_board()  # Redraw the board to reflect the move

    
    def highlight_moves(self, moves):
        for row, col in moves:  # Loop through each valid move
            x1 = col * 50
            y1 = row * 50
            x2 = x1 + 50
            y2 = y1 + 50
            self.board_canvas.create_rectangle(x1, y1, x2, y2, fill="", outline="green", width=3)
            # Redraw the piece on top if needed
            piece = self.board.get_board_pieces()[row][col]
            piece_number = self.board.get_board()[row][col]
            if piece_number != 0:
                self.draw_piece(piece_number, row, col)

            
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
