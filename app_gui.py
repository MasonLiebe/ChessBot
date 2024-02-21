from os import name
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from game import Game


class ChessGui:
    def __init__(self, game):
        self.game = game
        self.root = tk.Tk()
        self.root.title("Chess Game by Mason Liebe")
        
        # FOR TESTING PURPOSES
        self.computer_opponent = True

        # Create chessboard canvas
        self.canvas = tk.Canvas(self.root, width=800, height=800)
        self.canvas.grid(row=0, column=0, columnspan=2)
        self.piece_images = {} # Stores the piece images due to tkinter garbage collection
        self.highlighted_squares = [] # Tracks the highlighted squares for valid moves
        self.selected_piece_position = None  # Tracks the selected piece's position
        self.load_piece_images()
        self.create_board()
        self.update_board()
        self.canvas.bind("<Button-1>", self.canvas_clicked)

        # Button for resetting the game
        self.reset_button = tk.Button(self.root, text="Reset Game", command=self.reset_game)
        self.reset_button.grid(row=0, column=2, rowspan= 10, columnspan=2)  # Adjusted for layout

        # Button for getting computer move
        self.computer_move_button = tk.Button(self.root, text="Computer Move", command=self.get_computer_move)
        self.computer_move_button.grid(row=1, column=2, columnspan=10)  # Adjusted for layout

        # Turn indicator label
        self.turn_indicator = tk.Label(self.root, text="White to move", font=("Arial", 16))
        self.turn_indicator.grid(row=3, column=2, sticky="nw", padx=20)


    def load_piece_images(self):
        pieces = ['white-pawn', 'white-bishop', 'white-knight', 'white-rook', 'white-queen', 'white-king',
                'black-pawn', 'black-bishop', 'black-knight', 'black-rook', 'black-queen', 'black-king']
        for piece in pieces:
            path = f'./assets/pieces/{piece}.png'
            img = Image.open(path)
            # Resize the image to 75x75 pixels using the LANCZOS filter
            img = img.resize((100, 100), Image.LANCZOS)
            if img.mode != 'RGBA':
                img = img.convert('RGBA')

            self.piece_images[piece] = ImageTk.PhotoImage(img)


    def create_board(self):
        for row in range(8):
            for col in range(8):
                color = "antique white" if (row + col) % 2 == 0 else "saddle brown"
                x1 = col * 100
                y1 = row * 100
                x2 = x1 + 100
                y2 = y1 + 100
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
    
    def update_board(self):
        """Places the piece images on the board according to the game state."""
        self.canvas.delete("all")  # Clear the canvas
        self.create_board()  # Redraw the board itself (the checkered pattern)

        for row in range(8):
            for col in range(8):
                piece = self.game.board[row][col]
                if not piece.is_empty():
                    piece_image = self.piece_images.get(f"{piece.color}-{piece.__class__.__name__.lower()}")
                    if piece_image:
                        x = col * 100 + 50  # Center of the square
                        y = row * 100 + 50
                        # Adjust for the 75x75 image size to ensure proper centering
                        self.canvas.create_image(x, y, image=piece_image, anchor="center")


    def canvas_clicked(self, event):
        col = event.x // 100
        row = event.y // 100
        if self.selected_piece_position:
            # If a piece is already selected and the new click is on a different square,
            # attempt to move or clear highlights if not moving.
            if self.selected_piece_position != (row, col):
                self.move_piece(self.selected_piece_position, (row, col))
            self.clear_highlights()  # Clear highlights whether moving or not
            self.selected_piece_position = None
        else:
            self.clear_highlights()  # Clear existing highlights before selecting a new piece
            self.selected_piece_position = (row, col)
            self.highlight_legal_moves(row, col)

    def highlight_legal_moves(self, row, col):
        """Highlights legal moves for the selected piece."""
        piece = self.game.board[row][col]
        if piece and piece.color == self.game.current_player:
            legal_moves = piece.possible_moves(self.game)
            for move in legal_moves:
                self.highlight_square(move[0], move[1])

    def highlight_square(self, row, col):
        """Highlight a square to indicate it's a legal move."""
        x1 = col * 100
        y1 = row * 100
        x2 = x1 + 100
        y2 = y1 + 100
        # Create a rectangle with a specific color or outline to indicate highlight
        square = self.canvas.create_rectangle(x1, y1, x2, y2, outline="blue", width=5, tags="highlight")
        self.highlighted_squares.append(square)

    def clear_highlights(self):
        """Clears all highlighted squares."""
        for square in self.highlighted_squares:
            self.canvas.delete(square)
        self.highlighted_squares.clear()  # Reset the list of highlighted squares

    
    def move_piece(self, start_pos, end_pos):
        if self.game.move_piece(start_pos, end_pos):
            # Move was successful
            print(f"Moved piece from {start_pos} to {end_pos}")
            self.selected_piece_position = None  # Deselect the piece
            self.game.current_player = 'black' if self.game.current_player == 'white' else 'white'
            self.update_board()
            # Check the game status after the move
            status = self.game.check_status()
            print(status)
            if status not in ["Normal", "Check!"]:
                messagebox.showinfo("Game Over", status)
            
            self.update_turn_indicator()
        else:
            # Move was illegal or failed, deselect the piece
            self.selected_piece_position = None
            print("Illegal move or selection, try again.")
    
    def reset_game(self):
        """Resets the game to its starting state and updates the GUI."""
        print("Resetting the game...")
        self.game.reset_game()  # Reset the game state
        self.selected_piece_position = None  # Clear any selected piece
        self.update_board()  # Redraw the board with pieces in starting positions

    def update_turn_indicator(self):
        """Updates the turn indicator text based on the current player."""
        text = "White to move" if self.game.current_player == "white" else "Black to move"
        self.turn_indicator.config(text=text)

    def show_start_menu(self):
        self.start_menu = tk.Toplevel(self.root)
        self.start_menu.title("Chess Game - Start Menu")
        self.start_menu.geometry("300x200")  # Adjust size as needed

        tk.Label(self.start_menu, text="Choose Game Mode:", font=("Arial", 14)).pack(pady=20)

        tk.Button(self.start_menu, text="Play Against Computer", command=self.start_computer_game).pack(fill="x", padx=50, pady=10)
        tk.Button(self.start_menu, text="1v1 Human Players", command=self.start_human_game).pack(fill="x", padx=50, pady=10)

    def get_computer_move(self):
        if self.game.current_player == "black":
            print("executing_minimax")
            eval, move = self.game.minimax(3, float('-inf'), float('inf'), True)
            print(eval)
            if move:
                self.move_piece(move[0], move[1])
            else:
                messagebox.showinfo("Game Over", "Checkmate! You win!")
                self.reset_game()

    def start_computer_game(self):
        self.start_menu.destroy()  # Close the start menu
        self.setup_game()

    def start_human_game(self):
        self.start_menu.destroy()  # Close the start menu
        self.setup_game()

    def setup_game(self, computer_opponent=False):
        # Set up the game for playing against a computer or another human
        self.game.reset_game() # Reset the game state to the initial state
        self.computer_opponent = computer_opponent
        self.update_board()  # Draw or redraw the board

    def run(self):
        self.show_start_menu()
        self.root.mainloop()
        if name == "main":
            game = Game() # Initialize your game class here
            gui = ChessGui(game)
            gui.run()


# Run the game
if __name__ == "__main__":
    game = Game()
    gui = ChessGui(game)
    gui.run()