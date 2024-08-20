from graphics import Window
from maze import Maze

def main():
    # defines a seed for random number generation; mostly for testing purposes, so that
    # the solver behaves the same way each run.
    seed = None

    win = Window()

    Maze(win, seed)

    win.wait_for_close()

main()
