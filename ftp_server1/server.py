import socket
import os
import shutil
import logging


logging.basicConfig(
    filename='logs.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


users = {
    'user1': 'password1',
    'user2': 'password2',
}

def process(req, is_authenticated):
    words = req.split(' ')
    wordsLen = len(words)

    if not is_authenticated:
        if words[0] == 'login':
            if wordsLen == 3:
                username = words[1]
                password = words[2]
                if authenticate_user(username, password):
                    logging.info('User "%s" logged in', username)
                    return 'Login successful. Welcome, {}!'.format(username)
                else:
                    logging.warning('Login failed for user "%s"', username)
                    return 'Invalid username or password'
            else:
                return 'Invalid number of arguments'
        elif words[0] == 'register':
            if wordsLen == 3:
                username = words[1]
                password = words[2]
                if register_user(username, password):
                    logging.info('New user "%s" registered', username)
                    return 'Registration successful. Welcome, {}!'.format(username)
                else:
                    logging.warning('Registration failed for user "%s"', username)
                    return 'Username already exists'
            else:
                return 'Invalid number of arguments'
        else:
            return 'Please login or register to access the FTP server'

    # Обработка команд после авторизации
    if words[0] == 'touch':
        if wordsLen == 2:
            return create_file(rootDirectory, words[1])
        else:
            return 'Invalid number of arguments'
    elif words[0] == 'writefile':
        if wordsLen > 2:
            return write_file(rootDirectory, words[1], words[2:])
        else:
            return 'Invalid number of arguments'
    elif words[0] == 'readfile':
        if wordsLen == 2:
            return read_file(rootDirectory, words[1])
        else:
            return 'Invalid number of arguments'
    elif words[0] == 'delfile':
        if wordsLen == 2:
            return delete_file(rootDirectory, words[1])
        else:
            return 'Invalid number of arguments'
    elif words[0] == 'quit':
        return 'Goodbye!'
    return 'Invalid command'


def create_file(path, name):
    filename = os.path.join(path, name)
    if not os.path.exists(filename):
        open(filename, 'a').close()
        return 'Successfully created file'
    else:
        return 'File already exists'


def write_file(path, name, words):
    filename = os.path.join(path, name)
    with open(filename, 'a') as file:
        text = ' '.join(words)
        file.write(text)
    return 'Successfully added text'


def read_file(path, name):
    filename = os.path.join(path, name)
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            text = file.read()
        return text
    else:
        return 'File does not exist'


def delete_file(path, name):
    filename = os.path.join(path, name)
    if os.path.exists(filename):
        os.remove(filename)
        return 'Successfully deleted file'
    else:
        return 'File does not exist'


def authenticate_user(username, password):
    if username in users and users[username] == password:
        return True
    return False


def register_user(username, password):
    if username in users:
        return False

    users[username] = password
    user_directory = os.path.join(rootDirectory, username)
    os.mkdir(user_directory)
    return True


rootDirectory = os.path.dirname(os.path.abspath(__file__))
dirName = 'root'
rootDirectory = os.path.join(rootDirectory, dirName)
if not os.path.exists(rootDirectory):
    os.mkdir(rootDirectory)

sock = socket.socket()
sock.bind(('', 6666))
sock.listen(1)

is_authenticated = False  # Флаг авторизации

while True:
    conn, addr = sock.accept()
    request = conn.recv(1024).decode()
    logging.info('Client: %s', request)
    response = process(request, is_authenticated)

    # is_authenticated в True при успешной авторизации
    if not is_authenticated and (response.startswith('Login successful') or response.startswith('Registration successful')):
        is_authenticated = True

    conn.send(response.encode())
    if request == 'quit':
        break

conn.close()
