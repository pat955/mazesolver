import time 
import random
import os
from cell import Cell

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
        