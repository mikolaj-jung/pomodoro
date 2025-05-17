import tkinter
from tkinter import Canvas, PhotoImage
import math
import pygame

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None
paused = False
remaining_time = 0
is_on = False

def music_after_work():
    pygame.mixer.init()
    pygame.mixer.music.load("end_work.wav")
    pygame.mixer.music.play()

def music_after_break():
    pygame.mixer.init()
    pygame.mixer.music.load("end_break.wav")
    pygame.mixer.music.play()

# ---------------------------- FOCUSING WINDOW ------------------------------- #
def focus_window(option):
    if option == "on":
        window.deiconify()
        window.focus_force()
        window.attributes('-topmost', 1)
    elif option == "off":
        window.attributes('-topmost', 0)

# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    global reps, is_on
    is_on = False
    reps = 0
    window.after_cancel(timer)
    timer_label.config(text="Timer", font=(FONT_NAME, 35, "bold"), bg=YELLOW, fg=GREEN)
    check_boxes.config(text="☐" * 4, fg=GREEN, bg=YELLOW, font=("", 20))
    canvas.itemconfig(timer_text, text="00:00")

# ---------------------------- TIMER PAUSE ------------------------------- #
def timer_pause():
    global timer, paused, remaining_time

    if not paused:
        paused = True
        window.after_cancel(timer)

# ---------------------------- TIMER MECHANISM ------------------------------- #
def timer_mechanism():
    global reps, paused, remaining_time, is_on

    if paused:
        paused = False
        count_down(remaining_time)

    if not is_on:
        is_on = True
        work_sec = WORK_MIN * 60
        short_break_sec = SHORT_BREAK_MIN * 60
        long_break_sec = LONG_BREAK_MIN * 60
        work_reps = [0, 2, 4, 6]
        short_break_reps = [1, 3, 5]
        long_break_rep = 7

        if reps in work_reps:
            focus_window(option="off")
            timer_label.config(text="Work", font=(FONT_NAME, 35, "bold"), bg=YELLOW, fg=GREEN)
            count_down(work_sec)
            reps += 1
        elif reps in short_break_reps:
            focus_window(option="on")
            timer_label.config(text="Break", font=(FONT_NAME, 35, "bold"), bg=YELLOW, fg=PINK)
            count_down(short_break_sec)
            reps += 1
        elif reps == long_break_rep:
            focus_window(option="on")
            timer_label.config(text="Break", font=(FONT_NAME, 35, "bold"), bg=YELLOW, fg=RED)
            count_down(long_break_sec)
            reps = 0

        check_boxes.config(text="✔" * (reps // 2) + "☐" * (4 - reps // 2))
# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    global paused, remaining_time, timer, is_on

    if not paused:
        minutes = math.floor(count / 60)
        seconds = count % 60

        if minutes < 10:
            minutes = f"0{minutes}"

        if seconds < 10:
            seconds = f"0{seconds}"

        canvas.itemconfig(timer_text, text=f"{minutes}:{seconds}")

        if count > 0:
            remaining_time = count - 1
            timer = window.after(1000, count_down, remaining_time)

        if count == 0:
            if reps in [0, 2, 4, 6, 8]:
                music_after_break()
            else:
                music_after_work()
            is_on = False
            timer_mechanism()

# ---------------------------- UI SETUP ------------------------------- #
window = tkinter.Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

timer_label = tkinter.Label(text="Timer", font=(FONT_NAME, 35, "bold"), bg=YELLOW, fg=GREEN)
timer_label.grid(row=0, column=1)

start_button = tkinter.Button(text="Start", command=timer_mechanism)
start_button.grid(row=2, column=0)

reset_button = tkinter.Button(text="Reset", command=reset_timer)
reset_button.grid(row=2, column=2)

pause_button = tkinter.Button(text="Pause", command=timer_pause)
pause_button.grid(row=2, column=3, padx=5)

check_boxes = tkinter.Label(text="☐" * 4, fg=GREEN, bg=YELLOW, font=("", 20))
check_boxes.grid(row=3, column=1)

canvas = Canvas(width=200, height=224, bg= YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 135, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(row=1, column=1)

window.mainloop()
