# this is a generic flash card programme, that only requires a single file in the \data folder names 'data.csv' to
# function. CSV file must be in format of two columns

# imports
import pandas
from tkinter import *
import random

# create root window

window = Tk()

# constants
CARD_BACK = PhotoImage(file=".\images\card_back.png")
CARD_FRONT = PhotoImage(file=".\images\card_front.png")
CORRECT = PhotoImage(file=".\images\correct.png")
INCORRECT = PhotoImage(file=".\images\incorrect.png")
BACKGROUND_COLOR = "#B1DDC6"
FONT = "arial"
LANGUAGE_FONT_SIZE = "40"
WORD_FONT_SIZE = "60"

# pandas setup to read csv data, format into list of dictionaries, column header as keywords, word as value.
# create list from column headers
data = pandas.read_csv("./data/data.csv")
data_dict = data.to_dict("records")
column_list = list(data)


# variables
var = random.randint(0, len(data_dict) - 1)
learn_word = data_dict[var][column_list[0]]
meaning = data_dict[var][column_list[1]]


# functions
def flip_card():
    canvas.itemconfig(card, image=CARD_BACK)
    canvas.itemconfig(language_text, text=column_list[1], fill="white")
    canvas.itemconfig(word_text, text=meaning, fill="white")
    correct_button.wait_variable(var)
    incorrect_button.wait_variable(var)


def reset_card():
    canvas.itemconfig(card, image=CARD_FRONT)
    canvas.itemconfig(language_text, text=column_list[0], fill="black")
    canvas.itemconfig(word_text, text=learn_word, fill="black")


def incorrect():
    global var, learn_word, meaning, flip_timer
    window.after_cancel(flip_timer)
    var = random.randint(0, len(data_dict) - 1)
    learn_word = data_dict[var][column_list[0]]
    meaning = data_dict[var][column_list[1]]
    reset_card()
    flip_timer = window.after(3000, flip_card)


def correct():
    global var, learn_word, meaning, flip_timer
    del data_dict[var]
    # convert dict to df then to CSV, overwrite data.csv
    df = pandas.DataFrame.from_dict(data_dict)
    df.to_csv(".\data\\data.csv", index_label=False, index=False)
    window.after_cancel(flip_timer)
    var = random.randint(0, len(data_dict) - 1)
    learn_word = data_dict[var][column_list[0]]
    meaning = data_dict[var][column_list[1]]
    reset_card()
    flip_timer = window.after(3000, flip_card)


# window config
window.title("Flashy Learning")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# UI components
# create canvas and background image
canvas = Canvas(bg=BACKGROUND_COLOR, highlightthickness=0, width=800, height=526)
card = canvas.create_image((400, 263), image=CARD_FRONT)
# card text
language_text = canvas.create_text((400, 150), font=(FONT, LANGUAGE_FONT_SIZE, "italic"), text=column_list[0])
word_text = canvas.create_text((400, 263), font=(FONT, WORD_FONT_SIZE, "bold"), text=learn_word)

# create buttons
correct_button = Button(image=CORRECT, bd=0, highlightthickness=0, relief="flat", command=correct)
incorrect_button = Button(image=INCORRECT, bd=0, highlightthickness=0, relief="flat", command=incorrect)

# UI layout
canvas.grid(column=0, row=0, columnspan=2, rowspan=2)
correct_button.grid(column=0, row=2)
incorrect_button.grid(column=1, row=2)

flip_timer = window.after(3000, flip_card)
window.mainloop()
