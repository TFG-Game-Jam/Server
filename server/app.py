from flask import jsonify, Flask

app = Flask(__name__)


@app.route('/')
def root_page():
    return jsonify({'ok': True})
