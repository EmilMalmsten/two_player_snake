from tkinter import *

WINDOW_HEIGHT = 800
WINDOW_WIDTH = 800
SPACE_SIZE = 25
BACKGROUND_COLOR = "#B7B0AA"
GAME_SPEED = 300  # Update frequency in ms
COUNTDOWN_LENGTH = 3 # seconds

class Snake:
    def __init__(self, color, start_x, start_y, direction):
        self._start_x = start_x
        self._start_y = start_y
        self._color = color
        self._start_direction = direction
        self.direction = direction
        self.coordinates = []
        self.circles = []
        self.ready = False
        self.crashed = False
        self.insert_head(start_x, start_y)

    def insert_head(self, x, y):
        self.coordinates.insert(0, (x, y))
        circle = canvas.create_oval(
                x,
                y,
                x + SPACE_SIZE,
                y + SPACE_SIZE,
                fill=self._color,
                outline="black",
                tag="snake_body"
                )
        self.circles.append(circle)

    def reset_state(self):
        self.coordinates = []
        self.circles = []
        self.ready = False
        self.crashed = False
        self.direction = self._start_direction
        self.insert_head(self._start_x, self._start_y)


def countdown(count):
    canvas.itemconfig("countdown_text", text=f"{count}")

    if count > 0:
        window.after(1000, countdown, count-1)
    else:
        canvas.delete("countdown_text")
        next_turn(snakes)

def ready(snake, tag):
    snake.ready = True
    canvas.delete(tag)
    
    if all(snake.ready == True for snake in snakes):
        countdown_text = canvas.create_text(
                350, 350, 
                text="",
                tag="countdown_text",
                )
        canvas.pack()
        countdown(COUNTDOWN_LENGTH)

def next_turn(snakes):

    if snakes[0].ready == False or snakes[1].ready == False:

        canvas.create_text(
                SPACE_SIZE * 5, SPACE_SIZE * 3, 
                text="Player 1 - Press 'W' when ready",
                tag="p1_ready",
                )

        canvas.create_text(
                WINDOW_WIDTH - SPACE_SIZE * 5, WINDOW_HEIGHT - SPACE_SIZE * 3, 
                text="Player 2 - Press 'Up Arrow' when ready",
                tag="p2_ready",
                )
        canvas.pack()

        window.bind("<w>", lambda event: ready(snakes[0], "p1_ready"))
        window.bind("<Up>", lambda event: ready(snakes[1], "p2_ready"))


    else:
        # both players ready and game started

        # snake one keybindings
        window.bind("<w>", lambda event: change_direction(snakes[0], "up"))
        window.bind("<d>", lambda event: change_direction(snakes[0], "right"))
        window.bind("<s>", lambda event: change_direction(snakes[0], "down"))
        window.bind("<a>", lambda event: change_direction(snakes[0], "left"))

        # snake two keybindings
        window.bind("<Up>", lambda event: change_direction(snakes[1], "up"))
        window.bind("<Right>", lambda event: change_direction(snakes[1], "right"))
        window.bind("<Down>", lambda event: change_direction(snakes[1], "down"))
        window.bind("<Left>", lambda event: change_direction(snakes[1], "left"))

        # add new head to snake in current direction
        for snake in snakes:
            x, y = snake.coordinates[0]

            if snake.direction == "up": 
                y -= SPACE_SIZE
            elif snake.direction == "right":
                x += SPACE_SIZE
            elif snake.direction == "down":
                y += SPACE_SIZE
            elif snake.direction == "left":
                x -= SPACE_SIZE

            snake.coordinates.insert(0, (x,y))
            circle = canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=snake._color, outline="black", tag="snake_body")
            snake.circles.insert(0, circle)

            if check_collisions(snake):
                snake.crashed = True

        # both snakes crashed at the same time (tie)
        if snakes[0].crashed and snakes[1].crashed:
            game_over(snakes)
            window.after(3000, reset_game, snakes)
        elif snakes[0].crashed:
            game_over([snakes[0]])
            window.after(3000, reset_game, snakes)
        elif snakes[1].crashed:
            game_over([snakes[1]])
            window.after(3000, reset_game, snakes)
        else:
            window.after(GAME_SPEED, next_turn, snakes)

def change_direction(snake, new_direction):

    if new_direction == snake.direction:
        return
    
    if new_direction == "up":
        if snake.direction != "down":
            snake.direction = new_direction
    elif new_direction == "right":
        if snake.direction != "left":
            snake.direction = new_direction
    elif new_direction == "down":
        if snake.direction != "up":
            snake.direction = new_direction
    elif new_direction == "left":
        if snake.direction != "right":
            snake.direction = new_direction

def check_collisions(snake):

    x, y = snake.coordinates[0]

    if x < 0 or x >= WINDOW_WIDTH:
        return True
    elif y < 0 or y >= WINDOW_HEIGHT:
        return True
    
    # Check if head of current snake is somewhere inside body of snake one
    if snake.coordinates[0] in snakes[0].coordinates[1:]:
        return True
    # Check if head of current snake is somewhere inside body of snake two
    if snake.coordinates[0] in snakes[1].coordinates[1:]:
        return True

    return False

def reset_game(snakes):
    canvas.delete("snake_body")
    for snake in snakes:
        snake.reset_state()
    next_turn(snakes)

def game_over(snakes):
    for snake in snakes:
        for circle in snake.circles:
            canvas.itemconfig(circle, fill="gray")

window = Tk()
window.title("PvP Snake")

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=WINDOW_HEIGHT, width=WINDOW_WIDTH)
#window.resizable(False, False)

label = Label(window, text="Snake game")
label.pack()

snakes = []
snakes.append(Snake("red", SPACE_SIZE * 4, SPACE_SIZE * 4, "down"))
snakes.append(Snake("blue", WINDOW_HEIGHT - SPACE_SIZE * 4, WINDOW_WIDTH - SPACE_SIZE * 4, "up"))
    
next_turn(snakes)

window.mainloop()

