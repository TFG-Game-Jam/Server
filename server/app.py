from flask import jsonify, Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/')
def root_page():
    return jsonify({'ok': True})
