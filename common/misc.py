"""Miscellaneous common functions."""

import math
import numpy as np

__author__ = 'Adriana Borowa'
__email__ = 'ada.borowa@gmail.com'


def get_unique(a):
    """Returns unique items in np.array
    :param a:  array
    :return: unique elements of array
    """
    if len(a) > 0:
        a = np.array(a)
        b = np.ascontiguousarray(a).view(np.dtype((np.void, a.dtype.itemsize * a.shape[1])))
        _, idx = np.unique(b, return_index=True)
        return a[idx]
    else:
        return np.array([])


def define_frame(i, j):
    """Defines frame of closest possible walls."""
    if i % 2 == 0 and j % 2 == 0:
        return [[i - 1, j], [i + 1, j], [i, j - 1], [i, j + 1]]
    elif i % 2 == 0 and j % 2 > 0:
        return [[i, j - 2], [i, j + 2], [i - 1, j - 1], [i - 1, j + 1], [i + 1, j - 1], [i + 1, j + 1]]
    elif i % 2 > 0 and j % 2 == 0:
        return [[i - 2, j], [i + 2, j], [i - 1, j - 1], [i - 1, j + 1], [i + 1, j - 1], [i + 1, j + 1]]
    elif i % 2 > 0 and j % 2 > 0:
        return [[i - 2, j - 1], [i - 2, j + 1], [i - 1, j - 2], [i - 1, j + 2],
                [i + 1, j - 2], [i + 1, j + 2], [i + 2, j - 1], [i + 2, j + 1]]


def define_block(i, j):
    """Defines squares in block."""
    if i % 2 == 0 and j % 2 == 0:
        return [[i, j]]
    elif i % 2 == 0 and j % 2 > 0:
        return [[i, j - 1], [i, j + 1]]
    elif i % 2 > 0 and j % 2 == 0:
        return [[i - 1, j], [i + 1, j]]
    elif i % 2 > 0 and j % 2 > 0:
        return [[i - 1, j - 1], [i - 1, j + 1],
                [i + 1, j - 1], [i + 1, j + 1]]


def symmetric_point(x, y, a, b):
    """Find wall symmetric to given: x, y - point of circle, a, b - point of line"""
    return 2 * x - a, 2 * y - b


def wall_between(x, y, i, j):
    """Finds location of the wall between two squares."""
    if x == i:
        return [x, int((y + j) / 2.0)]
    elif y == j:
        return [int((x + i) / 2.0), y]


def squares_next_to(x, y):
    """Returns 2 squares next to a wall."""
    if x % 2 == 0:
        return [[x, y - 1], [x, y + 1]]
    elif y % 2 == 0:
        return [[x - 1, y], [x + 1, y]]
    return []


def count(array, el):
    """Counts elements el in numpy array"""
    c = 0
    for a in array:
        if a[0] == el[0] and a[1] == el[1]:
            c += 1
    return c


def point_dist(x, y, i, j):
    """Calculates distance between points."""
    return math.sqrt((x - i) ** 2 + (y - j) ** 2)


def adjacent_squares(x, y):
    """Returns list of squares adjacent to given."""
    return [[x - 2, y], [x + 2, y], [x, y - 2], [x, y + 2]]


def closest_closed(i, j, array):
    """Checks if closest block to dot are filled."""
    block = define_block(i, j)
    closed = True
    for b in block:
        if array[b[0], b[1]] < 1:
            closed = False
    return closed
