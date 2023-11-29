import unittest
from main import Maze


class Tests(unittest.TestCase):
    def test_break_enterance_and_exit(self):
        grid_num = 10 
        m1 = Maze(0, 0, grid_num, 10)
        m1.create_cells()
        self.assertEqual(m1.cells[0][0].bottom, False)
        self.assertEqual(m1.cells[-1][-1].top, False)

    def test_break_enterance_and_exit1(self):
        grid_num = 34
        m1 = Maze(2, 2, grid_num, 10)
        m1.create_cells()
        self.assertEqual(m1.cells[0][0].top, False)
        self.assertEqual(m1.cells[-1][-1].bottom, False)
    """def test_maze_create_cells(self):
        grid_num = 10 
        m1 = Maze(0, 0, grid_num, 10)
        m1.create_cells()
        self.assertEqual(
            len(m1.cells),
            grid_num,
)
        self.assertEqual(
            len(m1.cells[0]),
            grid_num,
        )

    def test_maze_create_cells2(self):
        grid_num = 20
        m1 = Maze(2, 2, grid_num, 3)
        m1.create_cells()
        self.assertEqual(
            len(m1.cells),
            grid_num,
        )
        self.assertEqual(
            len(m1.cells[0]),
            grid_num,
        )
"""
"""if __name__ == "__main__":
    unittest.main()
"""

