import time 
import random 
from cell import Cell

class Game:
    def __init__(
            self,
            x1,
            y1,
            num_rows,
            num_cols,
            cell_size_x,
            cell_size_y,
            win=None,
            seed=None
        ):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._seed = seed

        if self._seed is not None:
            self._random = random.seed(seed)

        self._create_grid()

    def _create_grid(self):
        self._cells = []
        for i in range(self._num_cols):
            column_list = []
            for j in range(self._num_rows):

                cell = Cell(self._win)

                cell._x1 = self._x1 + i * self._cell_size_x
                cell._y1 = self._y1 + j * self._cell_size_y

                cell._x2 = cell._x1 + self._cell_size_x
                cell._y2 = cell._y1 + self._cell_size_y

                column_list.append(cell)

            self._cells.append(column_list)

        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._color_cell(i, j)


    def _color_cell(self, i, j):
        if self._win is None:
            raise Exception("No window object in game class")
        self._cells[i][j]._color()



