import unittest

from fillapix.imageops.reader import FillAPixReader
from fillapix.solver.solver import FillAPixSolver
import numpy as np


class TestSolverSizeOfHood(unittest.TestCase):
    """Tests for size_of_hood function."""

    def setUp(self):
        self.solver = FillAPixSolver(None)

    def test_corner(self):
        """Tests for corner, all corner have neighbourhoods of size 4"""
        self.assertEqual(self.solver.size_of_hood(0, 0), 4)
        self.assertEqual(self.solver.size_of_hood(0, 9), 4)
        self.assertEqual(self.solver.size_of_hood(9, 0), 4)
        self.assertEqual(self.solver.size_of_hood(9, 9), 4)

    def test_border(self):
        """Tests for borders, all borders have neighbourhoods of size 6"""
        self.assertEqual(self.solver.size_of_hood(0, 5), 6)
        self.assertEqual(self.solver.size_of_hood(9, 5), 6)
        self.assertEqual(self.solver.size_of_hood(5, 0), 6)
        self.assertEqual(self.solver.size_of_hood(5, 9), 6)

    def test_inside(self):
        """Tests for other points, all other points have neighbourhoods of size 9"""
        self.assertEqual(self.solver.size_of_hood(2, 3), 9)
        self.assertEqual(self.solver.size_of_hood(4, 3), 9)
        self.assertEqual(self.solver.size_of_hood(8, 2), 9)
        self.assertEqual(self.solver.size_of_hood(5, 5), 9)


if __name__ == '__main__':
    SUITE1 = unittest.TestLoader().loadTestsFromTestCase(TestSolverSizeOfHood)
    print(unittest.TextTestRunner(verbosity=3).run(SUITE1))
