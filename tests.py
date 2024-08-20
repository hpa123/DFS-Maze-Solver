# here we test the logic of the maze code without the graphics

import unittest
from maze import Maze

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(num_rows,num_cols)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )
        self.assertFalse(m1._cells[0][0].has_top)
        self.assertFalse(m1._cells[num_cols-1][num_rows-1].has_bottom)

        for row in m1._cells:
            for j in range(len(row)):
                self.assertFalse(row[j].visited)

        m1.solve()


if __name__ == "__main__":
    unittest.main()
        
