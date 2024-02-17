import tkinter as tk
from PIL import Image, ImageTk
import os

class GridApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Chess Piece Placement")

        self.pieces = {}  # Cache for loaded piece images
        self.selected_piece = None  # Currently selected piece

        # Entry for width and height with labels
        self.setup_inputs()

        # Load and display piece icons
        self.load_piece_icons()

        # Default grid generation
        self.generate_grid()

    def setup_inputs(self):
        self.entry_width = tk.Entry(self)
        self.entry_height = tk.Entry(self)
        self.label_width = tk.Label(self, text="Width:")
        self.label_height = tk.Label(self, text="Height:")
        self.generate_button = tk.Button(self, text="Generate Grid", command=self.generate_grid)

        self.label_width.grid(row=0, column=9, padx=10, pady=10)
        self.entry_width.grid(row=0, column=10, padx=10, pady=10)
        self.label_height.grid(row=1, column=9, padx=10, pady=10)
        self.entry_height.grid(row=1, column=10, padx=10, pady=10)
        self.generate_button.grid(row=2, column=9, columnspan=2, padx=10, pady=10)

    def load_piece_icons(self):
        pieces = sorted(["b_bishop", "w_bishop", "b_knight", "w_knight", "b_rook", "w_rook", "b_pawn", "w_pawn", "b_queen", "w_queen", "b_king", "w_king"], key=lambda x: (x[0], x[-6:]))
        assets_folder = "assets"
        for i, piece_name in enumerate(pieces):
            path = os.path.join(assets_folder, f"{piece_name}.png")
            image = Image.open(path)
            image = image.resize((50, 50))
            self.pieces[piece_name] = ImageTk.PhotoImage(image)

            row = (i % 6) + 3
            column = 9 if i < 6 else 10

            label = tk.Label(self, image=self.pieces[piece_name], bg='white')  # Assume the background is white
            label.grid(row=row, column=column, sticky="ew")
            label.bind("<Button-1>", lambda event, name=piece_name: self.select_piece(name))


    def select_piece(self, name):
        self.selected_piece = name

    def generate_grid(self):
        # Retrieve and validate width and height from entry boxes
        try:
            width = int(self.entry_width.get())
            height = int(self.entry_height.get())
            if width <= 0 or height <= 0:
                raise ValueError("Dimensions must be positive integers")
        except ValueError as e:
            print("Error:", e)
            return

        # Clear previous grid
        for widget in self.winfo_children():
            if isinstance(widget, tk.Canvas) and widget not in [self.entry_width, self.entry_height, self.label_width, self.label_height, self.generate_button]:
                widget.destroy()

        self.squares = {}  # Store Canvas references to update them later

        # Generate new grid based on width and height
        for row in range(height):
            for col in range(width):
                canvas = tk.Canvas(self, width=60, height=60, borderwidth=1, highlightthickness=0)
                color = "light gray" if (row + col) % 2 == 0 else "black"
                canvas.create_rectangle(0, 0, 60, 60, fill=color, outline=color)
                canvas.grid(row=row, column=col, sticky="nsew")
                canvas.bind("<Button-1>", lambda event, r=row, c=col: self.place_piece(r, c))
                self.squares[(row, col)] = canvas

    def place_piece(self, row, col):
        if self.selected_piece and (row, col) in self.squares:  # Check if a piece is selected and a valid cell is clicked
            canvas = self.squares[(row, col)]
            canvas.delete("all")  # Clear previous piece or rectangle
            color = "light gray" if (row + col) % 2 == 0 else "black"
            canvas.create_rectangle(0, 0, 60, 60, fill=color, outline=color)  # Redraw square color
            canvas.create_image(30, 30, image=self.pieces[self.selected_piece])  # Place piece at center


if __name__ == "__main__":
    app = GridApp()
    app.mainloop()
