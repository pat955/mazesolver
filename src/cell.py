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
