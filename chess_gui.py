import tkinter as tk
from PIL import Image, ImageTk
import os
from chess import ChessGame

class GridApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Chess Piece Placement")

        self.pieces = {}  # Cache for loaded piece images
        self.selected_piece = None  # Currently selected piece

        # Entry for width and height with labels
        self.setup_inputs()

        self.grid_frame = tk.Frame(self)  # Frame to hold the grid
        self.piece_selection_frame = None  # Initialize frame for piece selection buttons

        # Load and display piece icons initially
        self.load_piece_icons()

        # Default grid generation placeholder
        self.grid_frame.grid(row=3, column=0, columnspan=12)
        
        # Initialize mouse event handling helpers
        self.dragging = False  # Track whether a drag is in progress
        self.dragged_piece = None  # The piece being dragged
        self.dragged_image = None  # The canvas image item being dragged


        self.generate_grid()

    def setup_inputs(self):
        self.entry_width = tk.Entry(self)
        self.entry_height = tk.Entry(self)
        self.label_width = tk.Label(self, text="Width:")
        self.label_height = tk.Label(self, text="Height:")
        self.generate_button = tk.Button(self, text="Generate Grid", command=self.generate_grid)

        self.label_width.grid(row=0, column=0, padx=10, pady=10)
        self.entry_width.grid(row=0, column=1, padx=10, pady=10)
        self.label_height.grid(row=1, column=0, padx=10, pady=10)
        self.entry_height.grid(row=1, column=1, padx=10, pady=10)
        self.generate_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def load_piece_icons(self):
        if self.piece_selection_frame:
            self.piece_selection_frame.destroy()  # Remove the old frame and its widgets
        self.piece_selection_frame = tk.Frame(self)  # Create a new frame for piece selection buttons
        self.piece_selection_frame.grid(row=4, column=0, columnspan=12, pady=(10, 0))  # Adjust columnspan as needed

        pieces = ["b_bishop", "w_bishop", "b_knight", "w_knight", "b_rook", "w_rook", "b_pawn", "w_pawn", "b_queen", "w_queen", "b_king", "w_king"]
        assets_folder = "assets"
        for i, piece_name in enumerate(pieces):
            path = os.path.join(assets_folder, f"{piece_name}.png")
            image = Image.open(path)
            image = image.resize((50, 50), Image.Resampling.LANCZOS)
            self.pieces[piece_name] = ImageTk.PhotoImage(image)

            button = tk.Button(self.piece_selection_frame, image=self.pieces[piece_name], bg='white', command=lambda name=piece_name: self.select_piece(name))
            button.grid(row=i % 2, column=i // 2, padx=5, pady=5)

    def select_piece(self, name):
        self.selected_piece = name

    def generate_grid(self):
        try:
            width = int(self.entry_width.get())
            height = int(self.entry_height.get())
            if width <= 0 or height <= 0:
                raise ValueError("Dimensions must be positive integers")
        except ValueError as e:
            print("Error:", e)
            return

        # Clear previous grid
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        self.squares = {}  # Store Canvas references to update them later

        # Generate new grid based on width and height
        for row in range(height):
            for col in range(width):
                canvas = tk.Canvas(self.grid_frame, width=60, height=60, borderwidth=1, highlightthickness=0)
                color = "light gray" if (row + col) % 2 == 0 else "black"
                canvas.create_rectangle(0, 0, 60, 60, fill=color, outline=color)
                canvas.grid(row=row, column=col, sticky="nsew")
                canvas.bind("<Button-1>", lambda event, r=row, c=col: self.place_piece(r, c))
                self.squares[(row, col)] = canvas

        # Reload piece icons to adjust their position based on the new grid
        self.load_piece_icons()

    def place_piece(self, row, col, piece_name = None):
        piece_name = piece_name or self.selected_piece
        if piece_name and (row, col) in self.squares:
            canvas = self.squares[(row, col)]
            canvas.delete("all")
            color = "light gray" if (row + col) % 2 == 0 else "black"
            canvas.create_rectangle(0, 0, 60, 60, fill=color, outline=color)
            canvas.create_image(30, 30, image=self.pieces[self.selected_piece])  # Place piece at center
            canvas.bind("<ButtonPress-1>", lambda event, p=piece_name, r=row, c=col: self.start_drag(event, p, r, c))
            canvas.bind("<B1-Motion>", self.do_drag)
            canvas.bind("<ButtonRelease-1>", self.end_drag)

    def start_drag(self, event, piece, row, col):
        if not self.dragging and piece:
            self.dragging = True
            self.dragged_piece = piece
            self.canvas.delete("dragged")  # Remove any existing dragged piece visuals
            self.dragged_image = self.canvas.create_image(event.x, event.y, image=self.pieces[piece], tags=("dragged",))
            self.current_row, self.current_col = row, col  # Store the initial position

    def do_drag(self, event):
        if self.dragging and self.dragged_image:
            # Update the dragged image position to follow the mouse cursor
            self.canvas.coords(self.dragged_image, event.x, event.y)

    def end_drag(self, event):
        if self.dragging:
            self.dragging = False
            target_row, target_col = self.calculate_target_square(event.x, event.y)
            if (target_row, target_col) in self.squares:
                # Move the piece in the backend model if needed, then visually
                self.place_piece(target_row, target_col, self.dragged_piece)
            self.canvas.delete("dragged")  # Remove the dragged piece visual
            self.dragged_piece = None
            self.dragged_image = None


if __name__ == "__main__":
    app = GridApp()
    app.mainloop()
