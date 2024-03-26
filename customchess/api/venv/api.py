from flask import Flask

app = Flask(__name__)

@app.route('/api/route')
def hello():
    return {'message': 'Hello, World!', 'sender': 'api.py'}