import unittest

from symapix.solver.solver import SymAPixSolver, symmetric_point
import numpy as np


class TestContainsDot(unittest.TestCase):
    """Tests for checking if there is dot or parto of dot in square."""

    def setUp(self):
        self.solver = SymAPixSolver(None)
        self.arr = np.array([[0, 0, 1, 0, 0, 0, 0],
                             [0, 0, 0, 0, 1, 0, 1],
                             [1, 0, 1, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 1, 0, 0, 1],
                             [0, 0, 0, 0, 0, 0, 0],
                             [0, 1, 0, 0, 1, 0, 1]])

    def test_corner(self):
        self.solver.set_puzzle(self.arr)
        txt = ''
        for i in range(0, self.arr.shape[0], 2):
            for j in range(0, self.arr.shape[1], 2):
                txt += str(int(self.solver.contains_dot(i, j)))
            txt += '\n'
        answer = '0111\n1111\n0111\n1111\n'
        self.assertEqual(txt, answer)


class TestSymmetricPoint(unittest.TestCase):
    """Tests for finding symmetric point"""
    def setUp(self):
        self.walls = [[3, 5], [2, 7], [0, 3], [3, 3], [0, 3], [0, 7], [0, 9]]
        self.dots = [[2, 4], [2, 3], [5, 6], [2, 2], [2, 3], [0, 8], [0, 8]]
        self.answers = [(1, 3), (2, -1), (10, 9), (1, 1), (4, 3), (0, 9), (0, 7)]

    def test(self):
        """Different dots."""
        for d, w, a in zip(self.walls, self.dots, self.answers):
            self.assertEqual(symmetric_point(w[0], w[1], d[0], d[1]), a)