#!/usr/bin/env python3

import socket

HOST = '127.0.0.1'
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        try:
            query = input()
        except EOFError:
            break

        query = query.strip()
        if not query:
            continue

        s.sendall(query.encode('utf-8'))
        data = s.recv(1024)
        print(f"-> {data.decode('utf-8')}")
