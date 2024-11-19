import tkinter as tk
from tkinter import messagebox
import random


root = tk.Tk()
root.title("Rock Paper Scissors Game")
root.geometry("450x600")
root.config(bg="#f9f5eb")  


FONT_TITLE = ("Helvetica", 20, "bold")
FONT = ("Helvetica", 16)
BUTTON_FONT = ("Helvetica", 14)
TEXT_COLOR = "#383e56"
HIGHLIGHT_COLOR = "#9fedd7"
WIN_COLOR = "#90be6d"
LOSE_COLOR = "#f28482"
TIE_COLOR = "#f4a261"


choices = ["Rock", "Paper", "Scissors"]
user_score = 0
computer_score = 0


def determine_winner(user_choice):
    global user_score, computer_score
    
    
    computer_choice = random.choice(choices)
    result_text.set(f"Computer chose: {computer_choice}")
    
    
    if user_choice == computer_choice:
        result = "It's a Tie!"
        result_label.config(fg=TIE_COLOR)
    elif (user_choice == "Rock" and computer_choice == "Scissors") or \
         (user_choice == "Paper" and computer_choice == "Rock") or \
         (user_choice == "Scissors" and computer_choice == "Paper"):
        result = "You Win! 🎉"
        user_score += 1
        result_label.config(fg=WIN_COLOR)
    else:
        result = "You Lose! 😢"
        computer_score += 1
        result_label.config(fg=LOSE_COLOR)
    
    
    result_text.set(f"Computer chose: {computer_choice} | {result}")
    update_scoreboard()


def update_scoreboard():
    scoreboard_text.set(f"Your Score: {user_score} | Computer Score: {computer_score}")


def reset_game():
    global user_score, computer_score
    user_score = 0
    computer_score = 0
    result_text.set("Make your move!")
    update_scoreboard()


instructions = (
    "Welcome to Rock Paper Scissors!\n\n"
    "Instructions:\n"
    "1. Click on 'Rock', 'Paper', or 'Scissors' to make your move.\n"
    "2. The computer will also make its choice.\n"
    "3. Rock beats Scissors, Scissors beats Paper, and Paper beats Rock.\n"
    "4. The scoreboard will update based on the results.\n"
    "5. Click 'Reset Game' to start over.\n\n"
    "Have fun playing!"
)


frame = tk.Frame(root, bg="#f9f5eb")
frame.pack(pady=10)


title_label = tk.Label(frame, text="Rock Paper Scissors", font=FONT_TITLE, bg="#f9f5eb", fg=TEXT_COLOR)
title_label.pack(pady=10)


instructions_label = tk.Label(frame, text=instructions, font=("Helvetica", 12), bg="#f9f5eb", fg=TEXT_COLOR, justify="left")
instructions_label.pack(pady=10)


result_text = tk.StringVar()
result_text.set("Make your move!")
result_label = tk.Label(frame, textvariable=result_text, font=FONT, bg="#f9f5eb", fg=TEXT_COLOR)
result_label.pack(pady=20)

# Creating buttons for Rock, Paper, Scissors
button_frame = tk.Frame(frame, bg="#f9f5eb")
button_frame.pack(pady=20)

rock_button = tk.Button(button_frame, text="Rock ✊", font=BUTTON_FONT, bg="#9fedd7", 
                        command=lambda: determine_winner("Rock"))
rock_button.grid(row=0, column=0, padx=15, pady=10)

paper_button = tk.Button(button_frame, text="Paper ✋", font=BUTTON_FONT, bg="#f8b400", 
                         command=lambda: determine_winner("Paper"))
paper_button.grid(row=0, column=1, padx=15, pady=10)

scissors_button = tk.Button(button_frame, text="Scissors ✌️", font=BUTTON_FONT, bg="#e58c8a", 
                            command=lambda: determine_winner("Scissors"))
scissors_button.grid(row=0, column=2, padx=15, pady=10)


scoreboard_text = tk.StringVar()
scoreboard_text.set(f"Your Score: {user_score} | Computer Score: {computer_score}")
scoreboard_label = tk.Label(root, textvariable=scoreboard_text, font=FONT, bg="#f9f5eb", fg=TEXT_COLOR)
scoreboard_label.pack(pady=20)


reset_button = tk.Button(root, text="Reset Game", font=BUTTON_FONT, bg="#f28482", command=reset_game)
reset_button.pack(pady=10)


root.mainloop()
