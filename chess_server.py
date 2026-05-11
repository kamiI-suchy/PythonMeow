#!/usr/bin/env python3

import socket


HOST = "127.0.0.1"
PORT = 65432

BOARD_FILES = "abcdefgh"
RANKS = "12345678"
VALID_FIELDS = {f"{file_}{rank}" for rank in RANKS for file_ in BOARD_FILES}
VALID_FIGURES = {
    "WK",
    "WQ",
    "WB",
    "WN",
    "WR",
    "WP",
    "BK",
    "BQ",
    "BB",
    "BN",
    "BR",
    "BP",
}
ALL_FIELDS_ORDERED = [f"{file_}{rank}" for rank in RANKS for file_ in BOARD_FILES]


def handle_command(command: str, board: dict[str, str]) -> str:
    parts = command.split()
    if not parts:
        return "not found"

    action = parts[0].lower()

    if action == "put" and len(parts) == 3:
        figure, field = parts[1], parts[2].lower()
        if figure not in VALID_FIGURES or field not in VALID_FIELDS:
            return "not found"
        previous = board.get(field, "E")
        board[field] = figure
        return "set" if previous == "E" else f"{previous} replaced"

    if action == "delete" and len(parts) == 2:
        field = parts[1].lower()
        if field not in VALID_FIELDS:
            return "not found"
        previous = board.get(field, "E")
        if previous == "E":
            return "E"
        board[field] = "E"
        return f"{previous} deleted"

    if action == "clear" and len(parts) == 1:
        removed = sum(1 for value in board.values() if value != "E")
        for field in ALL_FIELDS_ORDERED:
            board[field] = "E"
        return str(removed)

    if action == "get" and len(parts) == 2:
        field = parts[1].lower()
        if field not in VALID_FIELDS:
            return "not found"
        return board.get(field, "E")

    if action == "getall" and len(parts) == 1:
        return " ".join(f"{field}-{board.get(field, 'E')}" for field in ALL_FIELDS_ORDERED)

    return "not found"


def run_server() -> None:
    # As required by the assignment, the server handles a single client connection.
    board = {field: "E" for field in ALL_FIELDS_ORDERED}

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((HOST, PORT))
        sock.listen(1)
        conn, _ = sock.accept()
        with conn:
            buffer = ""
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                buffer += data.decode('utf-8', errors='replace')
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    response = handle_command(line.strip(), board)
                    conn.sendall((response + "\n").encode())


if __name__ == "__main__":
    run_server()
