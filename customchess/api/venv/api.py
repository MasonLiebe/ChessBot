from flask import Flask
from .engine import Engine

app = Flask(__name__)

@app.route('/api/start_game/<string:board><int rows><int cols>')
def start_game(board, rows, cols):
    engine = Engine(board, rows, cols)
    return engine.start_game()

