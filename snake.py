from tkinter import *

# Game constants
CANVAS_HEIGHT = 600
CANVAS_WIDTH = 800
SPACE_SIZE = 20
BACKGROUND_COLOR = "#B7B0AA"
GAME_SPEED = 300  # Update frequency in ms
COUNTDOWN_LENGTH = 3 # seconds

class Snake:
    def __init__(self, color, start_x, start_y, direction, name):
        self._start_x = start_x
        self._start_y = start_y
        self._color = color
        self._name = name
        self._start_direction = direction
        self.direction = direction
        self.coordinates = []
        self.circles = []
        self.ready = False
        self.crashed = False
        self.score = 0
        self.insert_head(start_x, start_y)

    # Create the first part of the snake in the starting location
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

    def change_direction(self, new_direction):
        if new_direction == self.direction:
            return
        
        if new_direction == "up":
            if self.direction != "down":
                self.direction = new_direction
        elif new_direction == "right":
            if self.direction != "left":
                self.direction = new_direction
        elif new_direction == "down":
            if self.direction != "up":
                self.direction = new_direction
        elif new_direction == "left":
            if self.direction != "right":
                self.direction = new_direction

    def move(self):
        # unpack coordinates for current head
        x, y = self.coordinates[0]
        
        if self.direction == "up":
            y -= SPACE_SIZE
        elif self.direction == "right":
            x += SPACE_SIZE
        elif self.direction == "down":
            y += SPACE_SIZE
        elif self.direction == "left":
            x -= SPACE_SIZE

        # insert the new head
        self.coordinates.insert(0, (x,y))

        circle = canvas.create_oval(
                x,
                y,
                x + SPACE_SIZE,
                y + SPACE_SIZE,
                fill=self._color,
                outline="black",
                tag="snake_body")
        self.circles.insert(0, circle)

    # After each round, reset the snake for the next round
    def reset_state(self):
        self.coordinates = []
        self.circles = []
        self.ready = False
        self.crashed = False
        self.direction = self._start_direction
        self.insert_head(self._start_x, self._start_y)

# Game functions
def set_ready_instructions():
    window.bind("<w>", lambda event: ready(snakes[0], "p1_ready"))
    window.bind("<Up>", lambda event: ready(snakes[1], "p2_ready"))
    canvas.create_text(
            SPACE_SIZE * 5.5, SPACE_SIZE * 4.5, 
            text="Player 1 - Press 'W' when ready",
            tag="p1_ready",
            anchor="w"
            )

    canvas.create_text(
            CANVAS_WIDTH - SPACE_SIZE * 5.5, CANVAS_HEIGHT - SPACE_SIZE * 4.5, 
            text="Player 2 - Press 'Up Arrow' when ready",
            tag="p2_ready",
            anchor="e"
            )
    canvas.pack()

# This function gets called whenever a player presses their respective ready button before a game
def ready(snake, ready_text_tag):
    snake.ready = True
    # delete the ready text instructions for the player that pressed ready
    canvas.delete(ready_text_tag)
    ready_check()

def ready_check():
    if all(snake.ready == True for snake in snakes):
        countdown_text = canvas.create_text(
                CANVAS_WIDTH / 2,
                CANVAS_HEIGHT / 2, 
                text="",
                tag="countdown_text",
                font=("TkDefaultFont", 30)
                )
        canvas.pack()
        countdown(COUNTDOWN_LENGTH)

# After both players are ready, start a countdown to game start
def countdown(count):
    canvas.itemconfig("countdown_text", text=f"{count}")

    if count > 0:
        window.after(1000, countdown, count-1)
    else:
        canvas.delete("countdown_text")
        set_movement_controls()
        next_turn(snakes)

def set_movement_controls():
    # snake one keybindings
    window.bind("<w>", lambda event: snakes[0].change_direction("up"))
    window.bind("<d>", lambda event: snakes[0].change_direction("right"))
    window.bind("<s>", lambda event: snakes[0].change_direction("down"))
    window.bind("<a>", lambda event: snakes[0].change_direction("left"))

    # snake two keybindings
    window.bind("<Up>", lambda event: snakes[1].change_direction("up"))
    window.bind("<Right>", lambda event: snakes[1].change_direction("right"))
    window.bind("<Down>", lambda event: snakes[1].change_direction("down"))
    window.bind("<Left>", lambda event: snakes[1].change_direction("left"))

# next_turn will be called recursively with a set delay between each called defined by
# the GAME_SPEED variable (as long as there are no collisions)
def next_turn(snakes):
    # add new head to snake in the current direction
    for snake in snakes:
        snake.move()

        if check_collisions(snake):
            snake.crashed = True

    if any(snake.crashed == True for snake in snakes):
        game_over(snakes)
        window.after(3000, reset_game, snakes)

    else:
        window.after(GAME_SPEED, next_turn, snakes)

def check_collisions(snake):
    x, y = snake.coordinates[0]

    # check if head is outside of the canvas
    if x < 0 or x >= CANVAS_WIDTH:
        return True
    elif y < 0 or y >= CANVAS_HEIGHT:
        return True
    
    # Check if head of current snake is somewhere inside body of snake one
    if snake.coordinates[0] in snakes[0].coordinates[1:]:
        return True
    # Check if head of current snake is somewhere inside body of snake two
    if snake.coordinates[0] in snakes[1].coordinates[1:]:
        return True

    return False

def game_over(snakes):
    winner = None

    for snake in snakes:
        if snake.crashed:
            for circle in snake.circles:
                canvas.itemconfig(circle, fill="gray")
        else:
            winner = snake

    winner_text = canvas.create_text(
            CANVAS_WIDTH / 2,
            CANVAS_HEIGHT / 2, 
            text="",
            tag="winner_text",
            font=("TkDefaultFont", 30)
            )
    canvas.pack()

    if winner:
        canvas.itemconfig("winner_text", text=f"{winner._name} is the winner!")
        winner.score += 1
        player_one_score.config(text=f"Player 1 score: {snakes[0].score}")
        player_two_score.config(text=f"Player 2 score: {snakes[1].score}")
    else:
        canvas.itemconfig("winner_text", text="It's a tie!")

def reset_game(snakes):
    canvas.delete("snake_body")
    canvas.delete("winner_text")
    for snake in snakes:
        snake.reset_state()
    set_ready_instructions()

window = Tk()
window.title("PvP Snake")
window.resizable(False, False)
snakes = []

top_frame = Frame(window)
top_frame.pack(side=TOP, fill=BOTH, expand=True)

player_one_score = Label(top_frame, text=f"Player 1 score: 0", pady=10)
player_one_score.pack(side=LEFT, fill=BOTH, expand=True)

player_two_score = Label(top_frame, text=f"Player 2 score: 0", pady=10)
player_two_score.pack(side=LEFT, fill=BOTH, expand=True)

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=CANVAS_HEIGHT, width=CANVAS_WIDTH)
canvas.pack()

player_one_controls = Label(window, text="Player 1 - Use WASD keys to move", pady=10)
player_one_controls.pack(side=LEFT, fill=BOTH, expand=True)

player_two_controls = Label(window, text="Player 2 - Use arrow keys to move", pady=10)
player_two_controls.pack(side=LEFT, fill=BOTH, expand=True)

snakes.append(Snake(
    "#A91814", #color
    SPACE_SIZE * 4, # start x
    SPACE_SIZE * 4, # start y
    "down", # start direction
    "Red snake" # name
    ))
snakes.append(Snake(
    "#417cff",
    CANVAS_WIDTH - SPACE_SIZE * 5,
    CANVAS_HEIGHT - SPACE_SIZE * 5,
    "up",
    "Blue snake"
    ))

set_ready_instructions()
window.mainloop()

