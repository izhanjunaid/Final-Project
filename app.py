from flask import Flask, request, jsonify
import redis
import json
import uuid
import random
import os
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

try:
    redis_host = os.getenv('REDIS_HOST', 'localhost')
    redis_client = redis.Redis(host=redis_host, port=6379, db=0)
    redis_client.ping()  # Test the connection
    app.logger.info(f"Successfully connected to Redis at {redis_host}")
except redis.ConnectionError as e:
    app.logger.error(f"Failed to connect to Redis: {e}")

GRID_SIZE = 20

def generate_food():
    return {
        'x': random.randint(0, GRID_SIZE - 1),
        'y': random.randint(0, GRID_SIZE - 1)
    }

@app.route('/game', methods=['POST'])
def create_game():
    try:
        game_id = str(uuid.uuid4())
        initial_state = {
            'snake': [{'x': GRID_SIZE // 2, 'y': GRID_SIZE // 2}],
            'direction': 'RIGHT',
            'food': generate_food(),
            'score': 0
        }
        redis_client.set(f'game:{game_id}', json.dumps(initial_state))
        return jsonify({'game_id': game_id, 'state': initial_state})
    except Exception as e:
        app.logger.error(f"Error creating game: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/game/<game_id>', methods=['GET'])
def get_game_state(game_id):
    try:
        state = redis_client.get(f'game:{game_id}')
        if state:
            return jsonify(json.loads(state))
        return jsonify({'error': 'Game not found'}), 404
    except Exception as e:
        app.logger.error(f"Error getting game state: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/game/<game_id>', methods=['PUT'])
def update_game_state(game_id):
    try:
        state = redis_client.get(f'game:{game_id}')
        if not state:
            return jsonify({'error': 'Game not found'}), 404
        
        state = json.loads(state)
        new_direction = request.json.get('direction')
        if new_direction in ['UP', 'DOWN', 'LEFT', 'RIGHT']:
            state['direction'] = new_direction
        
        # Move snake
        head = state['snake'][0].copy()
        if state['direction'] == 'UP':
            head['y'] = (head['y'] - 1) % GRID_SIZE
        elif state['direction'] == 'DOWN':
            head['y'] = (head['y'] + 1) % GRID_SIZE
        elif state['direction'] == 'LEFT':
            head['x'] = (head['x'] - 1) % GRID_SIZE
        elif state['direction'] == 'RIGHT':
            head['x'] = (head['x'] + 1) % GRID_SIZE
        
        # Check if food is eaten
        if head == state['food']:
            state['score'] += 1
            state['food'] = generate_food()
        else:
            state['snake'].pop()
        
        state['snake'].insert(0, head)
        
        # Check for game over (snake collides with itself)
        if head in state['snake'][1:]:
            redis_client.delete(f'game:{game_id}')
            return jsonify({'game_over': True, 'score': state['score']})
        
        redis_client.set(f'game:{game_id}', json.dumps(state))
        return jsonify(state)
    except Exception as e:
        app.logger.error(f"Error updating game state: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/game/<game_id>', methods=['DELETE'])
def end_game(game_id):
    try:
        if redis_client.delete(f'game:{game_id}'):
            return '', 204
        return jsonify({'error': 'Game not found'}), 404
    except Exception as e:
        app.logger.error(f"Error ending game: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/highscores', methods=['POST'])
def add_high_score():
    try:
        score_data = request.json
        score = score_data.get('score')
        name = score_data.get('name')
        if score is None or name is None:
            return jsonify({'error': 'Invalid score data'}), 400
        redis_client.zadd('highscores', {name: score})
        return jsonify({'message': 'High score added successfully'})
    except Exception as e:
        app.logger.error(f"Error adding high score: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/highscores', methods=['GET'])
def get_high_scores():
    try:
        scores = redis_client.zrevrange('highscores', 0, 9, withscores=True)
        return jsonify([{'name': name.decode(), 'score': score} for name, score in scores])
    except Exception as e:
        app.logger.error(f"Error getting high scores: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=False)
