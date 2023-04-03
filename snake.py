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

# After both players are ready, start a countdown to start the game
def countdown(count):
    canvas.itemconfig("countdown_text", text=f"{count}")

    if count > 0:
        window.after(1000, countdown, count-1)
    else:
        canvas.delete("countdown_text")
        next_turn(snakes)

# This function gets called whenever a player presses their respective ready button before a game
def ready(snake, tag):
    snake.ready = True
    # delete the ready text instructions for the player that pressed ready
    canvas.delete(tag)
    
    if all(snake.ready == True for snake in snakes):
        # re-bind the up key to movement
        window.bind("<w>", lambda event: snakes[0].change_direction("up"))
        window.bind("<Up>", lambda event: snakes[1].change_direction("up"))
        countdown_text = canvas.create_text(
                CANVAS_WIDTH / 2,
                CANVAS_HEIGHT / 2, 
                text="",
                tag="countdown_text",
                font=("TkDefaultFont", 30)
                )
        canvas.pack()
        countdown(COUNTDOWN_LENGTH)

# This function will be called recursively with a set delay between each called defined by
# the GAME_SPEED variable (as long as there are no collisions)
def next_turn(snakes):

    if snakes[0].ready == False or snakes[1].ready == False:

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

        # Change the up key to act as a ready check
        window.bind("<w>", lambda event: ready(snakes[0], "p1_ready"))
        window.bind("<Up>", lambda event: ready(snakes[1], "p2_ready"))


    else:
        # both players ready and game started

        # add new head to snake in the current direction
        for snake in snakes:
            snake.move()

            if check_collisions(snake):
                snake.crashed = True

        # logic to see who the winner is if there were any crashes
        if snakes[0].crashed and snakes[1].crashed:
            game_over(snakes)
            window.after(3000, reset_game, snakes)
        elif snakes[0].crashed:
            winner = snakes[1]
            game_over([snakes[0]], winner)
            window.after(3000, reset_game, snakes)
        elif snakes[1].crashed:
            winner = snakes[0]
            game_over([snakes[1]], winner)
            window.after(3000, reset_game, snakes)
        else:
            # recursively call itself for the next turn if there were no crashes
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

def reset_game(snakes):
    canvas.delete("snake_body")
    canvas.delete("winner_text")
    for snake in snakes:
        snake.reset_state()
    next_turn(snakes)

def game_over(snakes, winner=None):
    for snake in snakes:
        for circle in snake.circles:
            canvas.itemconfig(circle, fill="gray")

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
    else:
        canvas.itemconfig("winner_text", text="It's a tie!")


window = Tk()
window.title("PvP Snake")
window.resizable(False, False)

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=CANVAS_HEIGHT, width=CANVAS_WIDTH)
canvas.pack()

frame = Frame(window)
frame.pack()

text1 = Text(frame, height=10, width=30)
text1.pack(side=LEFT)

text2 = Text(frame, height=10, width=30)
text2.pack(side=LEFT)

text1.insert(END, "Player 1 Controls:\n")
text1.insert(END, "\n")
text1.insert(END, "W - Move up\n")
text1.insert(END, "A - Move left\n")
text1.insert(END, "S - Move down\n")
text1.insert(END, "D - Move right\n")
    
text2.insert(END, "Player 2 Controls:\n")
text2.insert(END, "\n")
text2.insert(END, "Up arrow - Move up\n")
text2.insert(END, "Left arrow - Move left\n")
text2.insert(END, "Down arrow - Move down\n")
text2.insert(END, "Right arrow - Move right\n")

snakes = []
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

next_turn(snakes)

window.mainloop()

