import socket
import threading
import random
import json
import datetime
import logging


def log_print(st):
    logging.info(st)
    print(st)


def session():
    with open('server.log') as f:
        f = f.readlines()

    last = 0

    for i in reversed(range(len(f[:-1]))):
        if f[i] == 'INFO:root:Порт пуст\n':
            last = i
            break
    k = 0
    for i in range(last + 1, len(f) - 1):
        if 'Пользователь присоединился' in f[i]:
            k += 1
    return 'количество участников за последнюю сессию: ' + str(k)


def open_f(file_name):
    try:
        with open(file_name, 'r') as f:
            data = json.load(f)
    except:
        with open(file_name, 'w') as f:
            json.dump({}, f)
        with open(file_name, 'r') as f:
            data = json.load(f)
    return data


def record_f(file_name, data):
    try:
        with open(file_name, 'r') as f:
            data_old = json.load(f)
        data_old.update(data)
        with open(file_name, 'w') as f:
            json.dump(data_old, f)
    except:
        with open(file_name, 'w') as f:
            json.dump(data, f)


def open_t(file_name):
    file = open(file_name, 'r')
    return file


def record_t(file_name, line):
    file = open(file_name, 'a')
    file.write(line + ' ;\n')
    file.close()


def reader(conn, addr, lst, login):
    right = 1
    while right:
        msg = conn.recv(1024).decode()
        if msg != 'exit':
            date = str(datetime.datetime.now()).split(' ')[0]
            time = ':'.join(str(datetime.datetime.now()).split(' ')[1].split('.')[0].split(':')[:2])
            record_t('hist.txt', login + ', ' + str(addr[1]) + ', ' + date + ', ' + time + ') ' + msg)
            for i in lst:
                if i != conn:
                    i.send((str(addr[1]) + ', ' + login + ', ' + time + ') ' + msg).encode())
        else:
            log_print(login + ', ' + str(addr[1]) + ', ' + str(addr[0]) + ' вышел из беседы')
            lst.remove(conn)
            if len(lst) != 0:
                print('Количество пользователей: ' + str(len(lst)))
            else:
                log_print('Порт пуст, ' + session())
            break
    conn.close()


def main(lst, sock, port):
    conn, addr = sock.accept()

    right = 1
    try:
        data = open_t('book.txt')
    except:
        data = record_t('book.txt', '')
        data = open_t('book.txt')
    nal = 'NO'
    for i in data:
        if i != ' ;\n':
            if i.split(', ')[2] == addr[0]:
                nal = 'YES'
                login = i.split(', ')[0]
    conn.send(str(nal).encode())
    if nal == 'YES':
        stata = open_f('stata.json')
        if stata[login] == conn.recv(1024).decode():
            conn.send('Верный пароль'.encode())
            record_t('book.txt', login + ', ' + str(port) + ', ' + str(addr[0]) + ', ' + str(addr[1]))
        else:
            conn.send('Не верный пароль'.encode())
            log_print('Пользователю' + login + 'не удалось подключиться')
            right = 0
    else:
        login = conn.recv(1024).decode()
        password = conn.recv(1024).decode()
        record_f('stata.json', {login: password})
        record_t('book.txt', login + ', ' + str(port) + ', ' + str(addr[0]) + ', ' + str(addr[1]))

    if right == 1:
        threading.Thread(target=reader, args=(conn, addr, lst, login), daemon=True).start()
        lst.append(conn)
        log_print('Присоединился к беседе: ' + login + ', ' + str(addr[1]) + ', ' + str(addr[0]))
    print('Количество пользователей: ' + str(len(lst)))
    main(lst, sock, port)


def start(sock, l):
    global lst
    port = 8080
    while True:
        try:
            sock.bind(('', port))
            break
        except:
            port = random.randint(8080, 8300)
    print('Свободный порт:', port)
    sock.listen(1)
    lst = []
    main(lst, sock, port)


sock = socket.socket()
s1 = threading.Thread(target=start, args=(sock, 1), daemon=True)
s1.start()


def menu():
    choice = input('1 - Очищение данных\n2 - Удаление логов\n3 - Выход\n4 - Показ логов\n')
    if choice == '1':
        if len(lst) == 0:
            del_ = input('Вы уверены? (1 - Да, 2 - Нет)\n')
            if del_ == '1':

                with open('stata.json', 'w') as f:
                    json.dump({}, f)
                book = open('book.txt', 'w')
                book.close()
                menu()
            else:
                print('Отмена')
                menu()
        else:
            print('Порт не пуст')
            menu()
    elif choice == '2':
        if len(lst) == 0:
            del_ = input('Вы уверены? (1 - Да, 2 - Нет)\n')
            if del_ == '1':
                f = open('server.log', 'w')
                f.close()
            else:
                print('Отмена')
            menu()
        else:
            print('Порт не пуст')
            menu()
    elif choice == '3':
        if len(lst) == 0:
            del_ = input('Вы уверены? (1 - Да, 2 - Нет)\n')
            if del_ == '1':
                sock.close()
            else:
                menu()
        else:
            print('Порт не пуст')
            menu()
    elif choice == '4':
        if len(lst) == 0:
            del_ = input('Вы уверены? (1 - Да, 2 - Нет)\n')
            if del_ == '1':
                f = open('server.log', 'r')
                print(*f)
            else:
                print('Отмена')
            menu()
        else:
            print('Порт не пуст')
            menu()
        # замки мб, Event() через set и clear
    else:
        print('Неверный ввод')
        menu()


logging.basicConfig(filename='server.log', encoding='utf-8', level=logging.INFO)
log_print('Порт пуст')

menu()