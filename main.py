from tkinter import Tk, BOTH, Canvas


def main():
    win = Window(800, 600)
    l = Line(Point(50, 50), Point(400, 400))
    win.draw_line(l, "black")
    win.wait_for_close()
  

class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title = ('Maze Solver')
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.canvas = Canvas(self.__root, bd=width, height=height, bg='white')
        self.canvas.pack()
        self.__running = False

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()
        print("window closed...")
    
    def close(self):
        self.__running = False

    def draw_line(self, line, color='black'):
        line.draw(self.canvas, color)
     

class Point:
    def __init__(self, x, y):
        self.x = x 
        self.y = y 

class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
    
    def draw(self, canvas, color):
        canvas.create_line(
            self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=color, width=5
        )
        canvas.pack()

class Cell:
    def __init__(self, x1, y1, x2, y2, win):
        self.left_wall = True 
        self.right_wall = True
        self.top_wall = True
        self.bottom_wall = True
        self.walls = [
            self.left_wall, self.right_wall, self.top_wall, self.bottom_wall
        ]
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.win = win
        
    def draw(self):
        if self.left_wall == True:
            l = Line(Point(self.x2, self.y1), Point(self.x1, self.y2))
            l.draw(self.win.canvas, 'black')

    
main()