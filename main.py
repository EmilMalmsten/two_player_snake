from graphics import Window
from game import Game

def main():
    window_width = 800
    window_height = 800
    window = Window(window_width, window_height)

    start_x = 100
    start_y = 100
    num_cols = 50
    num_rows = 50
    cell_size_x = 10
    cell_size_y = 10

    game = Game(start_x, start_y, num_cols, num_rows, cell_size_x, cell_size_y, window)

    window.run()

main()


