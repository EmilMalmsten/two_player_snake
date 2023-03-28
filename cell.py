from graphics import Circle

class Cell:
    def __init__(self, _win=None):
        self._x1 = None
        self._x2 = None
        self._y1 = None
        self._y2 = None
        self._win = _win
        self.visited = False

    def _color(self, fill_color='red'):
        self._win.color_cell(Circle(self._x1, self._y1, self._x2, self._y2))


