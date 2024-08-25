from flask import Flask, request, jsonify
import redis

app = Flask(__name__)

# Connect to Redis server
redis_client = redis.StrictRedis(host='redis', port=6379, decode_responses=True)

@app.route('/')
def home():
    return "Welcome to the Redis API Service!"

@app.route('/get', methods=['GET'])
def get_value():
    value = redis_client.get('counter')
    return jsonify({'counter': value})

@app.route('/api/set', methods=['POST'])
def set_value():
    data = request.get_json()
    key = data.get('key')
    value = data.get('value')
    redis_client.set(key, value)
    return jsonify({"message": "Value set successfully", "key": key, "value": value})

@app.route('/post', methods=['POST'])
def increment_value():
    incremented_value = redis_client.incr('counter')
    return jsonify({"message": "Value incremented successfully", "key": 'counter', "value": incremented_value})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)