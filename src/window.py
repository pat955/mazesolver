import os
import tkinter
from tkinter import Tk, Canvas, Button, Frame, Entry, Label
from maze import Maze

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
                    maze_str = str(self.current_maze.rows), str(self.current_maze.columns), str(self.current_maze.cell_x), str(self.current_maze.cell_y)+'\n'
                    if len(file.read()) != 0:
                        if file.readlines[-1] == maze_str:
                            file.writeline(maze_str)
                    else:
                        file.write(maze_str)
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