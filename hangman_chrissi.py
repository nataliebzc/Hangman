import random
import customtkinter as ctk
from tkinter import messagebox

# ASCII representations of the hangman for every remaining try (6 → 0)
STAGES = [
    """
       ------
       |    |
       |    O
       |   /|\\
       |   / \\
       |
    """,
    """
       ------
       |    |
       |    O
       |   /|\\
       |   /
       |
    """,
    """
       ------
       |    |
       |    O
       |   /|
       |
       |
    """,
    """
       ------
       |    |
       |    O
       |
       |
       |
    """,
    """
       ------
       |    |
       |
       |
       |
       |
    """,
    """
       ------
       |
       |
       |
       |
       |
    """,
    """





    """,
]

WORDS = ["python", "hangman", "challenge", "programming", "computer"]


class HangmanGame(ctk.CTk):
    """CustomTkinter-based Hangman game."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Hangman")
        self.geometry("500x400")
        self.resizable(False, False)
        self._setup_game_state()
        self._create_widgets()

    def _setup_game_state(self):
        self.word: str = random.choice(WORDS)
        self.word_completion: list[str] = ["_"] * len(self.word)
        self.guessed_letters: set[str] = set()
        self.guessed_words: set[str] = set()
        self.tries: int = 6
        self.game_over: bool = False

    def _process_letter_guess(self, letter: str):
        if letter in self.guessed_letters:
            messagebox.showinfo("Schon geraten", f"Den Buchstaben '{letter}' hast du bereits geraten.")
            return
        self.guessed_letters.add(letter)

        if letter in self.word:
            for idx, ch in enumerate(self.word):
                if ch == letter:
                    self.word_completion[idx] = letter
            self._update_word_label()
            if "_" not in self.word_completion:
                self._end_game(won=True)
        else:
            self.tries -= 1
            self._update_stage()

    def _process_word_guess(self, word_guess: str):
        if len(word_guess) != len(self.word):
            messagebox.showwarning("Falsche Länge", "Das Wort hat eine andere Länge.")
            return
        if word_guess in self.guessed_words:
            messagebox.showinfo("Schon geraten", f"Das Wort '{word_guess}' hast du bereits geraten.")
            return
        self.guessed_words.add(word_guess)

        if word_guess == self.word:
            self.word_completion = list(self.word)
            self._update_word_label()
            self._end_game(won=True)
        else:
            self.tries -= 1
            self._update_stage()

    def _create_widgets(self):
        self.stage_label = ctk.CTkLabel(self, text=STAGES[-1], font=("Courier", 12), justify="left")
        self.stage_label.pack(pady=(10, 5))

        self.word_label = ctk.CTkLabel(self, text=" ".join(self.word_completion), font=("Helvetica", 18))
        self.word_label.pack()

        self.info_label = ctk.CTkLabel(self, text=f"Tries left: {self.tries}", font=("Helvetica", 12))
        self.info_label.pack(pady=5)

        self.entry = ctk.CTkEntry(self, width=200, justify="center")
        self.entry.pack(pady=5)
        self.entry.bind("<Return>", self._make_guess_event)

        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=5)

        self.guess_button = ctk.CTkButton(button_frame, text="Guess", command=self._make_guess)
        self.guess_button.grid(row=0, column=0, padx=10)

        self.replay_button = ctk.CTkButton(button_frame, text="Play Again", command=self._play_again, state="disabled")
        self.replay_button.grid(row=0, column=1, padx=10)

        self.guessed_label = ctk.CTkLabel(self, text="Guessed letters:", font=("Helvetica", 10))
        self.guessed_label.pack(pady=5)

    def _update_stage(self):
        self.stage_label.configure(text=STAGES[self.tries])
        self.info_label.configure(text=f"Tries left: {self.tries}")
        self.guessed_label.configure(text=f"Guessed false letters: {', '.join(sorted(self.guessed_letters))}")
        if self.tries <= 0:
            self._end_game(won=False)

    def _update_word_label(self):
        self.word_label.configure(text=" ".join(self.word_completion))

    def _make_guess_event(self, event):
        self._make_guess()

    def _make_guess(self):
        if self.game_over:
            return

        guess = self.entry.get().lower().strip()
        self.entry.delete(0, 'end')

        if not guess.isalpha():
            messagebox.showwarning("Ungültige Eingabe", "Bitte gib einen Buchstaben oder ein Wort ein.")
            return

        if len(guess) == 1:
            self._process_letter_guess(guess)
        else:
            self._process_word_guess(guess)

    def _end_game(self, *, won: bool):
        self.game_over = True
        message = (
            f"Congratulations! You guessed the word '{self.word}'."
            if won
            else f"Sorry, you ran out of tries. The word was '{self.word}'."
        )
        messagebox.showinfo("Hangman", message)
        self.replay_button.configure(state="normal")
        self.guess_button.configure(state="disabled")

    def _play_again(self):
        self._setup_game_state()
        self.stage_label.configure(text=STAGES[-1])
        self._update_word_label()
        self.info_label.configure(text=f"Tries left: {self.tries}")
        self.guessed_label.configure(text="Guessed false letters:")
        self.guess_button.configure(state="normal")
        self.replay_button.configure(state="disabled")
        self.entry.focus()


if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    HangmanGame().mainloop()