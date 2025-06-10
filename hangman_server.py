import socket
import threading
import random

WORDS = ["python", "hangman", "challenge", "programming", "computer", "customtkinter", "game", "development", "interface", "functionality"]

class HangmanServer:
    def __init__(self, host="127.0.0.1", port=5555):
        self.word = random.choice(WORDS)
        self.word_completion = ["_"] * len(self.word)
        self.guessed_letters = set()
        self.guessed_words = set()
        self.tries = 6
        self.host = host
        self.port = port

    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen()

        print(f"Server is listening on {self.host}:{self.port}")
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()

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

    def process_guess(self, guess):
        if len(guess) == 1 and guess.isalpha():
            return self.process_letter_guess(guess.lower())
        elif len(guess) > 1 and guess.isalpha():
            return self.process_word_guess(guess.lower())
        else:
            return "Invalid input. Please guess a letter or a word."
        
    def process_letter_guess(self, letter):
        if letter in self.guessed_letters:
            return f"You already guessed the letter '{letter}'."

        self.guessed_letters.add(letter)

        if letter in self.word:
            indices = [i for i, l in enumerate(self.word) if l == letter]
            for index in indices:
                self.word_completion[index] = letter
            return f"Good job! '{letter}' is in the word: {''.join(self.word_completion)}"
        else:
            self.tries -= 1
            return f"'{letter}' is not in the word. You have {self.tries} tries left."
if __name__ == "__main__":
    HangmanServer().start()
