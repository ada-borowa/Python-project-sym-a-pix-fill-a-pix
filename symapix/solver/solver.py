#!/usr/bin/env python3
""" Sym-a-pix: Solving puzzle
"""
import random

import numpy as np
import math
from itertools import permutations
from time import time
import copy

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


def squares_next_to(x, y):
    """Returns 2 squares next to a wall."""
    if x % 2 == 0:
        return [[x, y - 1], [x, y + 1]]
    elif y % 2 == 0:
        return [[x - 1, y], [x + 1, y]]
    return []


class SymAPixSolver:
    """ Solver class. """

    def __init__(self, puzzle):
        if puzzle is None:
            self.puzzle = np.zeros((10, 10), int)
        else:
            self.puzzle = puzzle.get_board()
        self.size = self.puzzle.shape
        self.solution = np.zeros(self.size, int)
        self.user_solution = np.zeros(self.size, int)
        self.set_dots()

    def set_puzzle(self, array):
        """Setting puzzle board; just for fill-a-pix_tests."""
        self.puzzle = array
        self.size = self.puzzle.shape
        self.solution = np.zeros(self.size, int)
        self.set_dots()

    def set_solution(self, array):
        """Sets solution, only for generated puzzles"""
        self.solution = array

    def set_dots(self):
        """Sets values in solution were dots are"""
        for i, row in enumerate(self.puzzle):
            for j, el in enumerate(row):
                if el > 0:
                    self.solution[i, j] = -2
                    self.user_solution[i, j] = -2

    def solve(self):
        """Main solver function"""
        self.init_fill()
        self.mark_closed()
        k_max = 2
        while k_max < 3:
            for k in range(1, k_max + 1):
                for i in range(0, self.size[0]):
                    for j in range(0, self.size[1]):
                        if self.solution[i, j] == -2:
                            self.find_symmetry(i, j, k)
                self.mark_closed()
            k_max += 1

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
            if self.is_wall(a, b):
                new_a, new_b = symmetric_point(x, y, a, b)
                if not self.is_wall_between(x, y, new_a, new_b) and\
                   0 <= new_a < self.size[0] and 0 <= new_b < self.size[1] and\
                   self.solution[new_a, new_b] > -1:
                    self.solution[new_a, new_b] = 1

    def mark_closed(self):
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if self.solution[i, j] == -2:
                    hood, closed = self.is_closed(i, j)
                    if closed:
                        for pair in hood:
                            if pair[0] % 2 == 0 and pair[1] % 2 == 0:
                                if self.solution[pair[0], pair[1]] != -2:
                                    self.solution[pair[0], pair[1]] = -3
                                else:
                                    self.solution[pair[0], pair[1]] = -4

    def is_closed(self, x, y):
        """Checks if region is closed and symmetrical,"""
        i1, i2, j1, j2 = define_frame(x, y)
        closest = [[a, b] for a in range(i1, i2 + 1)
                   for b in range(j1, j2 + 1)
                   if a in [i1, i2] or b in [j1, j2]]
        walls_visited = []
        hood = [[x, y]]
        hood.extend([[a, b] for a in range(i1, i2 + 1)
                    for b in range(j1, j2 + 1)
                    if a not in [i1, i2] and b not in [j1, j2]])
        while closest:
            a, b = closest.pop()
            walls_visited.append([a, b])
            if self.is_wall(a, b):
                c, d = symmetric_point(x, y, a, b)
                if not self.is_wall(c, d):
                    return hood, False
            else:
                options = squares_next_to(a, b)
                for square in options:
                    if square not in hood:
                        hood.append(square)
                        i1, i2, j1, j2 = define_frame(square[0], square[1])
                        frame = [[a, b] for a in range(i1, i2 + 1)
                                 for b in range(j1, j2 + 1)
                                 if a in [i1, i2] or b in [j1, j2]]
                        closest.extend([pair for pair in frame if pair not in walls_visited])
        return hood, True

    def is_wall(self, x, y):
        if x in [-1, self.size[0]]:
            return True
        elif y in [-1, self.size[1]]:
            return True
        elif 0 < x < self.size[0] and 0 < y < self.size[1] and self.solution[x, y] == 1:
            return True
        return False

    def is_wall_between(self, x, y, a, b):
        """Checks if there already is a wall between two points."""
        x_move = 2
        if x > a:
            x_move = -1
        y_move = 2
        if y > a:
            y_move = -1
        if x % 2 == 0:
            if x < a:
                x += 1
            else:
                x -= 1
        if y % 2 == 0 and x % 2 > 0:
            if y < b:
                y += 1
            else:
                y -= 1
        moves = permutations(np.hstack([np.zeros(int(max(0, math.fabs(x-a) - 1))),
                                               np.ones(int(max(0, math.fabs(y-b) - 1)))]))
        moves = list(set(moves))
        if max(0, math.fabs(x-a) - 1) + max(0, math.fabs(y-b) - 1) > 0:
            if len(moves) > 100:
                moves = np.array(moves)
                moves = moves[np.random.choice(len(moves), 100)]
            for move in moves:
                for i, m in enumerate(move):
                    if m == 0:
                        x += x_move
                    elif m == 1:
                        y += y_move
                    if self.is_wall(x, y):
                        return True
        return False

    def is_solved(self):
        """Checks if puzzle is finished: if all squares are -2 or -3"""
        for i in range(0, self.size[0], 2):
            for j in range(0, self.size[1], 2):
                if self.solution[i, j] > -2:
                    return False
        return True

    def correct_fill(self):
        pass

    def print_solution(self):
        """Prints solution, for visual testing."""
        for i, row in enumerate(self.solution):
            txt = ''
            for j, el in enumerate(row):
                if el == -4:
                    txt += 'O '
                elif el == -3:
                    txt += 'x '
                elif el == -2:
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

    def get_solution(self):
        return self.solution

    def get_user_solution(self):
        return self.user_solution

    def get_user_value(self, i, j):
        return self.user_solution[i, j]

    def set_user_value(self, x, y, val):
        self.user_solution[x, y] = val

    def set_solved(self):
        self.user_solution = copy.deepcopy(self.solution)

    def clear_user_solution(self):
        self.user_solution = np.zeros(self.size, int)

    def check_user_solution(self):
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if self.solution[i, j] != self.user_solution[i, j] and self.user_solution[i, j] != 0:
                    return i, j
        return -1, -1

    def is_solved_by_user(self):
        """Checks if puzzle is solved by user."""
        count = 0
        for i in range(0, self.size[0]):
            for j in range(0, self.size[1]):
                if self.user_solution[i, j] != self.solution[i, j]:
                    count += 1
        if count == 0:
            return True
        else:
            return False