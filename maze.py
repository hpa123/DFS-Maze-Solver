import time
from cell import Cell
from graphics import Point
import random
from collections import deque
from tkinter import *
from tkinter import messagebox

class Maze:
    # this class holds all the cells in the maze as a list of lists.
    def __init__(
            self,
            win=None,
            seed=None,
            x1=10,
            y1=10,
    ):
        
        # x1 and y1 represent how many pixels from the top and left
        # the maze should start from the side of the window.
        self._x1 = x1
        self._y1 = y1
        self._win = win
        
        root = win.get_root()

        # create text fields and get user input for dimensions
        # of maze
        cols = Entry(root,justify='center')
        cols.pack()
        rows = Entry(root,justify='center')
        rows.pack()
        cols.focus_set()
        
        def submit(*unused):
            self._num_cols = cols.get()
            self._num_rows = rows.get()
            try:
                val1 = int(self._num_rows)
                val2 = int(self._num_cols)
                if val1 <= 0 or val2 <= 0:
                    messagebox.showerror('You Have Messed Up', 'Maze dimensions must be larger than 0.')
                    rows.delete(0,'end')
                    cols.delete(0,'end')
                    cols.focus_set()
                    return
            except:
                messagebox.showerror("You Have Messed Up","That's not an integer....")
                rows.delete(0,'end')
                cols.delete(0,'end')
                cols.focus_set()
                return
            
            self._num_rows = val1
            self._num_cols = val2

            cols.destroy()
            rows.destroy()
            go_button.destroy()

            self._cell_size_x = (win.win_w - 2*x1)/self._num_cols
            self._cell_size_y = (win.win_h - 2*y1)/self._num_rows

            self._create_cells()
            self._break_entrance_and_exit()

            if seed:
                random.seed(seed)

            self._break_walls_r(0,0)

            self._reset_cells_visited()

            self.solve()

        go_button = Button(root,text='Create Maze',command=submit)
        go_button.pack()

    def _create_cells(self):
        self._cells = []
        
        for i in range(self._num_cols):
            self._cells.append([])
            for j in range(self._num_rows):
                self._cells[i].append(Cell(self._win))
    
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i,j)
        
    def _draw_cell(self, i, j):

        if self._win == None:
            return

        to_draw = self._cells[i][j]

        # to get the new cell's corners, we start at the maze's starting
        # point and move i (j) units of cell_size_x (cell_size_y) to the right (down).
        # i correponds to x, j corresponds to y

        cell_x1 = self._x1 + i*self._cell_size_x
        cell_x2 = cell_x1 + self._cell_size_x
        cell_y1 = self._y1 + j*self._cell_size_y
        cell_y2 = cell_y1 + self._cell_size_y
        p1 = Point(cell_x1, cell_y1)
        p2 = Point(cell_x2, cell_y2)

        to_draw.draw_cell(p1,p2)
        self._animate()
    
    def _animate(self):

        if self._win == None:
            return
        
        self._win.redraw()
        time.sleep(.05)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top = False
        self._draw_cell(0,0)

        end_x = self._num_cols - 1
        end_y = self._num_rows - 1

        self._cells[end_x][end_y].has_bottom = False
        self._draw_cell(end_x, end_y)

    def _break_walls_r(self,i,j):
        # DFS through the grid, removing walls at random as we go,
        # generating the maze
        self._cells[i][j].visited = True
        
        while True:
            to_visit = []             
            
            # left and right
            for k in [i-1, i+1]:
                if 0 < k < self._num_cols:
                    if not self._cells[k][j].visited:
                        to_visit.append((k,j))
            # up and down
            for l in [j-1, j+1]:
                if 0 < l < self._num_rows:  
                    if not self._cells[i][l].visited:
                        to_visit.append((i,l))
            
            if not to_visit:
                self._draw_cell(i,j)
                return
            
            next_i, next_j = random.choice(to_visit)

            # right
            if next_i == i + 1:
                self._cells[i][j].has_right = False
                self._cells[next_i][j].has_left = False
            # left
            if next_i == i - 1:
                self._cells[i][j].has_left = False
                self._cells[next_i][j].has_right = False
            # up
            if next_j == j - 1:
                self._cells[i][j].has_top = False
                self._cells[i][next_j].has_bottom = False
            
            # down
            if next_j == j + 1:
                self._cells[i][j].has_bottom = False
                self._cells[i][next_j].has_top = False

            self._break_walls_r(next_i, next_j)
            
    def _reset_cells_visited(self):
        for row in self._cells:
            for i in range(len(row)):
                row[i].visited = False
    
    def solve(self):
        return self._solve_r(0,0)
    
    def get_adjacent(self, i,j):
        adj = []
        
        # left and right
        for k in [i-1, i+1]:
            if 0 < k < self._num_cols:
                adj.append((k,j))
        
        # up and down
        for l in [j-1, j+1]:
            if 0 < l < self._num_rows:  
                adj.append((i,l))
        
        return adj
        
    # def _solve_BFS(self, i,j):
        # for this, get the full reversed path and then draw at the end.
        # maybe create another variable that tracks backtracking
        # number of times a given cell connects to another cell > 1
        # means backtracking occured?


        path = {self._cells[i][j]: None}
        to_visit = [self._cells[i][j]]
        undo = False
        
        while to_visit:
            self._animate()
            cur_cell = to_visit.pop(0)
            adj = self.get_adjacent(i,j)
            
            for coords in adj:
                k, l = coords
                if k == i + 1 and not self._cells[k][j].visited:
                    if not self._cells[k][j].has_left:
                        to_visit.append(self._cells[k][j])
                        path[self._cells[k][j]] = cur_cell
                        cur_cell.draw_move(self._cells[k][j])
                        i = k
                
                elif k == i - 1 and not self._cells[k][j].visited:
                    if not self._cells[k][j].has_right:
                        to_visit.append(self._cells[k][j])
                        path[self._cells[k][j]] = cur_cell
                        cur_cell.draw_move(self._cells[k][j])
                        i = k

                elif l == j + 1 and not self._cells[i][l].visited:
                    if not self._cells[i][l].has_top:
                        to_visit.append(self._cells[i][l])
                        path[self._cells[i][l]] = cur_cell
                        cur_cell.draw_move(self._cells[i][l])
                        j = l
                
                elif l == j - 1 and not self._cells[i][l].visited:
                    if not self._cells[i][l].has_bottom:
                        to_visit.append(self._cells[i][l])
                        path[self._cells[i][l]] = cur_cell
                        cur_cell.draw_move(self._cells[i][l])
                        j = l

                else:
                    to_visit.insert(0,cur_cell)
                    undo=True

            cur_cell.visited = True

            """if self._cells[self._num_cols-1][self._num_rows-1].visited == True:
                path_list = []
                
                while cur_cell is not None:
                    path_list.append(cur_cell)
                    cur_cell = path[cur_cell]

                path_list.reverse()

                for cell, next_cell in zip(path_list, path_list[1:]+[path_list[0]]):
                    cell.draw_move(next_cell)"""
            
        return

    def _solve_r(self,i,j):
        self._animate()

        self._cells[i][j].visited = True

        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return True
        
        adj = self.get_adjacent(i,j)

        for coords in adj:
                k, l = coords
                cur_cell = self._cells[i][j]

                if k == i + 1 and not self._cells[k][j].visited:
                    
                    if not self._cells[k][j].has_left:
                        cur_cell.draw_move(self._cells[k][j])
                        
                        if self._solve_r(k,j):
                            return True
                        cur_cell.draw_move(self._cells[k][j],True)
                
                elif k == i - 1 and not self._cells[k][j].visited:
                    
                    if not self._cells[k][j].has_right:
                        cur_cell.draw_move(self._cells[k][j])
                        
                        if self._solve_r(k,j):
                            return True
                        
                        cur_cell.draw_move(self._cells[k][j],True)

                elif l == j + 1 and not self._cells[i][l].visited:
                    if not self._cells[i][l].has_top:
                        cur_cell.draw_move(self._cells[i][l])
                        
                        if self._solve_r(i,l):
                            return True
                        
                        cur_cell.draw_move(self._cells[i][l],True)
                
                elif l == j - 1 and not self._cells[i][l].visited:
                    if not self._cells[i][l].has_bottom:
                        cur_cell.draw_move(self._cells[i][l])
                        
                        if self._solve_r(i,l):
                            return True
                        
                        cur_cell.draw_move(self._cells[i][l],True)
                
        return False


        

        



            


            
            



        
















