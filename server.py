#!/usr/bin/env python3

import socket

HOST = '127.0.0.1'
PORT = 65432

def handle(board, req):
    args = req.split()
    operation = args[0]

    out = ""

    match operation:
        case "put":
            figure = args[1]
            field = args[2]
            if board[field] == 'E':
                board[field] = figure
                return "set"
            else:
                out = (f"{board[field]} replaced")
                board[field] = figure
                return out
        case "delete":
            field = args[1]
            if board[field] == 'E':
                return "E"
            else:
                out = (f"{board[field]} deleted")
                board[field] == 'E'
                return out
        case "clear":
            counter = 0
            for x in board:
                if board[x] != 'E':
                    counter += 1
                    board[x] = 'E'
            return str(counter)
        case "get":
            field = args[1]
            return str(board[field])
        case "getall":
            for x in board:
                out += (f"{x}-{board[x]} ")
            return out
        case _:
            return "unknown operation"
        
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    print(f'Serwer nasłuchuje na {HOST}:{PORT}')
    while True:
        conn, addr = s.accept()
        with conn:
            print('Połączono z', addr)
            board = {
                'a8': 'E', 'b8': 'E', 'c8': 'E', 'd8': 'E', 'e8': 'E', 'f8': 'E', 'g8': 'E', 'h8': 'E',
                'a7': 'E', 'b7': 'E', 'c7': 'E', 'd7': 'E', 'e7': 'E', 'f7': 'E', 'g7': 'E', 'h7': 'E',
                'a6': 'E', 'b6': 'E', 'c6': 'E', 'd6': 'E', 'e6': 'E', 'f6': 'E', 'g6': 'E', 'h6': 'E',
                'a5': 'E', 'b5': 'E', 'c5': 'E', 'd5': 'E', 'e5': 'E', 'f5': 'E', 'g5': 'E', 'h5': 'E',
                'a4': 'E', 'b4': 'E', 'c4': 'E', 'd4': 'E', 'e4': 'E', 'f4': 'E', 'g4': 'E', 'h4': 'E',
                'a3': 'E', 'b3': 'E', 'c3': 'E', 'd3': 'E', 'e3': 'E', 'f3': 'E', 'g3': 'E', 'h3': 'E',
                'a2': 'E', 'b2': 'E', 'c2': 'E', 'd2': 'E', 'e2': 'E', 'f2': 'E', 'g2': 'E', 'h2': 'E',
                'a1': 'E', 'b1': 'E', 'c1': 'E', 'd1': 'E', 'e1': 'E', 'f1': 'E', 'g1': 'E', 'h1': 'E',
            }
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                response = handle(board, data.decode('utf-8'))
                conn.sendall(response.encode('utf-8'))

        