import numpy as np
from numpy.testing import assert_array_equal
import unittest
import common.misc as cm

__author__ = 'Adriana Borowa'
__email__ = 'ada.borowa@gmail.com'


class TestGetUnique(unittest.TestCase):
    """Tests for getting unique points from point list"""

    def setUp(self):
        self.lists = [[[1, 2], [2, 3], [1, 2], [2, 3]],
                      [[1], [1], [1], [1], [1]],
                      []]
        self.answers = [np.array([[1, 2], [2, 3]]).transpose(), np.array([[1]]), np.array([])]

    def test(self):
        for l, a in zip(self.lists, self.answers):
            assert_array_equal(cm.get_unique(l), a)


class TestSymmetricPoint(unittest.TestCase):
    """Tests for finding symmetric point"""

    def setUp(self):
        self.walls = [[3, 5], [2, 7], [0, 3], [3, 3], [0, 3], [0, 7], [0, 9]]
        self.dots = [[2, 4], [2, 3], [5, 6], [2, 2], [2, 3], [0, 8], [0, 8]]
        self.answers = [(1, 3), (2, -1), (10, 9), (1, 1), (4, 3), (0, 9), (0, 7)]

    def test(self):
        """Different dots."""
        for d, w, a in zip(self.walls, self.dots, self.answers):
            self.assertEqual(cm.symmetric_point(w[0], w[1], d[0], d[1]), a)
