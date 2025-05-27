import customtkinter as ctk
import random

<<<<<<< HEAD
def random_word():
    words = ["python", "hangman", "challenge", "programming", "customtkinter"]
    return random.choice(words)
button = ctk.CTkButton(
    text="Test",
    command=lambda: print("Button clicked"),
    width=30,
    height=30
)
