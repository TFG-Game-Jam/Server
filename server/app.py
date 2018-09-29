from flask import Flask, jsonify, request
from flask_cors import CORS

from server import datastore

app = Flask(__name__)
CORS(app)

state = {
    'energy': 100,
    'shotsTaken': 0,
    'players': [],
}
actions = {
    'port': False,
    'starboard': False,
    'loadPurple': False,
    'loadGreen': False,
    'loadCyan': False,
    'loadWhite': False,
    'fixGenerator': False,
}

@app.route('/create-game')
def create_game():
    username = request.args.get('username', 'captain')
    datastore.set('captain', username)
    return ''


@app.route('/get-games')
def get_games():
    return jsonify([])


@app.route('/join-game')
def join_game():
    state['players'].append(request.args.get('username', ''))
    return jsonify('')


@app.route('/get-players')
def get_player_count():
    return jsonify(state['players'])


@app.route('/get-state')
def get_oxigen_level():
    return jsonify(state)


@app.route('/set-state', methods=['POST'])
def set_state():
    for key in state:
        value = request.args.get(key, request.form.get(key))
        if value:
            state[key] = value
    return jsonify('')


@app.route('/set-actions')
def set_actions():
    for key in actions:
        value = request.args.get(key)
        if value:
            actions[key] = value
    print(actions)
    return jsonify('')


@app.route('/get-actions')
def get_actions():
    return jsonify(actions)
