import time 
import random
import tkinter
from tkinter import Tk, BOTH, Canvas, Button, Frame, Entry

# Figure out how to close window while it animates
# Add documentation 
# Add more interaction
# Clean code up

def main():
    win = Window(900, 900)
    win.wait_for_close()

class Window:
    def __init__(self, width, height):

        self.__root = Tk()
        self.__root.bg = 'white'
        self.__root.title("Maze Solver")
        self.__root.configure(background='white')
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__root.attributes('-zoomed', True)
        self.__root.columnconfigure(0, weight=1)
        self.__root.columnconfigure(1, weight=0)
        self.__root.rowconfigure(0, weight=1)
     

        self.main_frame = Frame(self.__root, bg='white')
        self.main_frame.grid(column=0, row=0, sticky="nsew")
        
        self.option_frame = Frame(self.__root, bg='white')
        self.option_frame.grid(column=1, row=0, sticky="ens")
    
        self.canvas = Canvas(self.main_frame, bg="white")
        self.canvas.pack(fill='both', expand=True)
        
        self.__running = False
        
        self.exit_button = Button(self.option_frame, text='Force quit', bg='lavender', command=self._quit)
        self.exit_button.pack(side="top", fill="x")

        self.run_button = Button(self.option_frame, text='Run Maze', bg='lavender', command=self.run_and_solve_maze)
        self.run_button.pack(side="top", fill="x", pady='10')

        self.reset_button = Button(self.option_frame, text='Reset', bg='lavender', command=self.reset_maze)    
        self.reset_button.pack(side="top", fill="x")

        self.seed_entry = Entry(self.option_frame, text='Seed', bg='lavender')
        self.seed_entry.pack(side="top", fill="x", pady='10')
        random.seed(self.seed_entry.get())

        
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
    

    def _quit(self):
        self.__running = False
        self.__root.quit()
        self.__root.destroy()


    def run_and_solve_maze(self):
        maze = Maze(25, 45, 35, self)
        maze.create_cells()
        maze.break_enterance_and_exit_walls()
        maze.break_walls_r(0, 0)
        maze.reset_cells_visited()
        maze.solve()


    def reset_maze(self):
        self.canvas.delete('all')

    def enter_seed(self, seed):
        random.seed(seed)

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
        canvas.pack(fill='both', expand=True)


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
        return f'|({self.x1}, {self.y1}), ({self.x2}, {self.y2})|'

    def draw(self, color='black'):
        canvas = self.win.canvas
        walls = [
            (self.left, Line(Point(self.x1, self.y1), Point(self.x1, self.y2))),
            (self.right, Line(Point(self.x2, self.y1), Point(self.x2, self.y2))),
            (self.top, Line(Point(self.x1, self.y1), Point(self.x2, self.y1))),
            (self.bottom, Line(Point(self.x1, self.y2), Point(self.x2, self.y2)))
            ]

        for wall, line in walls:
            if wall:
                line.draw(canvas, color)
            else:
                line.draw(canvas, 'white')


    def draw_move(self, to_cell, direction, undo=False):
        x1, x2, y1, y2 = self.x1, self.x2, self.y1, self.y2
        directions = {
            (0, 1): (((x2 - x1)/2 + x1, (y2 - y1)/2 + y1), ((x2 - x1)/2 + x2, (y2 - y1)/2+ y1)),
            (0, -1): ((x1 - (x2 - x1)/2, (y2 - y1)/2 + y1), (x2 - (x2 - x1)/2, (y2 - y1)/2+ y1)),

            (-1, 0): (((x2 - x1)/2 + x1, y1-(y2 - y1)/2), ((x2 - x1)/2 + x1, y2- (y2 - y1)/2 )),
            (1, 0): (((x2 - x1)/2 + x1, (y2 - y1)/2 + y1), ((x2 - x1)/2 + x1, (y2 - y1)/2 + y2))
        }
        recipe = directions[direction]

        if undo:
            start = Point(recipe[0], recipe[1])
            end = Point(recipe[0], recipe[1])
            self.win.draw_line(Line(start, end), 'gray')
        else:
            start = Point(recipe[0], recipe[1])
            end = Point(recipe[0], recipe[1])
            self.win.draw_line(Line(start, end), 'red2')

class Maze:
    def __init__(self, rows, columns, cell_size, win):
        self.x = 20
        self.y = 0
        self.rows = rows
        self.columns = columns
        self.cell_size = cell_size
        self.win = win
        self.cells = []


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
            adjecent_cells = self.find_adjecent_cells(i, j)
            if adjecent_cells == []:
                self.cells[i][j].draw()
                return
            chosen_cell = random.choice(adjecent_cells)
            self.break_adjecent_walls(i, j, chosen_cell[0], chosen_cell[1])
            self.break_walls_r(i + chosen_cell[1][0], j + chosen_cell[1][1])        
            

    def break_adjecent_walls(self, i, j, chosen_cell, direction):
        current_cell = self.cells[i][j]
        if direction == (-1, 0):
            current_cell.top= False
            chosen_cell.bottom = False
        elif direction == (0, 1):
            current_cell.right = False
            chosen_cell.left = False
        elif direction == (0, -1):
            current_cell.left = False
            chosen_cell.right = False
        elif direction == (1, 0):
            current_cell.bottom = False
            chosen_cell.top = False
        
        self.cells[i][j].draw('pink')
        self.animate()


    def find_adjecent_cells(self, i, j):
        vals = [(-1, 0), (0, 1), (0, -1), (1, 0)]
        adjecent_cells = []
        for index in range(4):
            try:
                if i + vals[index][0] >= 0 and j + vals[index][1] >= 0:
                    adjecent_cells.append((self.cells[i + vals[index][0]][j + vals[index][1]], vals[index]))
            except:
                pass
        return [cell for cell in adjecent_cells if cell[0].visited == False]


    def find_open_adjecent_cells(self, i, j):
        valid_cells = []
        
        cells = self.find_adjecent_cells(i, j)
        for info in cells:
            cell, direction = info[0], info[1]

            if direction == (-1, 0):
                if not cell.bottom:
                    valid_cells.append((cell, direction))
            elif direction == (0, 1):
                if not cell.left:
                    valid_cells.append((cell, direction))
            elif direction == (0, -1):
                if not cell.right:
                    valid_cells.append((cell, direction))
            elif direction == (1, 0):
                if not cell.top:
                    valid_cells.append((cell, direction))
        return valid_cells


    def reset_cells_visited(self):
        for row in self.cells:
            for cell in row:
                cell.visited = False
    

    def solve(self):
        return self.solve_r(0, 0)


    def solve_r(self, i, j):
        self.animate()
        current_cell = self.cells[i][j]
        current_cell.visited = True
        if current_cell == self.cells[-1][-1]:
            return True
        valid_cells = self.find_open_adjecent_cells(i, j)
        for cell, direction in valid_cells:
            if not cell.visited:
                current_cell.draw_move(cell, direction)
                if self.solve_r(i+direction[0],j+direction[1]):
                    return True
                else:
                    current_cell.draw_move(cell, direction, True)
                    #self.animate(0.01)# for slow undo
        return False

    def create_cells(self):
        cell_x, cell_y = self.x, self.y
        for i in range(self.rows):   
            for j in range(self.columns):
                if j % self.columns == 0 :
                    self.cells.append([])
                    cell_y += self.cell_size
                    cell_x = self.x
                self.cells[i].append(Cell(cell_x, cell_y, cell_x + self.cell_size, cell_y + self.cell_size, self.win))
                cell_x += self.cell_size
        for row in self.cells:
            for cell in row:
                cell.draw()
                self.animate(0.00001)
                
    
    def animate(self, sleep_time=0.01):
        self.win.redraw()
        time.sleep(sleep_time)
        
 
main()

"""
IDEAS FOR EXTENDING THE PROJECT
Add other solving algorithms, like breadth-first search or A*
Make the visuals prettier, change the colors, etc
Mess with the animation settings to make it faster/slower. Maybe make backtracking slow and blazing new paths faster?
Add configurations in the app itself using Tkinter buttons and inputs to allow users to change maze size, speed, etc
Make much larger mazes to solve
Make it a game where the user chooses directions
If you made it a game, allow the user to race an algorithm
Make it 3 dimensional
Time the various algorithms and see which ones are the fastest
"""