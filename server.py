#!/usr/bin/env python3

import socket

HOST = '127.0.0.1'
PORT = 65432
FILES = tuple("abcdefgh")
RANKS = tuple("12345678")
VALID_FIELDS = {f"{file}{rank}" for rank in RANKS for file in FILES}
VALID_FIGURES = {"WK", "WQ", "WB", "WN", "WR", "WP", "BK", "BQ", "BB", "BN", "BR", "BP"}
ALL_FIELDS = [f"{file}{rank}" for rank in RANKS for file in FILES]

def handle(board, request):
    args = request.strip().split()
    if not args:
        return "not found"

    operation = args[0]

    if operation == "put" and len(args) == 3:
        figure, field = args[1], args[2]
        if figure not in VALID_FIGURES or field not in VALID_FIELDS:
            return "not found"
        previous = board[field]
        board[field] = figure
        return "set" if previous == "E" else f"{previous} replaced"

    if operation == "delete" and len(args) == 2:
        field = args[1]
        if field not in VALID_FIELDS:
            return "not found"
        current = board[field]
        if current == "E":
            return "E"
        board[field] = "E"
        return f"{current} deleted"

    if operation == "clear" and len(args) == 1:
        removed = sum(1 for value in board.values() if value != "E")
        for field in board:
            board[field] = "E"
        return str(removed)

    if operation == "get" and len(args) == 2:
        field = args[1]
        if field not in VALID_FIELDS:
            return "not found"
        return board[field]

    if operation == "getall" and len(args) == 1:
        return " ".join(f"{field}-{board[field]}" for field in ALL_FIELDS)

    return "not found"


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    print(f'Serwer nasłuchuje na {HOST}:{PORT}')
    while True:
        conn, addr = s.accept()
        with conn:
            print('Połączono z', addr)
            board = {field: "E" for field in ALL_FIELDS}
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                response = handle(board, data.decode('utf-8'))
                conn.sendall(response.encode('utf-8'))

        
