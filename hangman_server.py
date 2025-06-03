import socket
import threading
import random

WORDS = ["python", "hangman", "challenge", "programming", "computer", "customtkinter", "game", "development", "interface", "functionality"]

class HangmanServer:
    def __init__(self, host="localhost", port=65432):
        self.word = random.choice(WORDS)
        self.word_completion = ["_"] * len(self.word)
        self.guessed_letters = set()
        self.guessed_words = set()
        self.tries = 6
        self.host = host
        self.port = port

    def handle_client(self, conn, addr):
        print(f"{addr} connected.")

        while self.tries > 0 and "_" in self.word_completion:
            try:
                data = conn.recv(1024).decode().strip()
                if not data:
                    break

                response = self.process_guess(data)
                conn.send(response.encode())

            except ConnectionResetError:
                break

        conn.close()
        print(f"{addr} disconnected.")

    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen()

        print(f"Server is listening on {self.host}:{self.port}")
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()

if __name__ == "__main__":
    HangmanServer().start()
