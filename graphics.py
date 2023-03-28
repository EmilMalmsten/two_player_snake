from tkinter import Tk, BOTH, Canvas

class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Snake")
        self.__canvas = Canvas(self.__root, bg="white", height=height, width=width)
        self.__canvas.pack(fill=BOTH, expand=1)

    def run(self):
        self.__root.mainloop()

    def redraw(self):
        self.__canvas.update_idletasks()

    def color_cell(self, circle, fill_color="red"):
        #self.__canvas.create_oval(100, 100, 200, 200, fill='red')

        circle.draw(self.__canvas, fill_color)

class Circle:
    def __init__(self, x1, y1, x2, y2):
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2

    def draw(self, canvas, fill_color="red"):
        canvas.create_oval(self._x1, self._y1, self._x2, self._y2, fill=fill_color)
        canvas.pack()



