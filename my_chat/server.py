#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import selectors
import sys
import syslog


def connect(server_sock):

    client, address = server_sock.accept()
    print(':'.join(map(str, address)), 'connected')
    selector.register(fileobj=client, events=selectors.EVENT_READ, data=receive)
    if address not in connections:
        connections[address] = client  # добавляем клиента в словарь соединений


def receive(client):

    address = str(client).split("'")[-2], int(str(client).split("'")[-1][2:-2])  # из объекта-сокета вычленяем адрес

    try:
        message = client.recv(4096)  # принять 4 кб с клиента / блокировка и ожидание сообщения
    except OSError:
        print(':'.join(map(str, address)), 'disconnected')
        del connections[address]
        selector.unregister(client)
        client.close()  # отсоединить клиента
    else:
        if message:
            message_decoded = message.decode('utf-8')
            try:  # валидация ip и порта
                ip, port, data = message_decoded.split('///')
                # логирование сообщений в syslog
                syslog.syslog(syslog.LOG_NOTICE,
                              f'from: {address[0]}:{address[1]}  to: {ip}:{port}  message: {data}'.strip())
                address = ip, int(port)
                if (ip.count('.') != 3) or (int(port) < 1):
                    raise ValueError
                tuple(map(int, ip.split('.')))
            except ValueError:
                try:
                    client.send('invalid address'.encode('utf-8'))
                except ConnectionError:
                    print(':'.join(map(str, address)), 'disconnected')
                    del connections[address]
                    selector.unregister(client)
                    client.close()  # отсоединить клиента
            else:
                if address in connections:
                    try:
                        connections[address].send(('\n' + data + '\n').encode('utf-8'))
                        client.send('message delivered :) '.encode('utf-8'))
                    except ConnectionError:
                        client.send("message not delivered :'( ".encode('utf-8'))
                else:
                    client.send("message not delivered :'( \nNo such address".encode('utf-8'))
        else:
            print(':'.join(map(str, address)), 'disconnected')
            del connections[address]
            selector.unregister(client)
            client.close()  # отсоединить клиента


def event_loop():
    while True:

        events = selector.select()

        for key, event in events:
            callback = key.data
            callback(key.fileobj)


def main():
    global connections
    global selector
    connections = dict()  # (ip, port) : client_socket

    selector = selectors.DefaultSelector()
    
    syslog.openlog(sys.argv[0])
    print(socket.gethostname(), 'started working...\nPress Cntrl+C to stop')
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(('', 7047))
    server_sock.listen(5)
    selector.register(fileobj=server_sock, events=selectors.EVENT_READ, data=connect)
    try:
        event_loop()
    except KeyboardInterrupt as e:

        for item in connections.values():
            selector.unregister(item)
            item.close()
        selector.unregister(server_sock)
        server_sock.close()
        syslog.closelog()
        print('\nProgram stopped working...')


if __name__ == '__main__':
    main()
