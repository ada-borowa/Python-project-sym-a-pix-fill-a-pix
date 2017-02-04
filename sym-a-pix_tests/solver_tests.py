import unittest
import numpy as np

from symapix.solver.solver import SymAPixSolver
from common.misc import symmetric_point

__author__ = 'Adriana Borowa'
__email__ = 'ada.borowa@gmail.com'


class TestContainsDot(unittest.TestCase):
    """Tests for checking if there is dot or part of dot in square."""
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


class TestIsInside(unittest.TestCase):
    """Test for checking if point is inside."""
    def setUp(self):
        self.solver = SymAPixSolver(None)
        self.arr = np.array([[0, 0, 1, 0, 0, 0, 0],
                             [0, 0, 0, 0, 1, 0, 1],
                             [1, 0, 1, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 1, 0, 0, 1],
                             [0, 0, 0, 0, 0, 0, 0],
                             [0, 1, 0, 0, 1, 0, 1]])

    def test_inside(self):
        self.solver.set_puzzle(self.arr)
        txt = ''
        for i in range(-3, 10):
            for j in range(-3, 10):
                txt += '1' if self.solver.is_inside(i, j) else '0'
            txt += '\n'
        answer = '0000000000000\n0000000000000\n0000000000000\n0001111111000' \
                 '\n0001111111000\n0001111111000\n0001111111000\n0001111111000' \
                 '\n0001111111000\n0001111111000\n0000000000000\n0000000000000' \
                 '\n0000000000000\n'
        self.assertEqual(txt, answer)
