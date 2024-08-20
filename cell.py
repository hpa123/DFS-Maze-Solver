from graphics import Line, Point

class Cell:
    # Cells are the boxes which make up our maze.
    def __init__(self,win):
        
        # these coordinates specify the upper left and lower right corners
        # of the cell.
        self._x1 = None
        self._y1 = None
        self._x2 = None
        self._y2 = None
        self.__win = win

        # by default a cell has four walls
        self.has_left = True
        self.has_right = True
        self.has_top = True
        self.has_bottom = True

        # by default, we've not visited a cell
        self.visited = False
    
    def draw_cell(self, p1,p2):
        self._x1 = p1.x
        self._y1 = p1.y
        self._x2 = p2.x
        self._y2 = p2.y
        
        x1 = p1.x
        y1 = p1.y
        x2 = p2.x
        y2 = p2.y


        # we draw whichever sides the cell has; initially all sides are drawn
        if self.has_left:
            left_side = Line(Point(x1,y1), Point(x1,y2))
            left_side.draw_line(self.__win.canvas, 'black')
        else:
            left_side = Line(Point(x1,y1), Point(x1,y2))
            left_side.draw_line(self.__win.canvas, "#d9d9d9")

        if self.has_right:
            right_side = Line(Point(x2,y1), Point(x2,y2))
            right_side.draw_line(self.__win.canvas, 'black')
        else:
            right_side = Line(Point(x2,y1), Point(x2,y2))
            right_side.draw_line(self.__win.canvas, "#d9d9d9")

        if self.has_top:
            top_side = Line(Point(x1,y1), Point(x2,y1))
            top_side.draw_line(self.__win.canvas, 'black')
        else:
            top_side = Line(Point(x1,y1), Point(x2,y1))
            top_side.draw_line(self.__win.canvas, "#d9d9d9")

        if self.has_bottom:
            bottom_side = Line(Point(x1,y2), Point(x2,y2))
            bottom_side.draw_line(self.__win.canvas, 'black')
        else:
            bottom_side = Line(Point(x1,y2), Point(x2,y2))
            bottom_side.draw_line(self.__win.canvas, "#d9d9d9")


    def draw_move(self, to_cell, undo=False):
        # this function draws a path from the center of 
        # one cell to the center of another.

        # if undo is true, we are backtracking through the maze
        if undo:
            color = 'red'
        else:
            color = 'green'

        # get coordinates of the center of the starting cell
        start_x = self._x1 + abs(self._x1 - self._x2)/2
        start_y = self._y1 + abs(self._y1 - self._y2)/2

        start = Point(start_x, start_y)

        end_x = to_cell._x1 + abs(to_cell._x1 - to_cell._x2)/2
        end_y = to_cell._y1 + abs(to_cell._y1 - to_cell._y2)/2

        end = Point(end_x, end_y)

        l = Line(start, end)

        l.draw_line(self.__win.canvas, color)


 

