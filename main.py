import time 
import random
import tkinter
import os
from functools import partial
from tkinter import Tk, BOTH, Canvas, Button, Frame, Entry, Label

# Add documentation 
# Add more interaction
# Clean code up----------------------------------------------
# Add customization, rows, columns, speed
# make the maze resize according to size
# Fix error when force quitting
# Function queue
# move window, cell, point and line to another file for cleanliness

def main():
    win = Window(900, 900)
    

class Window:
    def __init__(self, width, height):
        # Main variables
        self.__running = False
        self.__root = Tk()
        self.__root.bg = 'white'
        self.__root.title("Maze Solver")
        self.__root.configure(background='white')
        self.__root.protocol("WM_DELETE_WINDOW", self._quit)
        self.__root.attributes('-zoomed', True)
        self.__root.columnconfigure(0, weight=1)
        self.__root.columnconfigure(1, weight=0)
        self.__root.rowconfigure(0, weight=1)
        self.current_maze = None

        # self.maze_settings = {self.current_maze.rows:25, self.current_maze.colums:45, self.current_maze.cell_size:0, self.current_maze.slow_undo:0}
        # Frames, canvas:
        self.main_frame = Frame(self.__root, bg='white')
        self.main_frame.grid(column=0, row=0, sticky="nsew")
        
        self.option_frame = Frame(self.__root, bg='white')
        self.option_frame.grid(column=1, row=0, sticky="ens")
    
        self.canvas = Canvas(self.main_frame, bg="white")
        self.canvas.pack(fill='both', expand=True)
        
        # Buttons and labels:
        self.run_button = Button(self.option_frame, text='Run Maze', bg='lavender', command=self.run_and_solve_maze)
        self.run_button.pack(side="top", fill="x", pady=10)

        #self.rerun_button = Button(self.option_frame, text='Rerun', bg='lavender', command=self.rerun)
        #self.rerun_button.pack(side="top", fill="x")
        self.previous_button = Button(self.option_frame, text='Previous Maze', bg='lavender', command=self.previous)
        self.previous_button.pack(side="top", fill="x")

        #self.save_button = Button(self.option_frame, text='Save Maze', bg='lavender', command=self.save_maze)
        #self.save_button.pack(side="top", fill="x", pady=10)

        #self.speed_up_button = 
        
        # self.speed_button = 0
        # self.enable_slow_undo_button = Button(self.option_frame, text='Enable slow undo')
        """
        self.pause_button = Button(self.option_frame, text='Pause', bg='lavender', command=self.pause)
        self.pause_button.pack(side="top", fill="x", pady='5')
        self.unpause_button = Button(self.option_frame, text='Unpause', bg='lavender', command=self.unpause)
        """
        #self.unpause_button.pack(side="top", fill="x", pady='5')
        
        
        self.seed_label = Label(self.option_frame, text='Seed', bg='white')
        self.seed_label.pack(side="top", fill="x")
        
        self.seed_entry = Entry(self.option_frame, bg='lavender')
        self.seed_entry.pack(side="top", fill="x")
        #rows and columns
        self.rows_label = Label(self.option_frame, text='Rows', bg='white')
        self.rows_label.pack(side="top", fill="x")
        self.rows_entry = Entry(self.option_frame, bg='lavender')
        self.rows_entry.pack(side='top', fill='x')

        self.columns_label = Label(self.option_frame, text='Columns', bg='white')
        self.columns_label.pack(side="top", fill="x")
        self.columns_entry = Entry(self.option_frame, bg='lavender')
        self.columns_entry.pack(side="top", fill="x")

        
        self.__root.mainloop()
        
        #self.skip_button = Button(self.option_frame, text='Skip', bg='lavender', command=skip)
        
        #self.__root.bind("<Configure>", self.resize)
        """
        excess parts, no longer needed, but could be useful:
        #self.reset_button = Button(self.option_frame, text='Reset', bg='lavender', command=self.reset_maze)    
        #self.reset_button.pack(side="top", fill="x")
        #self.exit_button = Button(self.option_frame, text='Force quit', bg='lavender', command=self._quit)
        #self.exit_button.pack(side="top", fill="x")
        """

    def redraw(self):
        # Updates the screen to match whats happening
        self.__root.update_idletasks()
        self.__root.update()


    def draw_line(self, line, fill_color="black"):
        line.draw(self.canvas, fill_color)


    def _quit(self):
        # Force quits, error: _tkinter.TclError: invalid command name ".!frame.!canvas"
        if os.path.exists('cache.txt'):
            os.remove('cache.txt')
        self.__running = False
        self.__root.quit()
        self.__root.destroy()


    def previous(self):
        if os.path.exists('cache.txt'):
            with open('cache.txt', 'r') as file:
                l = file.readlines()
                try:
                    rows, columns, cell_x, cell_y = [char.strip(',') for char in l[-2].split()]
                except:
                    rows, columns, cell_x, cell_y = [char.strip(',') for char in l[0].split()]
                self.current_maze = Maze(int(rows), int(columns), int(cell_x), int(cell_y), self)
                print(self.current_maze)
        else:
            self.error_message('No saved mazes')
        self.run_and_solve_maze(True)


    def save_maze(self):  
        with open('cache.txt', 'a+') as file:
            try:
                if self.current_maze is not None:
                    maze_str = ', '.join([str(self.current_maze.rows), str(self.current_maze.columns), str(self.current_maze.cell_x), str(self.current_maze.cell_y)])
                    file.write(maze_str + '\n')
            except TypeError:
                #self.error_message('No maze to save!')
                pass


    def error_message(self, error_text):
        T = tkinter.Label(self.canvas, text=f'Error: {error_text}', bg='white', font='Calibri 15')
        T.pack(side='bottom')
    
        

    def run_and_solve_maze(self, prev=False):
        if not prev:
            rows, columns, cell_x, cell_y = self.resize_cells()
        
        if self.current_maze is None:
            self.current_maze = Maze(rows, columns, cell_x, cell_y, self)      
        
        if self.current_maze.running == False:
            
            self.canvas.delete(tkinter.ALL)
            if not prev:
                self.current_maze = Maze(rows, columns, cell_x, cell_y, self)
            self.current_maze.running = True
            self.current_maze.create_cells()
            self.current_maze.break_enterance_and_exit_walls()
            self.current_maze.break_walls_r(0, 0)
            self.current_maze.reset_cells_visited()
            self.current_maze.solve()
            self.current_maze.running = False
        self.save_maze()
        

    def resize_cells(self):

        rows = 25
        columns = 45
        cell_x = 35
        cell_y = 35
        
        try:
            rows = int(self.rows_entry.get())
            if rows > 27:
                while rows*cell_y > 945:
                    if cell_y > 2:
                        cell_y -=1
                    else:
                        break
        except:
            pass
        try:
            columns = int(self.columns_entry.get())
            if columns > 48:
                while columns*cell_x > 1680:
                    if cell_x > 2:
                        cell_x -=1
                    else:
                        break
        except:
            pass    
        return rows, columns, cell_x, cell_y
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
    def __init__(self, rows, columns, cell_x, cell_y, win):
        self.running = False
        self.x = 20
        self.y = 0
        self.rows = rows
        self.columns = columns
        self.cell_x = cell_x
        self.cell_y = cell_y
        self.win = win
        self.cells = []
        self.slow_undo = False
        self.paused = False
        random.seed(self.win.seed_entry.get())
    
    def __repr__(self):
        return f'{self.rows}, {self.columns}, {self.cell_x}, {self.cell_y}'


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
        """
        Tries to check each direction for cells.
        :param: (i, j) coordinates for current cell. 
        :return: lst, all UNVISITED adjecent cells
        """
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
        """
        Finds adjecent cells and if its open returns as list of valid cells
        :param: (i, j) coordinates for current cell
        :return: valid(open) cells.
        """
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
        """
        recursive function to go through the maze, depth first search.
        Starts by animating itself from its previous action. Visits current cell.
        for each open adjecent cell check if it has been visited. if not draw and recursivelly move to cell.
        else undo.
        :param: (i, j) coordinates for current cell
        :return: bool, if solvable True, else False but all my mazes are solvable :)
        """
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
                    if self.slow_undo:
                        self.animate(0.01)# for slow undo
        return False

    def create_cells(self):
        self.cells = []
        cell_x, cell_y = self.x, self.y
        for i in range(self.rows):   
            for j in range(self.columns):
                if j % self.columns == 0 :
                    self.cells.append([])
                    cell_y += self.cell_y
                    cell_x = self.x
                self.cells[i].append(Cell(cell_x, cell_y, cell_x + self.cell_x, cell_y + self.cell_y, self.win))
                cell_x += self.cell_x
        for row in self.cells:
            for cell in row:
                cell.draw()
                self.animate(0.00001)
                
    
    def animate(self, sleep_time=0.005):
        while self.paused:
            sleep(0.01)
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