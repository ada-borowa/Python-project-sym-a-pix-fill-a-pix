#!/usr/bin/env python3
""" Sym-a-pix: Solving puzzle
"""

import numpy as np
import math
from itertools import product

__author__ = 'Adriana Borowa'
__email__ = 'ada.borowa@gmail.com'


def define_frame(i, j):
    """Defines frame of closest possible walls."""
    if i % 2 == 0 and j % 2 == 0:
        return [i - 1, i + 1, j - 1, j + 1]
    elif i % 2 == 0 and j % 2 > 0:
        return [i - 1, i + 1, j - 2, j + 2]
    elif i % 2 > 0 and j % 2 == 0:
        return [i - 2, i + 2, j - 1, j + 1]
    elif i % 2 > 0 and j % 2 > 0:
        return [i - 2, i + 2, j - 2, j + 2]


def expand(x1, x2, y1, y2):
    """Expands pre-defined frame."""
    return x1 - 2, x2 + 2, y1 - 2, y2 + 2


def symmetric_point(x, y, a, b):
    """Find wall symmetric to given: x, y - point of circle, a, b - point of line"""
    return 2 * x - a, 2 * y - b


def wall_between(x, y, i, j):
    """Finds location of the wall between two squares."""
    if x == i:
        return [x, int((y + j) / 2.0)]
    elif y == j:
        return [int((x + i) / 2.0), y]


class SymAPixSolver:
    """ Solver class. """

    def __init__(self, puzzle):
        if puzzle is None:
            self.puzzle = np.zeros((10, 10), int)
        else:
            self.puzzle = puzzle.get_board()
        self.size = self.puzzle.shape
        self.solution = np.zeros(self.size, int)
        self.set_dots()

    def set_puzzle(self, array):
        """Setting puzzle board; just for fill-a-pix_tests."""
        self.puzzle = array
        self.size = self.puzzle.shape
        self.solution = np.zeros(self.size, int)
        self.set_dots()

    def set_dots(self):
        """Sets values in solution were dots are"""
        for i, row in enumerate(self.puzzle):
            for j, el in enumerate(row):
                if el > 0:
                    self.solution[i, j] = -2

    def solve(self):
        """Main solver function"""
        self.init_fill()
        for i in range(0, self.size[0]):
            for j in range(0, self.size[1]):
                if self.solution[i, j] == -2:
                    self.find_symmetry(i, j, 1)
        for i in range(0, self.size[0]):
            for j in range(0, self.size[1]):
                if self.solution[i, j] == -2:
                    self.find_symmetry(i, j, 2)

    def init_fill(self):
        """Fills obvious lines between two dots."""
        for x in range(0, self.size[0], 2):
            for y in range(0, self.size[1], 2):
                if self.contains_dot(x, y):
                    adjacent = self.adjacent_squares(x, y)
                    for pair in adjacent:
                        i, j = pair
                        if self.contains_dot(i, j) and not self.is_same_dot(x, y, i, j):
                            a, b = wall_between(x, y, i, j)
                            self.solution[a, b] = 1

    def contains_dot(self, x, y):
        """Checks if square contains dot or part of a dot"""
        for i in range(max(x - 1, 0), min(x + 2, self.size[0])):
            for j in range(max(y - 1, 0), min(y + 2, self.size[1])):
                if self.solution[i, j] == -2:
                    return True
        return False

    def adjacent_squares(self, x, y):
        """Returns list of squares adjacent to given."""
        adj = []
        if x > 1:
            adj.append([x - 2, y])
        if x < self.size[0] - 1:
            adj.append([x + 2, y])
        if y > 1:
            adj.append([x, y - 2])
        if y < self.size[1] - 1:
            adj.append([x, y + 2])
        return adj

    def is_same_dot(self, x, y, i, j):
        """Checks if two squares have the same dot."""
        a = self.dots_list(x, y)
        b = self.dots_list(i, j)
        if len([k for k in a + b if k in a and k in b]) > 0:
            return True
        else:
            return False

    def dots_list(self, x, y):
        """Gives list of dots for point."""
        dots = []
        for i in range(max(x - 1, 0), min(x + 2, self.size[0])):
            for j in range(max(y - 1, 0), min(y + 2, self.size[1])):
                if self.solution[i, j] == -2:
                    dots.append([i, j])
        return dots

    def find_symmetry(self, x, y, k):
        """Find symmetry in distance k."""
        i1, i2, j1, j2 = define_frame(x, y)
        c = 1
        while c < k:
            i1, i2, j1, j2 = expand(i1, i2, j1, j2)
            c += 1
        frame = [(a, b) for a in range(i1, i2 + 1)
                 for b in range(j1, j2 + 1)
                 if a in [i1, i2] or b in [j1, j2]]
        for (a, b) in frame:
            print(x, y, a, b)
            if a in [-1, self.size[0]] or \
               b in [-1, self.size[1]] or \
               0 <= a < self.size[0] and 0 <= b < self.size[1] and self.solution[a, b] == 1:
                new_a, new_b = symmetric_point(x, y, a, b)
                print(x, y, a, b, new_a, new_b)
                if 0 <= new_a < self.size[0] and 0 <= new_b < self.size[1] and\
                   self.solution[new_a, new_b] > -1:
                    # print(new_a, new_b)
                    self.solution[new_a, new_b] = 1

    def is_solved(self):
        pass

    def correct_fill(self):
        pass

    def print_solution(self):
        """Prints solution, for visual testing."""
        for i, row in enumerate(self.solution):
            txt = ''
            for j, el in enumerate(row):
                if el == -2:
                    if i % 2 == 0 and j % 2 == 0:
                        txt += 'o '
                    elif i % 2 == 0 and j % 2 > 0:
                        txt += 'o '
                    elif i % 2 > 0 and j % 2 == 0:
                        txt += 'o '
                    elif i % 2 > 0 and j % 2 > 0:
                        txt += 'o '
                elif el == -1:
                    if i % 2 == 0 and j % 2 == 0:
                        txt += '  '
                    elif i % 2 == 0 and j % 2 > 0:
                        txt += '| '
                    elif i % 2 > 0 and j % 2 == 0:
                        txt += '_ '
                    elif i % 2 > 0 and j % 2 > 0:
                        txt += '+ '
                elif el == 0:
                    if i % 2 == 0 and j % 2 == 0:
                        txt += '  '
                    elif i % 2 == 0 and j % 2 > 0:
                        txt += 'l '
                    elif i % 2 > 0 and j % 2 == 0:
                        txt += '. '
                    elif i % 2 > 0 and j % 2 > 0:
                        txt += '+ '
                elif el == 1:
                    if i % 2 == 0 and j % 2 == 0:
                        txt += '  '
                    elif i % 2 == 0 and j % 2 > 0:
                        txt += '||'
                    elif i % 2 > 0 and j % 2 == 0:
                        txt += '__'
                    elif i % 2 > 0 and j % 2 > 0:
                        txt += '+ '

            print(txt)
