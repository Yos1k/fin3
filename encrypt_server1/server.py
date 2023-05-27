import socket
from random import randint

HOST = '127.0.0.1'
PORT = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print('Сервер запущен. Ожидание подключения клиента...')
client_socket, address = server_socket.accept()
print(f'Установлено соединение с клиентом {address}')

prime = 23
base = 5
server_secret = randint(1, prime - 1)
server_public_key = pow(base, server_secret, prime)
client_socket.sendall(str(server_public_key).encode('utf-8'))

client_public_key = int(client_socket.recv(1024).decode('utf-8'))

shared_secret = pow(client_public_key, server_secret, prime)
print(f'Общий секретный ключ: {shared_secret}')


client_socket.close()
server_socket.close()
