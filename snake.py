from tkinter import *

WINDOW_HEIGHT = 800
WINDOW_WIDTH = 800
SPACE_SIZE = 25
BACKGROUND_COLOR = "#B7B0AA"
GAME_SPEED = 500 # Update frequency in ms

class Snake:
    def __init__(self, color):
        self._color = color
        self._coordinates = []
        self._circles = []

        self._coordinates.append((0,0))

        for x, y in self._coordinates:
            canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=self._color, outline="black")




def next_turn(snake):
    x, y = snake._coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE

    snake._coordinates.insert(0, (x,y))
    canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=snake._color, outline="black")
        
    window.after(GAME_SPEED, next_turn, snake)

def change_direction():
    pass

def check_collisions():
    pass

def game_over():
    pass

window = Tk()
window.title("PvP Snake")
window.resizable(False, False)

direction = "down"

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=WINDOW_HEIGHT, width=WINDOW_WIDTH)
canvas.pack()

snake = Snake("red")

next_turn(snake)

window.mainloop()


