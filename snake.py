from tkinter import *

WINDOW_HEIGHT = 800
WINDOW_WIDTH = 800
SPACE_SIZE = 25
BACKGROUND_COLOR = "#B7B0AA"
GAME_SPEED = 300  # Update frequency in ms

class Snake:
    def __init__(self, color, start_x, start_y, direction):
        self._color = color
        self._coordinates = []
        self._circles = []
        self._direction = direction

        self._coordinates.append((start_x, start_y))

        for x, y in self._coordinates:
            circle = canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=self._color, outline="black")
            self._circles.append(circle)


def next_turn(snake):
    x, y = snake._coordinates[0]

    if snake._direction == "up": 
        y -= SPACE_SIZE
    elif snake._direction == "right":
        x += SPACE_SIZE
    elif snake._direction == "down":
        y += SPACE_SIZE
    elif snake._direction == "left":
        x -= SPACE_SIZE

    snake._coordinates.insert(0, (x,y))
    circle = canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=snake._color, outline="black")
    snake._circles.insert(0, circle)

    if check_collisions(snake):
        game_over(snake)
        
    else:
        window.after(GAME_SPEED, next_turn, snake)

def change_direction(snake, new_direction):

    if new_direction == snake._direction:
        return
    
    if new_direction == "up":
        if snake._direction != "down":
            snake._direction = new_direction
    elif new_direction == "right":
        if snake._direction != "left":
            snake._direction = new_direction
    elif new_direction == "down":
        if snake._direction != "up":
            snake._direction = new_direction
    elif new_direction == "left":
        if snake._direction != "right":
            snake._direction = new_direction

def check_collisions(snake):
    
    x, y = snake._coordinates[0]

    if x < 0 or x >= WINDOW_WIDTH:
        print("game over")
        return True
    elif y < 0 or y >= WINDOW_HEIGHT:
        print("game over")
        return True
    
    for body_part in snake._coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            print("game over")
            return True

    return False

def game_over(snake):
    for circle in snake._circles:
        canvas.itemconfig(circle, fill="gray")
    pass

window = Tk()
window.title("PvP Snake")
window.resizable(False, False)

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=WINDOW_HEIGHT, width=WINDOW_WIDTH)
canvas.pack()

window.bind("<Up>", lambda event: change_direction(snake, "up"))
window.bind("<Right>", lambda event: change_direction(snake, "right"))
window.bind("<Down>", lambda event: change_direction(snake, "down"))
window.bind("<Left>", lambda event: change_direction(snake, "left"))

snake = Snake("red", SPACE_SIZE * 4, SPACE_SIZE * 4, "down")

next_turn(snake)

window.mainloop()


