import time 
import random
from tkinter import Tk, BOTH, Canvas

def main():
    window_x = 800
    window_y = 800
    win = Window(window_x, window_y)

    maze = Maze(10, 10, 10, 40, win, random.seed(0))
   
    maze.create_cells()
    maze.break_enterance_and_exit_walls()
    maze.break_walls_r(0, 0)
    win.wait_for_close()

DIRECTIONS = ['top', 'right', 'left', 'bottom']

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
    def __init__(self, x1, y1, x2, y2, win=None):
        self.left = True
        self.right = True
        self.top = True
        self.bottom = True
        self.x1 = x1
        self.y1 = y1 
        self.x2 = x2
        self.y2 = y2
        self.win = win
        self.visited = False

    def __repr__(self):
        return '!'
        #return f'|({self.x1}, {self.y1}), ({self.x2}, {self.y2})|'

    def draw(self, color='black'):
        canvas = self.win.canvas
        if self.left:
            Line(Point(self.x1, self.y1), Point(self.x1, self.y2)).draw(canvas, color)
        else:
            Line(Point(self.x1, self.y1), Point(self.x1, self.y2)).draw(canvas,'white')

        if self.right:
            Line(Point(self.x2, self.y1), Point(self.x2, self.y2)).draw(canvas)
        else:
            Line(Point(self.x2, self.y1), Point(self.x2, self.y2)).draw(canvas, 'white') 

        if self.top:
            Line(Point(self.x1, self.y1), Point(self.x2, self.y1)).draw(canvas, color)
        else:
            Line(Point(self.x1, self.y1), Point(self.x2, self.y1)).draw(canvas, 'white')

        if self.bottom:
            Line(Point(self.x1, self.y2), Point(self.x2, self.y2)).draw(canvas, color)
        else:
            Line(Point(self.x1, self.y2), Point(self.x2, self.y2)).draw(canvas, 'white')

    def draw_move(self, to_cell, undo=False):
        start = Point(self.x2/2, self.y2/2)
        end = Point(to_cell.x2/1.25, to_cell.y2/2)
        Line(start, end).draw(self.win.canvas, 'red')
            

class Maze:
    def __init__(self, x, y, grid_num, cell_size, win=None, seed=None):
        self.x = x
        self.y = y
        self.grid_num = grid_num
        self.cell_size = cell_size
        self.win = win
        self.cells = []
        self.seed = seed

    def break_enterance_and_exit_walls(self):
        first_cell = self.cells[0][0]
        first_cell.top = False
        first_cell.draw()

        exit_cell = self.cells[-1][-1]
        exit_cell.bottom = False
        exit_cell.draw()
    def break_walls_r(self, i, j):
        self.cells[i][j].visited = True
        while True:
            to_visit = []
            possible_directions = self.find_adjecent(i, j)
            if possible_directions == []:
                self.cells[i][j].draw('red')
                return
            adjecent_values = [(0, -1), (0,1), ]
            chosen_direction_info = random.choice(possible_directions)
            self.break_walls_between_two_cells(self.cells[i][j], chosen_direction_info)
            self.break_walls_r()

    def find_adjecent(self, i, j):
        directions = {'top': (0, -1), 'right': (1, 0), 'left': (-1, 0), 'bottom': (0, 1)}
        possible_directions = []
        for direction, values in directions:
            try:
                if i + values[0] >= 0 and j + values[1] >= 0:
                    possible_directions.append((direction, self.cells[i + values[0][j + values[1]]]))
        return [info for info in possible_directions if info[1].visited == False]

    def break_walls_r(self, to_visit, current_cell):
        current_cell.visited = True
        while True:
            to_visit = []
            to_visit.append(self.find_adjecent)
            possible_directions = self.find_adjecent(current_cell)
            if possible_directions == []:
                current_cell.draw()
                self.animate()
                return
            for direction in possible_directions:
                direction[1].draw('pink')
                self.animate()
            chosen_direction = random.choice(possible_directions)
            new_cell = chosen_direction[1]
            self.break_walls_between_two(current_cell, chosen_direction)
            self.break_walls_r(to_visit, new_cell)

    def break_walls_between_two_cells(self, current_cell, direction_info):
        direction = direction_info[0]
        chosen_cell = direction_info[1]
        if direction == 'top':
            current_cell.top= False
            chosen_cell.bottom = False
        elif direction == 'right':
            current_cell.right = False
            chosen_cell.left = False
        elif direction == 'left':
            current_cell.left = False
            chosen_cell.right = False
        elif direction == 'bottom':
            current_cell.bottom = False
            current_cell.top = False
        else:
            print('Something went wrong!')

    def find_adjecent(self, target_cell):
        directions = {'top': (-1, 0), 'right': (0, 1), 'left': (0, -1), 'bottom': (1, 0)}
        adjecent = []
        i_row = -1
        for row in self.cells:
            i_row += 1
            i = -1
            for cell in row:
                i += 1
                if cell == target_cell:
                    for direction, val in directions.items():
                        try:
                            new_row = i_row + val[0]
                            new_i = i + val[1]
                            if new_i >= 0 and new_row >= 0:
                                adjecent.append((direction, self.cells[new_i][new_row]))
                        except:
                            continue
        return [info for info in adjecent if info[1].visited == False]

    def reset_cells_visited(self):
        for row in self.cells:
            for cell in row:
                cell.visited = False

    def create_cells(self):
        cell_x, cell_y = self.x, self.y

        for i in range(self.grid_num):   
            for j in range(self.grid_num):
                if j % self.grid_num == 0 :
                    self.cells.append([])
                    cell_y += self.cell_size
                    cell_x = self.x
                
                self.cells[i].append(Cell(cell_x, cell_y, cell_x + self.cell_size, cell_y + self.cell_size, self.win))
                cell_x += self.cell_size

        for row in self.cells:
            for cell in row:
                cell.draw()
                
    
    def animate(self):
        self.win.redraw() 
        time.sleep(0.4)
 
main()