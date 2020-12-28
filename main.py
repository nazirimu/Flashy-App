from tkinter import *
from PIL import ImageTk, Image
import pandas as pd
import random

# --------------------- CONSTANTS ---------------------- #

BACKGROUND_COLOR = "#B1DDC6"
FONT_NAME = "arial"
timer = None


# --------------------- CORRECT BUTTON ------------------------------- #
def right_button():
    global current_card, to_learn
    # Removes the word that was known to the user, it is then saved to a new file as a csv
    to_learn.remove(current_card)
    df = pd.DataFrame(to_learn)
    df.to_csv("data/words_to_learn",index=False)
    # Calls the next card function to move to the next card
    next_card()

# --------------------- FLIPPING THROUGH THE CARDS ------------------- #
def next_card():
    global timer, current_card
    # switches to the next card, changing the GUI and the text.
    window.after_cancel(timer)
    # Generates a random word from the list
    current_card = random.choice(to_learn)
    # These lines change the canvas
    canvas.itemconfig(language_label, text="French", fill="black")
    canvas.itemconfig(word_label, text=current_card["French"], fill="black")
    canvas.itemconfig(canvas_image, image=front_card_image)
    # Gives the user 3 seconds to see if they remember before it flips the card
    timer = window.after(3000, func=flip_card)


def flip_card():
    global timer, current_card
    # Flips the card, switching to the other side and changing the GUI
    window.after_cancel(timer)
    # These lines change the canvas
    canvas.itemconfig(canvas_image, image=back_card_image)
    canvas.itemconfig(language_label, text="English", fill="white")
    canvas.itemconfig(word_label, text=current_card["English"], fill="white")


# --------------------- OBTAINING WORDS ---------------- #
# Importing the data as df
try:
    # If the file has not been run before, this file wont be found
    words_dataframe = pd.read_csv("data/words_to_learn")
except FileNotFoundError:
    words_dataframe = pd.read_csv("data/french_words.csv")
finally:
    # Creates a list using the dataframe that was obtained
    to_learn = words_dataframe.to_dict(orient="records")
    current_card = {}

# --------------------- UI ----------------------------- #
# Sets up the window
window = Tk()
window.title("Flash Card App")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

timer = window.after(3000, func=flip_card)

# Canvas
canvas = Canvas(height=526, width=800, bg=BACKGROUND_COLOR, highlightthickness=0)
front_card_image = ImageTk.PhotoImage(Image.open("images/card_front.png"))
back_card_image = ImageTk.PhotoImage(Image.open("images/card_back.png"))
canvas_image = canvas.create_image(400, 260, image=front_card_image)
canvas.grid(column=0, row=0, columnspan=2)

# Buttons
# # Correct Button
correct_button = PhotoImage(file="images/right.png")
button = Button(image=correct_button, highlightthickness=0, command=right_button)
button.grid(row=1, column=1)

# # Wrong Button
cross_button = PhotoImage(file="images/wrong.png")
button = Button(image=cross_button, highlightthickness=0, command=next_card)
button.grid(row=1, column=0)

# Labels
language_label = canvas.create_text(400, 150, text="French", font=(FONT_NAME, 40, "italic"))
word_label = canvas.create_text(400, 263, text='word', font=(FONT_NAME, 60, "bold"))

next_card()

window.mainloop()
