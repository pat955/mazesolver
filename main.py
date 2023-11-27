import time 
from tkinter import Tk, BOTH, Canvas

def main():
    window_x = 800
    window_y = 800
    win = Window(window_x, window_y)

    maze = Maze(20, 20, 16, 40, win)
    
    maze.create_cells()
    win.wait_for_close()

class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.canvas = Canvas(self.__root, bg="white", height=height, width=width)
        self.canvas.pack(expand=1)
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
        canvas.pack(expand=1)

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

    def draw_move(self, to_cell, undo=False):
        start = Point(self.x2/2, self.y2/2)
        end = Point(to_cell.x2/1.25, to_cell.y2/2)
        Line(start, end).draw(self.win.canvas, 'red')

class Maze:
    def __init__(self, x, y, grid_num, cell_size, win):
        self.x = x
        self.y = y
        self.grid_num = grid_num
        self.cell_size = cell_size
        self.win = win
        self.cells = []

    def create_cells(self):
        cell_x, cell_y = self.x, self.y
        for i in range(self.grid_num**2):
            if i % self.grid_num == 0 :
                cell_y += self.cell_size
                cell_x = self.x
        
            self.cells.append(Cell(cell_x, cell_y, cell_x + self.cell_size, cell_y + self.cell_size, self.win))
            cell_x += self.cell_size
        if len(self.cells) != self.grid_num**2:
            print(len(self.cells), grid_num)
        for cell in self.cells:
            cell.draw()
            self.animate()
    
    def animate(self):
        self.win.redraw()
        time.sleep(0.01)
 
main()