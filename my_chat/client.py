#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import sys
import threading
from time import sleep


def read(sock):
    while True:
        try:
            data = sock.recv(4096)
        except OSError as e:
            break
        try:
            if data.decode('utf-8'):
                print(data.decode('utf-8'))
            else:
                break
        except UnicodeDecodeError:
            print('invalid characters')


def write(sock):
    global thread_flag
    print('Press Cntrl+C to stop')
    alias = input('input your alias: ')  # Вводим наш псевдоним
    while thread_flag:
        sleep(0.5)
        try:
            message = input('input ip, port and message through a "^":  ')
        except ValueError:
            break
        try:
            ip, port, data = message.split('^')
        except ValueError:
            if thread_flag:
                print('invalid message, wrong amount of separators (must be 2)')
                continue
            break
        try:
            message_encoded = (ip + '///' + port + '///' + f'[{alias}]' + data).encode('utf-8')
        except UnicodeEncodeError:
            print('invalid characters')
        else:
            try:
                sock.send(message_encoded)
            except OSError:
                break


def main():
    global thread_flag
    thread_flag = True
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server = 'localhost', 7047  # введите адрес и порт своего сервера
    try:
        sock.connect(server)
    except ConnectionError:
        sys.exit("Connection refused")
    try:
        thread = threading.Thread(target=write, args=(sock, ))
        thread.start()
        read(sock)
        sock.close()
        thread_flag = False
        thread.join()
        sys.exit("\nServer dropped connection")
    except KeyboardInterrupt:
        sock.close()
        thread_flag = False
        exit('\nPress enter...')


if __name__ == '__main__':
    main()
