from graphics import Window
from maze import Maze

def main():
    seed = None

    win = Window()

    Maze(win, seed)

    win.wait_for_close()

main()