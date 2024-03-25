# gui for the window where custom games can be created
import tkinter as tk

class GameBuilderGUI(tk.Tk):
    
    CHAR_TO_FILENAME = {
        'p': 'black-pawn.png',
        'r': 'black-rook.png',
        'n': 'black-knight.png',
        'b': 'black-bishop.png',
        'q': 'black-queen.png',
        'k': 'black-king.png',
        'P': 'white-pawn.png',
        'R': 'white-rook.png',
        'N': 'white-knight.png',
        'B': 'white-bishop.png',
        'Q': 'white-queen.png',
        'K': 'white-king.png'
    }

    def __init__(self):
        super().__init__()
        self.title("Custom Chess Game Builder")
        # Adjust the initial geometry to ensure enough space
        self.geometry("1000x600")  # Adjusted to provide space for board visualization
        # Initialize board variables
        self.rows = 8
        self.cols = 8

        self.board_strings = ['rnbqkbnr', 'pppppppp', '········', '········', '········', '········', 'PPPPPPPP', 'RNBQKBNR']

        self.cell_size = 600 // max(self.rows, self.cols)

        # Initialize GUI components
        self.create_widgets()

    def create_widgets(self):
        # Control Panel for inputs
        control_panel = tk.Frame(self)
        control_panel.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        # Rows configuration with slider
        self.rows_label = tk.Label(control_panel, text="Rows:")
        self.rows_label.grid(row=0, column=0)
        self.rows_slider = tk.Scale(control_panel, from_=1, to=16, orient=tk.HORIZONTAL, command=self.update_rows)
        self.rows_slider.set(self.rows)  # Initialize slider position
        self.rows_slider.grid(row=0, column=1)

        # Columns configuration with slider
        self.cols_label = tk.Label(control_panel, text="Columns:")
        self.cols_label.grid(row=1, column=0)
        self.cols_slider = tk.Scale(control_panel, from_=1, to=16, orient=tk.HORIZONTAL, command=self.update_cols)
        self.cols_slider.set(self.cols)  # Initialize slider position
        self.cols_slider.grid(row=1, column=1)

        # Create game button
        self.create_game_button = tk.Button(control_panel, text="Create Game", command=self.create_game)
        self.create_game_button.grid(row=6, column=0, columnspan=2)

        # Canvas for board visualization
        self.board_canvas = tk.Canvas(self, width=self.cols * self.cell_size, height=self.rows * self.cell_size)
        self.board_canvas.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=5, pady=5)
        self.render_board()

    def update_rows(self, val):
        # TODO: update the board string representation to add or remove rows
        self.rows = int(val)
        self.cell_size = 600 // max(self.rows, self.cols)
        print("reset rows to", self.rows, "cell size to", self.cell_size, "pixels")
        self.render_board()

    def update_cols(self, val):
        # TODO: update the board string representation to add or remove columns
        self.cols = int(val)
        self.cell_size = 600 // max(self.rows, self.cols)
        self.render_board()

    def render_board(self):
        print('start rendering')
        if self.board_canvas is not None:
            new_width = self.cols * self.cell_size
            new_height = self.rows * self.cell_size

            # Adjust the canvas size to fit the new board dimensions
            self.board_canvas.config(width=new_width, height=new_height)
            print('rendering now')
            self.board_canvas.delete("all")  # Clear existing board
            for row in range(self.rows):
                for col in range(self.cols):
                    x1 = col * self.cell_size
                    y1 = row * self.cell_size
                    x2 = x1 + self.cell_size
                    y2 = y1 + self.cell_size
                    fill = "antique white" if (row + col) % 2 == 0 else "saddle brown"
                    self.board_canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline="black")

    def render_pieces(self):
        # Your logic to render the pieces on the board
        pass


    def create_game(self):
        # Your logic to handle game creation
        print("Game created with rows:", self.rows, "cols:", self.cols, "cell size:", self.cell_size)
        # self.destroy()  # Consider whether you want to close the builder window automatically



if __name__ == "__main__":
    # Example usage

    app = GameBuilderGUI()
    app.mainloop()