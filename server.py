from datetime import datetime
from flask import Flask, request

import re
import time


app = Flask(__name__)
messages = [
    # {'username': 'John', 'time': time.time(), 'text': 'Hello, Mary!'},
    # {'username': 'Mary', 'time': time.time(), 'text': 'Hello, John!'}
]
passwords_storage = {
    # 'John': '1234',
    # 'Mary': '4321'
}


def validate_password(password):
    """
    password - str
    :return: bool
    """
    if len(password) < 4 or \
            len(password) > 16 or \
            re.search('[0-9]', password) is None or \
            re.search('[A-Z]', password) is None:
        return False
    return True


@app.route('/')
def hello_method():
    return 'Hello, World!'


@app.route('/status')
def status_method():
    return {
        'status': True,
        'time': datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
        'users_count': len(passwords_storage),  # number of registered users
        'messages_count': len(messages)  # total number of messages
    }


@app.route('/send', methods=['POST'])
def send_method():
    """
    JSON {'username': str, 'password': str, 'text': str}
    username, text - not empty strs
    :return: {'ok': bool}
    """
    username = request.json['username']
    password = request.json['password']
    text = request.json['text']

    # first attempt for password is always valid
    # if username not in passwords_storage and validate_password(password):
    if username not in passwords_storage:
        passwords_storage[username] = password

    # validate data
    if not isinstance(username, str) or len(username) == 0:
        return {'ok': False}
    if not isinstance(text, str) or len(text) == 0:
        return {'ok': False}
    if passwords_storage[username] != password:
        return {'ok': False}

    messages.append(
        {'username': username, 'time': time.time(), 'text': text})

    return {'ok': True}


@app.route('/messages')
def messages_method():
    """
    Param after - time of the last message
    :return: {'messages': [
        {'username': str, 'time': float, 'text': str},
        ...
    ]}
    """
    after = float(request.args['after'])
    filtered_messages = [
        message for message in messages if message['time'] > after]

    return {'messages': filtered_messages}


if __name__ == '__main__':
    app.run()
