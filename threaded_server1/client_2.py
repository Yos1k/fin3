import socket
import threading


def reader():
    right = 1
    while right:
        msg = sock.recv(1024).decode()
        if msg != 'exit':
            print(msg)
        else:
            break


sock = socket.socket()
isnal = 0
try:
    sock.connect(('localhost', int(input('Введите порт: '))))
    isnal = 1
except:
    isnal = 0

if isnal == 1:
    nal = sock.recv(1024).decode()
    if isnal == 0:
        nal = 'nothing'
    if nal == 'YES':
        print('Вы зарегистрированы')
    else:
        print('Вы не зарегистрированы')
    right = 1
    if nal == 'YES':
        password = input('Введите пароль: ')
        sock.send(password.encode())
        if (sock.recv(1024).decode()) == 'Верный пароль':
            print('Верный пароль')
        else:
            print('Не верный пароль')
            right = 0
    else:
        login = input('Введите логин: ')
        sock.send(login.encode())
        password = input('Введите пароль: ')
        sock.send(password.encode())

    s1 = threading.Thread(target=reader)
    s1.daemon = True
    s1.start()
    if right:
        print('Введите сообщение:')
    while right:
        msg = input()
        if msg != 'exit':
            sock.send(msg.encode())
        else:
            sock.send(msg.encode())
            right = 0
else:
    input('Неверный порт')
sock.close()