import socket
from random import randint

HOST = '127.0.0.1'
PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
print('Соединение с сервером установлено.')

server_public_key = int(client_socket.recv(1024).decode('utf-8'))
print(f'Получен публичный ключ сервера: {server_public_key}')

prime = 23
base = 5
client_secret = randint(1, prime - 1)
client_public_key = pow(base, client_secret, prime)
client_socket.sendall(str(client_public_key).encode('utf-8'))

shared_secret = pow(server_public_key, client_secret, prime)
print(f'Общий секретный ключ: {shared_secret}')

client_socket.close()
