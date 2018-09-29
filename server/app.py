from flask import Flask, jsonify, request
from flask_cors import CORS

from server import datastore

app = Flask(__name__)
CORS(app)

state = {
    'oxygen': 100,
}
queued_actions = []

@app.route('/create-game')
def create_game():
    username = request.args.get('username', 'captain')
    datastore.set('captain', username)
    return ''


@app.route('/get-games')
def get_games():
    return jsonify([])


@app.route('/get-state')
def get_oxigen_level():
    return jsonify(state)


@app.route('/set-state')
def login():
    for key in state:
        value = request.args.get(key)
        if value:
            state[key] = value
    return ''


@app.route('/act')
def act():
    action = request.args['action']
    queued_actions.append(action)
    return ''


@app.route('/get-actions')
def get_actions():
    actions = []
    while queued_actions:
        actions.append(queued_actions.pop())
    return jsonify(actions)
