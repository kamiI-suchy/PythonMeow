#!/usr/bin/env python3

import socket


HOST = "127.0.0.1"
PORT = 65432


def recv_line(sock: socket.socket) -> str:
    chunks: list[str] = []
    while True:
        data = sock.recv(1024)
        if not data:
            if chunks:
                raise ConnectionError("Connection closed before response completed.")
            raise ConnectionError("Server connection was closed.")
        decoded = data.decode('utf-8', errors='replace')
        if "\n" in decoded:
            first_line = decoded.split("\n", 1)[0]
            chunks.append(first_line)
            return "".join(chunks).strip()
        chunks.append(decoded)


def run_client() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        while True:
            try:
                command = input()
            except (EOFError, KeyboardInterrupt):
                break
            try:
                sock.sendall((command.strip() + "\n").encode())
                response = recv_line(sock)
                print(f"-> {response}")
            except ConnectionError as error:
                print(f"Error: {error}")
                break


if __name__ == "__main__":
    run_client()
