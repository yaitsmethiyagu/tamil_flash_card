from tkinter import *
from tkinter import messagebox
import pandas
import random


to_learn ={}
df = {}
try:

    to_learn = pandas.read_csv("data/to_learn.csv")

except FileNotFoundError:
    df = pandas.read_csv("data/tamil.csv")

except pandas.errors.EmptyDataError:
    df = pandas.read_csv("data/tamil.csv")

else:
    df = to_learn

dataframe = df.to_dict(orient="records")
df_length = len(dataframe)
current_card = None


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)

    current_card = random.choice(dataframe)

    choosen_tamil_word = current_card["tamilword"]

    canvas.itemconfig(card_image, image=front_image)
    canvas.itemconfig(card_word, text=choosen_tamil_word, fill="black")
    canvas.itemconfig(card_language, text="Tamil", fill="black")
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)

    canvas.itemconfig(card_image, image=back_image)
    canvas.itemconfig(card_word, text=current_card["englishword"], fill="gray")
    canvas.itemconfig(card_language, text="English", fill="black")


def remove_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)

    try:
        dataframe.remove(current_card)
        data = pandas.DataFrame(dataframe)
        data.to_csv("data/to_learn.csv", index= False)
        next_card()

    except IndexError:
        messagebox.showinfo(title="End of workds", message="Congrats you learnt all frequent tamil words" )


BACKGROUND_COLOR = "#B1DDC6"

window = Tk()

window.minsize(width=800, height=800)
window.title("Tamil - Engligh flash card")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)

canvas = Canvas(width=800, height=536)
front_image = PhotoImage(file="images/card_front.png")
back_image = PhotoImage(file="images/card_back.png")
right_image = PhotoImage(file="images/right.png")
wrong_image = PhotoImage(file="images/wrong.png")

card_image = canvas.create_image(400, 263, image=front_image)
card_language = canvas.create_text(400, 150, text="Tamil", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 50, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)

right_button = Button(image=right_image, highlightthickness=0, bd=0, command=next_card)
wrong_button = Button(image=wrong_image, highlightthickness=0, bd=0, command=remove_card)

canvas.grid(column=0, row=0, columnspan=2)
right_button.grid(column=1, row=1)
wrong_button.grid(column=0, row=1)
flip_timer = window.after(3000, func=flip_card)
next_card()

window.mainloop()
