from flask import Flask, jsonify, request
import json
from datetime import datetime

app = Flask(__name__)

users = []


@app.route('/user/register', methods=['POST'])
def register_user():
    data = request.get_json()
    login = data.get('login')
    password = data.get('password')
    if not login or not password:
        return jsonify({'error': 'Login and password are required.'}), 400


    for user in users:
        if user['login'] == login:
            return jsonify({'error': 'User with this login already exists.'}), 400


    user = {
        'login': login,
        'password_hash': hash(password),
        'registration_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    users.append(user)

    return jsonify({'message': 'User registered successfully.'}), 201


@app.route('/user/', methods=['GET'])
def get_users():
    return jsonify(users), 200


if __name__ == '__main__':
    app.run(debug=True)

