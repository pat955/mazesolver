from tkinter import Tk, BOTH, Canvas

def main():
    win = Window(800, 800)
    c = Cell(0, 0, 100, 100, win)
    c.draw()

    win.wait_for_close()

class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.canvas = Canvas(self.__root, bg="white", height=height, width=width)
        self.canvas.pack()
        self.__running = False

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()
        print("Window closed...")

    def draw_line(self, line, fill_color="black"):
        line.draw(self.canvas, fill_color)

    def close(self):
        self.__running = False


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas, fill_color="black"):
        canvas.create_line(
            self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=2
        )
        canvas.pack()

class Cell:
    def __init__(self, x1, y1, x2, y2, win):
        self.left = True
        self.right = True
        self.top = True
        self.bottom = True
        self.x1 = x1
        self.y1 = y1 
        self.x2 = x2
        self.y2 = y2
        self.win = win
    
    def draw(self):
        canvas = self.win.canvas
        if self.left:
            Line(Point(self.x2, self.y2), Point(self.x2, self.y1)).draw(canvas)
        if self.right:
            Line(Point(self.x1, self.y1), Point(self.x1, self.y2)).draw(canvas)
        if self.top:
            Line(Point(self.x1, self.y2), Point(self.x2, self.y2)).draw(canvas)
        if self.bottom:
            Line(Point(self.x1, self.y1), Point(self.x2, self.y1)).draw(canvas)


main()