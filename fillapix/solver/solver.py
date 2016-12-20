#!/usr/bin/env python3
""" Fill-a-pix: Solving puzzle
"""

import numpy as np
import math
import copy
from fillapix.puzzle.container import Container

__author__ = 'Adriana Borowa'
__email__ = 'ada.borowa@gmail.com'


class FillAPixSolver:
    """ Solver class. """

    def __init__(self, puzzle):
        if puzzle is None:
            self.puzzle = np.zeros((10, 10), int)
        else:
            self.puzzle = puzzle.get_board()
        self.size = self.puzzle.shape
        self.solution = np.zeros(self.size, int)

    def set_puzzle(self, array):
        """Setting puzzle board; just for tests."""
        self.puzzle = array
        self.size = self.puzzle.shape
        self.solution = np.zeros(self.size, int)

    def solve(self):
        """Solver:
        1. Fills obvious: 0 and 9, 4 in corners, 6 on borders
        2. Goes from 8 to 1 and checks if there are obvious points"""
        for i in range(0, self.size[0]):
            for j in range(0, self.size[1]):
                if self.puzzle[i, j] == 0:
                    self.assign_to_hood(i, j, -1)
                elif self.puzzle[i, j] == 9:
                    self.assign_to_hood(i, j, 1)
                elif self.size_of_hood(i, j) == 4 and self.puzzle[i, j] == 4:
                    self.assign_to_hood(i, j, 1)
                elif self.size_of_hood(i, j) == 6 and self.puzzle[i, j] == 6:
                    self.assign_to_hood(i, j, 1)

        count = 0
        while not self.is_solved():
            self.fill()
            self.print_solution()
            for i in range(0, self.size[0]):
                for j in range(0, self.size[1]):
                    if (self.solution[i, j] == 0 or \
                                        self.filled_sure(i, j) + self.empty_sure(i, j) < self.size_of_hood(i, j)) \
                            and self.puzzle[i, j] < 10:
                        self.find_2_clue(i, j)
            if count == 10:
                break
            count += 1
        self.print_solution()

    def fill(self):
        """Fills fields with respect to actual knowledge."""
        while True:
            changed = 0
            for k in range(8, 0, -1):
                for i in range(0, self.size[0]):
                    for j in range(0, self.size[1]):
                        if self.puzzle[i, j] == k:
                            if self.filled_sure(i, j) == k:
                                changed += self.assign_to_hood(i, j, -1)
                            elif self.empty_sure(i, j) == self.size_of_hood(i, j) - k:
                                changed += self.assign_to_hood(i, j, 1)
            if changed == 0:
                break

    def find_2_clue(self, x, y):
        el1 = self.puzzle[x, y]
        el1_hood = [(a, b) for a in range(max(0, x - 1), min(x + 2, self.size[0]))
                    for b in range(max(0, y - 1), min(y + 2, self.size[1]))]
        for i in range(max(0, x - 1), min(x + 2, self.size[0])):
            for j in range(max(0, y - 1), min(y + 2, self.size[1])):
                if (i != x or j != y) and self.puzzle[i, j] < 10:
                    el2 = self.puzzle[i, j]
                    el2_hood = [(a, b) for a in range(max(0, i - 1), min(i + 2, self.size[0]))
                                for b in range(max(0, j - 1), min(j + 2, self.size[1]))]
                    intersection = [a for a in set(el1_hood + el2_hood) if a in el1_hood and a in el2_hood]
                    if max(len(el1_hood), len(el2_hood)) - len(intersection) == math.fabs(el1 - el2):
                        el1_alone = [a for a in el1_hood if a not in intersection]
                        el2_alone = [a for a in el2_hood if a not in intersection]
                        if el1 > el2:
                            for (k, l) in el1_alone:
                                self.solution[k, l] = 1
                            for (k, l) in el2_alone:
                                self.solution[k, l] = -1
                        else:
                            for (k, l) in el1_alone:
                                self.solution[k, l] = -1
                            for (k, l) in el2_alone:
                                self.solution[k, l] = 1

        for i in range(max(0, x - 2), min(x + 2, self.size[0])):
            for j in range(max(0, y - 2), min(y + 2, self.size[1])):
                if (i not in range(max(0, x - 1), min(x + 1, self.size[0])) or
                            j not in range(max(0, y - 1), min(y + 1, self.size[1]))) and \
                                self.puzzle[i, j] < 10:
                    el2 = self.puzzle[i, j]
                    el2_hood = [(a, b) for a in range(max(0, i - 1), min(i + 2, self.size[0]))
                                for b in range(max(0, j - 1), min(j + 2, self.size[1]))]
                    intersection = [a for a in set(el1_hood + el2_hood) if
                                    a in el1_hood and a in el2_hood]
                    if max(len(el1_hood), len(el2_hood)) - len(intersection) == math.fabs(
                                    el1 - el2):
                        el1_alone = [a for a in el1_hood if a not in intersection]
                        el2_alone = [a for a in el2_hood if a not in intersection]
                        if el1 > el2:
                            for (k, l) in el1_alone:
                                self.solution[k, l] = 1
                            for (k, l) in el2_alone:
                                self.solution[k, l] = -1
                        else:
                            for (k, l) in el1_alone:
                                self.solution[k, l] = -1
                            for (k, l) in el2_alone:
                                self.solution[k, l] = 1

    def filled_sure(self, x, y):
        count = 0
        for i in range(max(0, x - 1), min(x + 2, self.size[0])):
            for j in range(max(0, y - 1), min(y + 2, self.size[1])):
                if self.solution[i, j] == 1:
                    count += 1
        return count

    def empty_sure(self, x, y):
        count = 0
        for i in range(max(0, x - 1), min(x + 2, self.size[0])):
            for j in range(max(0, y - 1), min(y + 2, self.size[1])):
                if self.solution[i, j] == -1:
                    count += 1
        return count

    def size_of_hood(self, i, j):
        """Gets size of the point's neighbourhood."""
        if 0 < i < self.size[0] - 1 and 0 < j < self.size[1] - 1:
            return 9
        elif (i == 0 or i == self.size[0] - 1) and (j == 0 or j == self.size[1] - 1):
            return 4
        else:
            return 6

    def assign_to_hood(self, x, y, val):
        """Assign val to entire neighbourhood of point (including point i, j)."""
        count = 0
        for i in range(max(0, x - 1), min(x + 2, self.size[0])):
            for j in range(max(0, y - 1), min(y + 2, self.size[1])):
                if self.solution[i, j] not in [-1, 1]:
                    self.solution[i, j] = val
                    count += 1
        return count

    def is_solved(self):
        count = 0
        for i in range(0, self.size[0]):
            for j in range(0, self.size[1]):
                if self.solution[i, j] == 0:
                    count += 1
        if count == 0:
            return True
        else:
            return False

    def correct_fill(self):
        for i in range(0, self.size[0]):
            for j in range(0, self.size[1]):
                el = self.puzzle[i, j]
                if el < 10:
                    if self.filled_sure(i, j) > el:
                        return False
                    if self.size_of_hood(i, j) - self.empty_sure(i, j) < el:
                        return False
        return True

    def print_solution(self):
        """Prints solution, for visual testing."""
        # for row in self.solution:
        #     txt = ''
        #     for el in row:
        #         if el in [0, 1]:
        #             txt += '  {}'.format(el)
        #         else:
        #             txt += ' {}'.format(el)
        #     print(txt)
        print()
        txt = ''
        for row in self.solution:
            for el in row:
                if el == -1:
                    txt += ' .'
                elif el == 1:
                    txt += ' *'
                else:
                    txt += ' -'
            txt += '\n'
        print(txt)
        return txt
