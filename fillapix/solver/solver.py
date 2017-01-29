# !/usr/bin/env python3
""" Fill-a-pix: Solving puzzle
"""

import numpy as np
import math
import copy
from operator import xor

from common.misc import get_unique

__author__ = 'Adriana Borowa'
__email__ = 'ada.borowa@gmail.com'


class FillAPixSolver:
    """ Solver class. """

    def __init__(self, puzzle):
        """Solver initialization.
        :param: puzzle: puzzle container
        """
        if puzzle is None:
            self.puzzle = np.zeros((10, 10), int)
        else:
            self.puzzle = puzzle.get_board()
        self.size = self.puzzle.shape
        self.solution = np.zeros(self.size, int)
        self.probability = np.zeros(self.size, float)
        self.user_solution = np.zeros(self.size, int)

    def set_puzzle(self, array):
        """Setting puzzle board; just for tests."""
        self.puzzle = array
        self.size = self.puzzle.shape
        self.solution = np.zeros(self.size, int)

    def set_solution(self, array):
        """
        Sets solution, only for generated puzzles
        :param array: array with solution to generated puzzle
        :return: None
        """
        self.solution = array

    def solve(self):
        """Solver:
        1. Fills obvious: 0 and 9, 4 in corners, 6 on borders.
        2. Checks for pairs of 3s on borders, and 2s in corners.
        3. Goes from 8 to 1 and checks if there are obvious points.
        4. Checks for 2 clue logic
        5. Checks for 3 clue logic"""
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
                if i in [0, self.size[0] - 1] or j in [0, self.size[1] - 1]:
                    self.special_case(i, j)
        self.fill()
        count = 1
        while not self.is_solved():
            self.fill()
            self.find_clues()
            self.fill()
            if count % 5 == 0:
                self.random_solver()
            self.correct_solution()
            if count > 39:
                break
            count += 1

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

    def find_clues(self):
        """Find 3 types of clues."""
        for i in range(0, self.size[0]):
            for j in range(0, self.size[1]):
                if self.puzzle[i, j] < 10:
                    self.find_2_clue_logic(i, j)
                    self.find_3_clue_logic(i, j)
                    self.find_ASA(i, j)

    def find_2_clue_logic(self, x, y):
        """Finds advanced 2 clue logic for point x, y if possible:
        1. Points directly next to each other
        2. Point not next to each other (one point between them)."""
        el1 = self.puzzle[x, y]
        if el1 == 100:
            return
        # directly to each other
        for i in range(max(0, x - 1), min(x + 2, self.size[0])):
            for j in range(max(0, y - 1), min(y + 2, self.size[1])):
                el1 = self.puzzle[x, y]
                el1_hood = [(a, b) for a in range(max(0, x - 1), min(x + 2, self.size[0]))
                            for b in range(max(0, y - 1), min(y + 2, self.size[1]))]
                if (i != x or j != y) and self.puzzle[i, j] < 10:
                    el2 = self.puzzle[i, j]
                    el2_hood = [(a, b) for a in range(max(0, i - 1), min(i + 2, self.size[0]))
                                for b in range(max(0, j - 1), min(j + 2, self.size[1]))]
                    intersection = [a for a in set(el1_hood + el2_hood) if
                                    a in el1_hood and a in el2_hood]
                    el1_alone = [a for a in el1_hood if a not in intersection if self.solution[a] != -1]
                    el2_alone = [a for a in el2_hood if a not in intersection if self.solution[a] != -1]
                    el1 -= len([a for a in el1_alone if self.solution[a] == 1])
                    el2 -= len([a for a in el2_alone if self.solution[a] == 1])
                    if el1 > el2 and len(el1_alone) == math.fabs(el1 - el2):
                        self.assign_to_array(el1_alone, 1)
                        self.assign_to_array(el2_alone, -1)
                    elif el1 < el2 and len(el2_alone) == math.fabs(el1 - el2):
                        self.assign_to_array(el1_alone, -1)
                        self.assign_to_array(el2_alone, 1)

        # not directly next to each other
        for i in range(max(0, x - 2), min(x + 3, self.size[0])):
            for j in range(max(0, y - 2), min(y + 3, self.size[1])):
                el1 = self.puzzle[x, y]
                el1_hood = [(a, b) for a in range(max(0, x - 1), min(x + 2, self.size[0]))
                            for b in range(max(0, y - 1), min(y + 2, self.size[1]))]
                if (i not in range(max(0, x - 1), min(x + 2, self.size[0])) or
                   j not in range(max(0, y - 1), min(y + 2, self.size[1]))) and \
                   self.puzzle[i, j] < 10:
                    el2 = self.puzzle[i, j]
                    el2_hood = [(a, b) for a in range(max(0, i - 1), min(i + 2, self.size[0]))
                                for b in range(max(0, j - 1), min(j + 2, self.size[1]))]
                    intersection = [a for a in set(el1_hood + el2_hood) if
                                    a in el1_hood and a in el2_hood]
                    el1_alone = [a for a in el1_hood if a not in intersection if self.solution[a] != -1]
                    el2_alone = [a for a in el2_hood if a not in intersection if self.solution[a] != -1]
                    el1 -= len([a for a in el1_alone if self.solution[a] == 1])
                    el2 -= len([a for a in el2_alone if self.solution[a] == 1])
                    if el1 > el2 and len(el1_alone) == math.fabs(el1 - el2):
                        self.assign_to_array(el1_alone, 1)
                        self.assign_to_array(el2_alone, -1)
                    elif el1 < el2 and len(el2_alone) == math.fabs(el1 - el2):
                        self.assign_to_array(el1_alone, -1)
                        self.assign_to_array(el2_alone, 1)

    def find_3_clue_logic(self, x, y, case1=True):
        """Finds 3 clue logic for point x, y (if possible)."""
        el1 = self.puzzle[x, y]
        if el1 == 100:
            return
        # first case
        neighbours = self.get_neighbours(x, y, True)
        if len(neighbours) >= 2:
            neighbours_pairs = get_unique(np.array([(a, b) for a in neighbours for b in neighbours if a != b]))
            for pair in neighbours_pairs:
                el2_x, el2_y = pair[0]
                el3_x, el3_y = pair[1]
                el1_hood = [(a, b) for a in range(max(0, x - 1), min(x + 2, self.size[0]))
                            for b in range(max(0, y - 1), min(y + 2, self.size[1]))]
                el2 = self.puzzle[el2_x, el2_y]
                el2_hood = [(a, b) for a in range(max(0, el2_x - 1), min(el2_x + 2, self.size[0]))
                            for b in range(max(0, el2_y - 1), min(el2_y + 2, self.size[1]))]
                el3 = self.puzzle[el3_x, el3_y]
                el3_hood = [(a, b) for a in range(max(0, el3_x - 1), min(el3_x + 2, self.size[0]))
                            for b in range(max(0, el3_y - 1), min(el3_y + 2, self.size[1]))]
                A_only = get_unique(np.array([a for a in el1_hood if a not in el2_hood and a not in el3_hood]))
                B_but_not_A = get_unique(np.array([a for a in el2_hood + el3_hood if a not in el1_hood]))
                A_and_all_B = get_unique(np.array([a for a in el1_hood if a in el2_hood and a in el3_hood]))
                if el1 == len(A_only) + el2 + el3:
                    self.assign_to_array(A_only, 1)
                    self.assign_to_array(B_but_not_A, -1)
                    self.assign_to_array(A_and_all_B, -1)
        # second case
        if case1:
            neighbours = self.get_neighbours(x, y, False)
            if len(neighbours) >= 2:
                neighbours_pairs = get_unique(np.array([(a, b) for a in neighbours for b in neighbours if a != b]))
                for pair in neighbours_pairs:
                    el2_x, el2_y = pair[0]
                    el3_x, el3_y = pair[1]
                    el1_hood = [(a, b) for a in range(max(0, x - 1), min(x + 2, self.size[0]))
                                for b in range(max(0, y - 1), min(y + 2, self.size[1]))]
                    el2 = self.puzzle[el2_x, el2_y]
                    el2_hood = [(a, b) for a in range(max(0, el2_x - 1), min(el2_x + 2, self.size[0]))
                                for b in range(max(0, el2_y - 1), min(el2_y + 2, self.size[1]))]
                    el3 = self.puzzle[el3_x, el3_y]
                    el3_hood = [(a, b) for a in range(max(0, el3_x - 1), min(el3_x + 2, self.size[0]))
                                for b in range(max(0, el3_y - 1), min(el3_y + 2, self.size[1]))]
                    el2 -= len([a for a in el2_hood if a not in el1_hood and self.solution[a] == 1])
                    el3 -= len([a for a in el3_hood if a not in el1_hood and self.solution[a] == 1])
                    A_only = get_unique(np.array([a for a in el1_hood if a not in el2_hood and a not in el3_hood]))
                    B_but_not_A = get_unique(np.array([a for a in el2_hood + el3_hood
                                                       if a not in el1_hood and self.solution[a] == 0]))
                    A_and_one_B = get_unique(np.array([a for a in el1_hood if xor(a in el2_hood, a in el3_hood)]))
                    # A_and_all_B = get_unique(np.array([a for a in el1_hood if a in el2_hood + el3_hood]))
                    if el1 == el2 + el3 and len(B_but_not_A) == 0 and el1 < len(A_and_one_B):
                        self.assign_to_array(A_only, -1)

    def find_ASA(self, x, y):
        """Find 3 clue logic of type ASA, for example: _ 2 6 _ 4 _"""
        el1 = self.puzzle[x, y]
        if el1 == 100:
            return
        el1_hood = [(a, b) for a in range(max(0, x - 1), min(x + 2, self.size[0]))
                    for b in range(max(0, y - 1), min(y + 2, self.size[1]))]
        hood = []
        if 1 < x < self.size[0] - 2 and self.puzzle[x - 1, y] + self.puzzle[x + 2, y] == el1:
            hood = [(a, b) for a in range(max(x - 2, 0), min(x + 4, self.size[0]))
                    for b in range(max(0, y - 1), min(y + 2, self.size[1]))]
        elif 2 < x < self.size[0] - 1 and self.puzzle[x + 1, y] + self.puzzle[x - 2, y] == el1:
            hood = [(a, b) for a in range(max(x - 3, 0), min(x + 3, self.size[0]))
                    for b in range(max(0, y - 1), min(y + 2, self.size[1]))]
        elif 1 < y < self.size[1] - 2 and self.puzzle[x, y - 1] + self.puzzle[x, y + 2] == el1:
            hood = [(a, b) for a in range(max(x - 1, 0), min(x + 2, self.size[0]))
                    for b in range(max(y - 2, 0), min(y + 4, self.size[1]))]
        elif 2 < y < self.size[1] - 1 and self.puzzle[x, y + 1] + self.puzzle[x, y - 2] == el1:
            hood = [(a, b) for a in range(max(x - 1, 0), min(x + 2, self.size[0]))
                    for b in range(max(y - 4, 0), min(y + 2, self.size[1]))]
        to_insert = [a for a in hood if a not in el1_hood]
        self.assign_to_array(to_insert, -1)

    def random_solver(self):
        queue = []
        for i in range(0, self.size[0]):
            for j in range(0, self.size[1]):
                if self.puzzle[i, j] - self.filled_sure(i, j) == 1:
                    queue.append([i, j])
        if len(queue) == 0:
            return

        q = queue[np.random.randint(0, len(queue))]
        queue2 = []
        for n in self.get_hood(*q):
            if self.solution[n[0], n[1]] == 0:
                queue2.append(n)
        for n in queue2:
            old_solution = copy.deepcopy(self.solution)
            self.solution[n[0], n[1]] = 1
            self.fill()
            self.find_clues()
            self.fill()
            if type(self.correct_fill()) == bool:
                break
            else:
                self.solution = copy.deepcopy(old_solution)

    def get_neighbours(self, x, y, close):
        """
        Checks if points has 2 neighbours - for 3 clue logic
        :param x: position
        :param y: position
        :param close: boolean, True if function is expected to check closes neighbours, False if 2 points away
        :return: neighbours
        """
        neighbours = []
        if close:
            for i in range(max(0, x - 1), min(x + 2, self.size[0])):
                for j in range(max(0, y - 1), min(y + 2, self.size[1])):
                    if (i != x or j != y) and self.puzzle[i, j] < 10:
                        neighbours.append([i, j])
        else:
            for i in range(max(0, x - 2), min(x + 3, self.size[0])):
                for j in range(max(0, y - 2), min(y + 3, self.size[1])):
                    if (i not in range(max(0, x - 1), min(x + 2, self.size[0])) or
                     j not in range(max(0, y - 1), min(y + 2, self.size[1]))) and self.puzzle[i, j] < 10:
                        neighbours.append([i, j])
        return neighbours

    def get_hood(self, x, y):
        return [[a, b] for a in range(max(0, x - 1), min(x + 2, self.size[0]))
                for b in range(max(0, y - 1), min(y + 2, self.size[1]))]

    def special_case(self, x, y):
        """Checks for special case: two 3: one on border, one next to it not on border,
        two 2: one in corner, one on border"""
        if self.puzzle[x, y] == 2:
            if x == 0 and y == 0:
                if self.puzzle[x + 1, y] == 2:
                    self.solution[x + 2, 0: 2] = -1
                if self.puzzle[x, y + 1] == 2:
                    self.solution[0: 2, y + 2] = -1
            if x == 0 and y == self.size[1] - 1:
                if self.puzzle[x + 1, y] == 2:
                    self.solution[x + 2, self.size[1] - 2: self.size[1]] = -1
                if self.puzzle[x, y - 1] == 2:
                    self.solution[0: 2, y - 2] = -1
            if x == self.size[0] - 1 and y == 0:
                if self.puzzle[x - 1, y] == 2:
                    self.solution[x - 2, 0: 2] = -1
                if self.puzzle[x, y + 1] == 2:
                    self.solution[self.size[0] - 2: self.size[0], y + 2] = -1
            if x == self.size[0] - 1 and y == self.size[1] - 1:
                if self.puzzle[x - 1, y] == 2:
                    self.solution[x - 2, self.size[1] - 2: self.size[1]] = -1
                if self.puzzle[x, y - 1] == 2:
                    self.solution[self.size[0] - 2: self.size[0], y - 2] = -1

        elif self.puzzle[x, y] == 3 and (
                        x in [0, self.size[0] - 1] or y in [0, self.size[1] - 1]):
            if x == 0 and 0 < y < self.size[1] - 1 and self.puzzle[x + 1, y] == 3:
                self.solution[x + 2, y - 1: y + 2] = -1
            if x == self.size[0] - 1 and 0 < y < self.size[1] - 1 and self.puzzle[
                        x - 1, y] == 3:
                self.solution[x - 2, y - 1: y + 2] = -1
            if 0 < x < self.size[0] - 1 and y == 0 and self.puzzle[x, y + 1] == 3:
                self.solution[x - 1: x + 2, y + 2] = -1
            if 0 < x < self.size[0] - 1 and y == self.size[1] - 1 and self.puzzle[
                x, y - 1] == 3:
                self.solution[x - 1: x + 2, y - 2] = -1

    def filled_sure(self, x, y):
        """
        Counts how many neighbours of point are for sure filled.
        :param x: position
        :param y: position
        :return: number of filled neighbours
        """
        count = 0
        for i in range(max(0, x - 1), min(x + 2, self.size[0])):
            for j in range(max(0, y - 1), min(y + 2, self.size[1])):
                if self.solution[i, j] == 1:
                    count += 1
        return count

    def empty_sure(self, x, y):
        """
        Counts how many neighbours of point are for sure unfilled.
        :param x: position
        :param y: position
        :return: number of unfilled neighbours
        """
        count = 0
        for i in range(max(0, x - 1), min(x + 2, self.size[0])):
            for j in range(max(0, y - 1), min(y + 2, self.size[1])):
                if self.solution[i, j] == -1:
                    count += 1
        return count

    def unsure_in_array(self, array):
        """
        Counts how many neighbours of point are for neither for sure filled nor unfilled
        :param x: position
        :param y: position
        :return: number of unsure neighbours
        """
        count = 0
        for el in array:
            if self.solution[el] == 0:
                count += 1
        return count

    def size_of_hood(self, i, j):
        """
        Size of point's neighbourhood.
        :param i: position
        :param j: position
        :return: number of neighbours
        """
        if 0 < i < self.size[0] - 1 and 0 < j < self.size[1] - 1:
            return 9
        elif (i == 0 or i == self.size[0] - 1) and (j == 0 or j == self.size[1] - 1):
            return 4
        else:
            return 6

    def assign_to_hood(self, x, y, val):
        """
        Assign val to entire neighbourhood of point (including point i, j).
        :param x: position
        :param y: position
        :param val: value to be assigned
        :return: how many points were assigned
        """
        count = 0
        for i in range(max(0, x - 1), min(x + 2, self.size[0])):
            for j in range(max(0, y - 1), min(y + 2, self.size[1])):
                if self.solution[i, j] not in [-1, 1]:
                    self.solution[i, j] = val
                    count += 1
        return count

    def reset_hood(self, x, y):
        """Resets values in neighbourhood to 0."""
        for i in range(max(0, x - 1), min(x + 2, self.size[0])):
            for j in range(max(0, y - 1), min(y + 2, self.size[1])):
                self.solution[i, j] = 0

    def assign_to_array(self, array, val):
        """
        Assign val to array of points.
        :param array: array to be filled
        :param val: value to be assigned
        :return: how many points were assigned
        """
        count = 0
        for x, y in array:
            if self.solution[x, y] == 0:
                self.solution[x, y] = val
                count += 1
        return count

    def is_solved(self):
        """Checks if puzzle is solved."""
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
        """Checks if current filling is correct."""
        for i in range(0, self.size[0]):
            for j in range(0, self.size[1]):
                el = self.puzzle[i, j]
                if el < 10:
                    if self.filled_sure(i, j) > el:
                        return i, j
                    elif self.empty_sure(i, j) > self.size_of_hood(i, j) - el:
                        return i, j
        return True

    def correct_solution(self):
        while type(self.correct_fill()) is not bool:
            self.reset_hood(*self.correct_fill())

    def print_solution(self):
        """Prints solution, for visual testing."""
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

    def get_solution(self):
        """Getter for solution."""
        return self.solution

    def get_user_solution(self):
        """Getter for user's solution."""
        return self.user_solution

    def get_user_value(self, i, j):
        """Getter for user chosen value in point."""
        return self.user_solution[i, j]

    def set_user_value(self, x, y, val):
        """Sets user chosen value."""
        self.user_solution[x, y] = val

    def set_solved(self):
        """Sets user's solution to solution."""
        self.user_solution = copy.deepcopy(self.solution)

    def clear_user_solution(self):
        """Resets user's solution."""
        self.user_solution = np.zeros(self.size, int)

    def check_user_solution(self):
        """Checks if user's solution is currently correct. Omits unfilled points."""
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
