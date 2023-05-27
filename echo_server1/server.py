import socket
import time
import logging
import json
from port import ask_port


def log_print(st):
    logging.info(st)
    print(st)


def open_file(file_name):
    try:
        with open(file_name, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        with open(file_name, 'w') as f:
            json.dump({}, f)
        with open(file_name, 'r') as f:
            data = json.load(f)
    return data


def record_file(file_name, data):
    try:
        with open(file_name, 'r') as f:
            data_old = json.load(f)
        data_old.update(data)
        with open(file_name, 'w') as f:
            json.dump(data_old, f)
    except FileNotFoundError:
        with open(file_name, 'w') as f:
            json.dump(data, f)


def open_text_file(file_name):
    with open(file_name, 'r') as file:
        return file.readlines()


def record_text_file(file_name, line):
    with open(file_name, 'a') as file:
        file.write(line + ' ;\n')


logging.basicConfig(filename='server.log', encoding='utf-8', level=logging.INFO)

log_print('Сервер запущен')
port = ask_port()

server = socket.socket()
server.bind(('127.0.0.1', port))
log_print(f'Прослушивание порта {port}')

try:
    while True:
        server.listen(1)

        client_socket, address = server.accept()
        right = 1
        try:
            data = open_text_file('book.txt')
        except FileNotFoundError:
            record_text_file('book.txt', '')
            data = open_text_file('book.txt')

        nal = 'NO'
        for i in data:
            if i != ' ;\n':
                if i.split(', ')[2] == address[0]:
                    nal = 'YES'
                    login = i.split(', ')[0]

        client_socket.send(str(nal).encode())
        if nal == 'YES':
            stata = open_file('stata.json')
            if stata[login] == client_socket.recv(1024).decode():
                client_socket.send('Пароль верен'.encode())
                log_print(f'{address[0]}, {address[1]} подсоединился')
                record_text_file('book.txt', f'{login}, {port}, {address[0]}, {address[1]}')
            else:
                client_socket.send('Пароль не верен'.encode())
                print('Неудачная попытка подключения')
                log_print(f'{login} пытался подключиться')
                right = 0
        else:
            login = client_socket.recv(1024).decode()
            password = client_socket.recv(1024).decode()
            record_file('stata.json', {login: password})
            record_text_file('book.txt', f'{login}, {port}, {address[0]}, {address[1]}')
            log_print(f'{address[0]}, {address[1]} подсоединился')

        while right:
            client_socket.send('Вы подключены!'.encode())
            try:
                data = client_socket.recv(2048).decode()
            except OSError:
                data = None

            time.sleep(3)
            if data:
                # получение данных от клиента
                log_print(f'\nПолучаем данные от клиента: {data}')

                if data.lower() == 'exit':
                    log_print('Клиент отключился')
                    break
            msg = input('\nВвод текста для клиента:\n').encode()

            client_socket.send(msg)
            if msg == 'exit'.encode():
                time.sleep(2)

                log_print('exit команда получена')
                server.shutdown(socket.SHUT_WR)
                server = socket.socket()
                server.bind(('127.0.0.1', port))
                break

except KeyboardInterrupt:
    log_print('Сервер отключен')
    server.shutdown(socket.SHUT_WR)
