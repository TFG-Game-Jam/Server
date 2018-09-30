import random
import time

from flask import Flask, jsonify, request
from flask_cors import CORS

from server import datastore

app = Flask(__name__)
CORS(app)

state = {
    'lastUpdate': time.time(),
    'lastAction': time.time(),
    'energy': 100,
    'shotsFired': 0,
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
    'aimAngle': 0.,
    'roomState': [0, 0, 0],
}
projectile_colors = ['loadPurple', 'loadGreen', 'loadCyan', 'loadWhite']
shuffled_rooms = [None, None, None]


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
def get_state():
    update_energy()
    return jsonify(state)


@app.route('/set-state', methods=['POST', 'GET'])
def set_state():
    shots_taken = int(request.args.get('shotsTaken', request.form.get('shotsTaken', state['shotsTaken'])))
    old_shots_taken = int(state['shotsTaken'])
    if shots_taken != old_shots_taken:
        if shots_taken < old_shots_taken:  # New game session
            state['shotsTaken'] = 0
        for _ in range(shots_taken - int(state['shotsTaken'])):
            rooms = [0, 1, 2]
            random.shuffle(rooms)
            for room in rooms:
                if actions['roomState'][room] < 2:
                    actions['roomState'][room] += 1
                    break
        state['shotsTaken'] = shots_taken
    for key in state:
        value = request.args.get(key, request.form.get(key))
        if value:
            state[key] = value
    return jsonify('')


@app.route('/set-actions')
def set_actions():
    if actions['roomState'][0] == 1:
        if shuffled_rooms[0] is None:
            shuffled_rooms[0] = random.choice([False, True])
    else:
        shuffled_rooms[0] = None
    if actions['roomState'][1] == 1:
        if shuffled_rooms[1] is None:
            shuffled_rooms[1] = projectile_colors[:]
            random.shuffle(shuffled_rooms[1])
    else:
        shuffled_rooms[1] = None
    if actions['roomState'][2] == 1:
        if shuffled_rooms[2] is None:
            shuffled_rooms[2] = random.random() * 360
    else:
        shuffled_rooms[2] = None

    for key in actions:
        value = request.args.get(key)
        if value:
            if shuffled_rooms[0] and (key == 'port' or key == 'starboard'):
                key = 'starboard' if key == 'port' else 'port'
            if shuffled_rooms[1] and key.startswith('load'):
                key = shuffled_rooms[1][projectile_colors.index(key)]
            if key == 'aimAngle':
                if not state['energy'] or actions['roomState'][2] == 2:
                    continue
                if shuffled_rooms[2]:
                    value += shuffled_rooms[2]
            actions[key] = value
    return jsonify('')


@app.route('/get-actions')
def get_actions():
    update_energy()
    update_rooms()
    for key in ('port', 'starboard', 'loadPurple', 'loadGreen', 'loadCyan', 'loadWhite'):
        if state['energy'] == 0:
            actions[key] = False
        else:
            actions[key] = str(actions[key]).lower().startswith('true')
    if actions['roomState'][0] == 2:  # Motors
        actions['port'] = actions['starboard'] = False
    if actions['roomState'][1] == 2:  # Weapon arming
        actions['loadPurple'] = actions['loadGreen'] = actions['loadCyan'] = actions['loadWhite'] = False
    return jsonify(actions)


def update_energy():
    delta = time.time() - state['lastUpdate']
    state['lastUpdate'] = time.time()
    print('Energy: {}'.format(state['energy']))
    if str(actions['fixGenerator']).lower().startswith('true'):
        state['energy'] += 8 * delta
    else:
        state['energy'] -= delta
    state['energy'] = min(max(state['energy'], 0), 100)


def update_rooms():
    t = time.time()
    if t - state['lastAction'] > 5:
        state['lastAction'] = t
        rooms = [0, 1, 2]
        random.shuffle(rooms)
        for room in rooms:
            if actions['roomState'][room]:
                actions['roomState'][room] = 0
                break

if __name__ == '__main__':
    app.run(host='0.0.0.0')
