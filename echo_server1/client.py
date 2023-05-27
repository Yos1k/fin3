# import
import socket
import time
from port import ask_port


port = ask_port()

client = socket.socket()
name = input('Введите имя хоста (по-умолчанию localhost)\n')
try:
    client.connect((name, port))
except (ConnectionRefusedError, socket.gaierror):
    print('Подключение с этого IP или порта недоступно сейчас.\nПрименить настройки по-умолчанию? Y\\N')
    if input() == 'Y':
        print('Соединение с сервером')
        client.connect(('127.0.0.1', port))
    else:
        print('OK. Попробуйте снова...')
        exit()


nal = client.recv(1024).decode()
if nal == 'YES':
    password = input('Введите пароль: ')
    client.send(password.encode())
    if (client.recv(1024).decode()) == 'Пароль верен':
        print('Пароль верен')
    else:
        print('Пароль не верен')
        right = 0
        exit()

else:
    login = input('Введите логин: ')
    client.send(login.encode())
    password = input('Введите пароль: ')
    client.send(password.encode())

print(client.recv(2048).decode())
while True:
    try:
        # Отправка данных серверу;
        cl_msg = input('Введите текст для сервера:\n').encode()
        client.send(cl_msg)
        if cl_msg.lower() == b'exit':
            break
        data = client.recv(2048).decode()
        time.sleep(3)

        # Разрыв соединения с сервером;
        if data.lower() == 'exit':
            break
        # Прием данных от сервера.
        if data:
            print(f'\nТекст с сервера: {data} \n')

    except KeyboardInterrupt:
        client.shutdown(socket.SHUT_WR)
    except:
        continue

print('exit команда получена\nПока!')
client.send('Клиент отсоединился\n'.encode())
print('Разрыв соединения с сервером')
client.shutdown(socket.SHUT_WR)
exit()