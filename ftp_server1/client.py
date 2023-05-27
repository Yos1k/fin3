import socket

sock = socket.socket()
sock.connect(('localhost', 6666))

while True:

    command = input('Введите команду для сервера: ')
    sock.send(command.encode())


    response = sock.recv(1024).decode()
    print('Server:', response)

    if command == 'quit':
        break

sock.close()
