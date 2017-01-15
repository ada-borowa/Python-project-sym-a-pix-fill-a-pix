#!/usr/bin/env python3
""" Sym-a-pix: Solving puzzle
"""
import random

import numpy as np
import math
from itertools import permutations
from time import time
import copy

from common.misc import get_unique

__author__ = 'Adriana Borowa'
__email__ = 'ada.borowa@gmail.com'


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
    return math.sqrt((x - i)**2 + (y - j)**2)


class SymAPixSolver:
    """ Solver class. """

    def __init__(self, puzzle):
        if puzzle is None:
            self.puzzle = np.zeros((10, 10), int) - 1
        else:
            self.puzzle = puzzle.get_board()
        self.size = self.puzzle.shape
        self.colors = puzzle.get_colors()

        # solution: -2 - dot, -1 - sure not wall, 1 - sure wall, 0 - unsure
        self.solution = np.zeros(self.size, int)
        self.user_solution = np.zeros(self.size, int)
        self.fill_color = np.zeros(self.size, int) - 1  # -1 - non, [0,1,2,3,...] - color from list
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
        self.set_dots()

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
        self.fill_smallest()
        self.check_closed()
        for i in range(1, 20):
            self.fill(i)
            self.fill_smallest()
            self.check_closed()
            self.print_solution()

    def init_fill(self):
        """Fills obvious lines between two dots: if two squares contain dot or part of dot there is line."""
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
        """Checks if square contains dot or part of a dot
        or checks if line contains dot or part of a dot."""
        if x % 2 == 0 and y % 2 == 0:
            for i in range(max(x - 1, 0), min(x + 2, self.size[0])):
                for j in range(max(y - 1, 0), min(y + 2, self.size[1])):
                    if self.solution[i, j] == -2:
                        return True
        elif x % 2 == 0:
            for j in range(y - 1, y + 2):
                if self.solution[x, j] == -2:
                    return True
        elif y % 2 == 0:
            for i in range(x - 1, x + 2):
                if self.solution[i, y] == -2:
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

    def fill_smallest(self):
        """Fils the smallest blocks (1, 2 or 4 squares depending on where dot is)."""
        for x in range(0, self.size[0]):
            for y in range(0, self.size[1]):
                if self.solution[x, y] == -2:
                    frame = define_frame(x, y)
                    for wall in frame:
                        if self.is_wall(*wall):
                            a, b = symmetric_point(x, y, wall[0], wall[1])
                            if 0 <= a < self.size[0] and 0 <= b < self.size[1]:
                                self.solution[a, b] = 1

    def fill(self, k):
        """Fills to length of k"""
        for i, row in enumerate(self.solution):
            for j, el in enumerate(row):
                if self.solution[i, j] == -2 and not self.closest_closed(i, j, self.solution):
                    queue = define_block(i, j)
                    visited = []
                    while queue:
                        p = queue.pop()
                        visited.append(p)
                        next_ones = self.adjacent_squares(p[0], p[1])
                        for n in next_ones:
                            if point_dist(i, j, n[0], n[1]) > k:
                                return
                            if not (self.solution[n[0], n[1]] == -2 or n in visited):
                                n_sym = symmetric_point(i, j, n[0], n[1])
                                p_sym = symmetric_point(i, j, p[0], p[1])
                                if (0 <= n_sym[0] < self.size[0] and 0 <= n_sym[1] < self.size[1] and
                                      0 <= p_sym[0] < self.size[0] and 0 <= p_sym[1] < self.size[1]) and \
                                      not (self.solution[n_sym[0], n_sym[1]] == -2 or
                                      self.is_wall(*wall_between(p_sym[0], p_sym[1], n_sym[0], n_sym[1]))):

                                    new_wall = wall_between(p_sym[0], p_sym[1], n_sym[0], n_sym[1])
                                    if self.is_wall(*wall_between(p[0], p[1], n[0], n[1])) and \
                                            not (self.is_wall(*wall_between(p_sym[0], p_sym[1], n_sym[0], n_sym[1]))
                                                 or self.contains_dot(new_wall[0], new_wall[1])):
                                        self.solution[new_wall[0], new_wall[1]] = 1
                                    else:
                                        queue.append(n)

                    block = get_unique(np.array(visited))
                    if self.block_is_closed(block, self.solution):
                        for b in block:
                            self.solution[b[0], b[1]] = self.puzzle[i, j]

    def check_closed(self, user=False):
        """
        Checks if there are new closed blocks.
        :param user: if True, sets user solution, otherwise game's solution
        :return: None
        """
        if user:
            array = self.user_solution
        else:
            array = self.solution

        for i, row in enumerate(array):
            for j, el in enumerate(row):
                if array[i, j] == -2 and not self.closest_closed(i, j, array):
                    queue = define_block(i, j)
                    visited = []
                    while queue:
                        p = queue.pop()
                        visited.append(p)
                        next_ones = self.adjacent_squares(p[0], p[1])
                        for n in next_ones:
                            if not (array[n[0], n[1]] == -2 or
                                        self.is_wall(*wall_between(p[0], p[1], n[0], n[1])) or
                                            n in visited):
                                n_sym = symmetric_point(i, j, n[0], n[1])
                                p_sym = symmetric_point(i, j, p[0], p[1])
                                if (0 <= n_sym[0] < self.size[0] and 0 <= n_sym[1] < self.size[1] and
                                                0 <= p_sym[0] < self.size[0] and 0 <= p_sym[1] < self.size[1]) and \
                                        not (array[n_sym[0], n_sym[1]] == -2 or
                                                 self.is_wall(*wall_between(p_sym[0], p_sym[1], n_sym[0], n_sym[1]))):
                                    queue.append(n)

                    block = get_unique(np.array(visited))
                    if self.block_is_closed(block, array):
                        for b in block:
                            array[b[0], b[1]] = self.puzzle[i, j]

    def block_is_closed(self, block, array):
        """Checks if all walls around block are closed."""
        all_walls = []
        for b in block:
            all_walls.append(define_frame(b[0], b[1]))
        all_walls = np.array(all_walls).reshape(-1, 2)
        all_walls = np.array([x for x in all_walls if count(all_walls, x) == 1])
        for w in all_walls:
            if 0 <= w[0] < self.size[0] and 0 <= w[1] < self.size[1] and array[w[0], w[1]] != 1:
                return False
        return True

    def closest_closed(self, i, j, array):
        """Checks if closest block to dot are filled."""
        block = define_block(i, j)
        closed = True
        for b in block:
            if array[b[0], b[1]] < 1:
                closed = False
        return closed

    def is_wall(self, x, y):
        """Checks if point is wall."""
        if x in [-1, self.size[0]]:
            return True
        elif y in [-1, self.size[1]]:
            return True
        elif 0 <= x < self.size[0] and 0 <= y < self.size[1] and self.solution[x, y] == 1:
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
        """Checks if game is currently correctly filled."""
        pass

    def print_solution(self):
        """Prints solution, for testing."""
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
        """Returns real solution."""
        return self.solution

    def get_user_solution(self):
        """Returns user's solution."""
        return self.user_solution

    def get_color_board(self):
        """Returns current colors and color list."""
        return self.fill_color

    def get_colors(self):
        """Returns colors used in puzzle."""
        return self.colors

    def get_user_value(self, i, j):
        """Reads value chosen by user."""
        if 0 <= i < self.size[0] and 0 <= j < self.size[1]:
            return self.user_solution[i, j]

    def set_user_value(self, x, y, val):
        """Sets value chosen by user."""
        self.user_solution[x, y] = val
        self.update_user_filling()

    def update_user_filling(self):
        self.check_closed(user=True)
        for i, row in enumerate(self.user_solution):
            for j, el in enumerate(row):
                self.fill_color[i, j] = el if i % 2 == 0 and j % 2 == 0 and el > 0 else -1

    def set_solved(self):
        """Sets user solution to real solution."""
        self.user_solution = copy.deepcopy(self.solution)
        for i, row in enumerate(self.user_solution):
            for j, el in enumerate(row):
                self.fill_color[i, j] = el if i % 2 == 0 and j % 2 == 0 and el > 0 else -1

    def clear_user_solution(self):
        """Resets user solution."""
        self.user_solution = np.zeros(self.size, int)
        self.fill_color = np.zeros(self.size, int) - 1

    def check_user_solution(self):
        """Checks user solution. Omits unsure squares."""
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
