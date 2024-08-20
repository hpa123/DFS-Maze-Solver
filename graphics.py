from tkinter import *

class Window:
    
    # creates a canvas widget to draw our maze with provided width w and height h
    def __init__(self):
        self.__root = Tk()
        self.__root.protocol("WM_DELETE_WINDOW",self.close)
        self.__root.title("Maze Solver")
        
        # calculate window size based on screen size
        w, h = self.get_screen_size()
        self.win_w = w//2
        self.win_h = h//2

        self.canvas = Canvas(self.__root, height=self.win_h, width=self.win_w)
        self.canvas.pack(fill=BOTH, expand=1)

        self.running = False

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def get_root(self):
        return self.__root

    def get_screen_size(self):
        screen_w = self.__root.winfo_screenwidth()
        screen_h = self.__root.winfo_screenheight()
        return screen_w, screen_h

    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()
    
    def close(self):
        self.running = False
        self.__root.destroy()

    def draw_line(self, line, color):
        line.draw(self.canvas, color)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2


    # pick out the x and y coordinates established by the constructor
    # and draw the line on the canvas in specified color.
    def draw_line(self, canvas, color):
        x1 = self.p1.x
        y1 = self.p1.y
        x2 = self.p2.x
        y2 = self.p2.y

        canvas.create_line(x1,y1,x2,y2, fill=color,width=2)