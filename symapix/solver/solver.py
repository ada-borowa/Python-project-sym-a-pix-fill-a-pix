#!/usr/bin/env python3
""" Sym-a-pix: Solving puzzle
"""
import numpy as np
import math
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
        # for i in range(1, limit):
        count = 1
        while count > 0:
            count = self.find_blocked_regions()
            self.check_closed()
            self.fill_smallest()
            self.check_closed()
        if self.is_solved():
            self.correct_solution()

    def init_fill(self):
        """Fills obvious lines between two dots: if two squares contain dot or part of dot there is line."""
        for x in range(0, self.size[0], 2):
            for y in range(0, self.size[1], 2):
                if self.contains_dot(x, y):
                    adjacent = adjacent_squares(x, y)
                    for pair in adjacent:
                        if self.is_inside(*pair):
                            i, j = pair
                            if self.contains_dot(i, j) and not self.is_same_dot(x, y, i, j):
                                a, b = wall_between(x, y, i, j)
                                self.solution[a, b] = 1

    def contains_dot(self, x, y):
        """Checks if square contains dot or part of a dot
        or checks if line contains dot or part of a dot."""
        if not self.is_inside(x, y):
            return False
        if x % 2 == 0 and y % 2 == 0:
            for i in range(max(x - 1, 0), min(x + 2, self.size[0])):
                for j in range(max(y - 1, 0), min(y + 2, self.size[1])):
                    if self.puzzle[i, j] > 0:
                        return True
        elif x % 2 == 0:
            for j in range(y - 1, y + 2):
                if self.puzzle[x, j] > 0:
                    return True
        elif y % 2 == 0:
            for i in range(x - 1, x + 2):
                if self.puzzle[i, y] > 0:
                    return True
        return False

    def dot_in_corner(self, x, y, i, j):
        """Checks if any corner of square has dot"""
        if x % 2 > 0 or y % 2 > 0:
            return [-1, -1]
        corners = []
        if x == i:
            corners = [[x - 1, int((y + j) / 2)], [x + 1, int((y + j) / 2)]]
        elif y == j:
            corners = [[int((x + i) / 2), y - 1], [int((x + i) / 2), y + 1]]
        for c in corners:
            if self.is_inside(*c) and self.puzzle[c[0], c[1]] > 0:
                return c
        return [-1, -1]

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
                if self.puzzle[i, j] > 0:
                    dots.append([i, j])
        return dots

    def fill_smallest(self):
        """Fils the smallest blocks (1, 2 or 4 squares depending on where dot is)."""
        count = 0
        for x in range(0, self.size[0]):
            for y in range(0, self.size[1]):
                if self.puzzle[x, y] > 0:
                    frame = define_frame(x, y)
                    for wall in frame:
                        if self.is_wall(*wall):
                            a, b = symmetric_point(x, y, wall[0], wall[1])
                            if 0 <= a < self.size[0] and 0 <= b < self.size[1]:
                                self.solution[a, b] = 1
                                count += 1
        return count

    def fill(self, k):
        """Fills to length of k"""
        count = 0
        for i, row in enumerate(self.solution):
            for j, el in enumerate(row):
                if self.puzzle[i, j] > 0 and not closest_closed(i, j, self.solution):
                    count += self.fill_from_dot(i, j, k)
        return count

    def fill_from_dot(self, i, j, k=0, block=[]):
        """
        Fills block from given dot.
        :param block: if not empty, function can use only points in block
        :param k: describes how far from dot algorithm will attempt to fill puzzle
        :param i: position
        :param j: position
        :return: how many walls were put in
        """
        count = 0
        queue = define_block(i, j)
        visited = []
        no_queue = False
        while queue:
            p = queue.pop()
            visited.append(p)
            next_ones = []
            for n in adjacent_squares(p[0], p[1]):
                if 0 < k < point_dist(n[0], n[1], i, j):
                    no_queue = True
                wall = wall_between(n[0], n[1], p[0], p[1])
                if n not in visited:
                    if len(block) > 0:
                        if n in block:
                            if not (self.is_inside(*wall) and self.puzzle[wall[0], wall[1]] > 0) \
                                    and not (self.is_inside(*n) and self.solution[n[0], n[1]] < 0):
                                next_ones.append(n)
                    else:
                        if not (self.is_inside(*wall) and self.puzzle[wall[0], wall[1]] > 0) \
                                and not (self.is_inside(*n) and self.puzzle[n[0], n[1]] > 0):
                            next_ones.append(n)
            for n in next_ones:
                n_sym = symmetric_point(i, j, n[0], n[1])
                p_sym = symmetric_point(i, j, p[0], p[1])
                new_wall = wall_between(p_sym[0], p_sym[1], n_sym[0], n_sym[1])
                curr_wall = wall_between(p[0], p[1], n[0], n[1])
                if self.is_wall(*curr_wall) and \
                        self.is_inside(*new_wall) and not (self.is_wall(*new_wall)
                                                           or self.puzzle[new_wall[0], new_wall[1]] > 0):
                    self.solution[new_wall[0], new_wall[1]] = 1
                    count += 1
                if self.is_wall(*new_wall) and \
                        self.is_inside(*curr_wall) and not (self.is_wall(*curr_wall)
                                                            or self.puzzle[curr_wall[0], curr_wall[1]] > 0):
                    self.solution[curr_wall[0], curr_wall[1]] = 1
                    count += 1
            if not no_queue:
                for n in next_ones:
                    curr_wall = wall_between(p[0], p[1], n[0], n[1])
                    if not self.is_wall(*curr_wall) and \
                            self.is_inside(*n) and self.solution[n[0], n[1]] < 1:
                        queue.append(n)

        if self.puzzle[i, j] > 0:
            block = get_unique(np.array(visited))
            if self.block_is_closed(block, self.solution):
                for b in block:
                    self.solution[b[0], b[1]] = self.puzzle[i, j]

        return count

    def check_closed(self):
        """
        Checks if there are new closed blocks.
        :param user: if True, sets user solution, otherwise game's solution
        :return: None
        """
        for i, row in enumerate(self.solution):
            for j, el in enumerate(row):
                if self.puzzle[i, j] > 0 and not closest_closed(i, j, self.solution):
                    queue = define_block(i, j)
                    visited = []
                    while queue:
                        p = queue.pop()
                        visited.append(p)
                        next_ones = adjacent_squares(p[0], p[1])
                        for n in next_ones:
                            if self.is_inside(*n) and not self.puzzle[n[0], n[1]] < 0 and \
                                    not self.is_wall(*wall_between(p[0], p[1], n[0], n[1])) and \
                                    not n in visited:
                                n_sym = symmetric_point(i, j, n[0], n[1])
                                p_sym = symmetric_point(i, j, p[0], p[1])
                                if (self.is_inside(*n_sym) and self.is_inside(*p_sym)) and \
                                        not self.puzzle[n_sym[0], n_sym[1]] < 0 or \
                                        not self.is_wall(*wall_between(p_sym[0], p_sym[1], n_sym[0], n_sym[1])):
                                    queue.append(n)
                    if self.puzzle[i, j] > 0:
                        block = get_unique(np.array(visited))
                        if self.block_is_closed(block, self.solution):
                            for b in block:
                                self.solution[b[0], b[1]] = self.puzzle[i, j]

    def find_blocked_regions(self):
        """Finds parts of blocks with all walls checked and one dot.
        Then fills symmetric part of that block."""
        count = 0
        for i, row in enumerate(self.solution):
            for j, el in enumerate(row):
                if i % 2 == 0 and j % 2 == 0 and el == 0:
                    queue = []
                    dots = []
                    visited = [[i, j]]

                    for p in adjacent_squares(i, j):
                        pos_wall = wall_between(i, j, p[0], p[1])
                        cor_dot = self.dot_in_corner(i, j, p[0], p[1])
                        if self.is_inside(*pos_wall) and self.puzzle[pos_wall[0], pos_wall[1]] > 0:
                            dots.append(pos_wall)
                        elif not self.is_wall(*pos_wall) and self.is_inside(*p) and self.puzzle[p[0], p[1]] > 0:
                            dots.append(p)
                        elif not self.is_wall(*pos_wall):
                            queue.append(p)
                        if not cor_dot == [-1, -1]:
                            dots.append(cor_dot)
                    while queue:
                        p = queue.pop()
                        sym_part = False
                        if len(dots) == 1:
                            for d in dots:
                                s = symmetric_point(d[0], d[1], p[0], p[1])
                                if [s[0], s[1]] in visited:
                                    sym_part = True
                        if not sym_part:
                            visited.append(p)
                            next_ones = adjacent_squares(p[0], p[1])
                            for n in next_ones:
                                pos_wall = wall_between(p[0], p[1], n[0], n[1])
                                if n not in visited and not self.is_wall(*pos_wall):
                                    corner_dot = self.dot_in_corner(n[0], n[1], p[0], p[1])
                                    if self.is_inside(*pos_wall) and self.puzzle[pos_wall[0], pos_wall[1]] > 0 \
                                            and pos_wall not in dots:
                                        dots.append(pos_wall)
                                    elif self.is_inside(*n) and self.puzzle[n[0], n[1]] > 0 and n not in dots:
                                        dots.append(n)
                                    elif self.is_inside(*n) and n not in visited and n not in dots:
                                        queue.append(n)
                                    if not corner_dot == [-1, -1] and corner_dot not in dots:
                                        dots.append(corner_dot)
                    block = get_unique(np.array(visited))
                    if len(dots) == 1 and len(block) > 0:
                        dot = dots[0]
                        count += self.fill_from_dot(dot[0], dot[1], k=0, block=block)
                    elif len(dots) > 1 and len(block) > 0:
                        self.test_dots(i, j, dots)
        return count

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

    def test_dots(self, x, y, dots):
        """
        Tests from x, y to dots if it can be filled
        :param x: starting position
        :param y: starting position
        :param dots: list of dots to be tested
        :return:
        """
        ok_dots = []
        for d in dots:
            p = symmetric_point(d[0], d[1], x, y)
            if self.is_inside(*p) and self.solution[p[0], p[1]] == 0:
                ok_dots.append(d)
        if len(ok_dots) == 1:
            d = ok_dots[0]
            walls = define_frame(x, y)
            for w in walls:
                sym_w = symmetric_point(d[0], d[1], w[0], w[1])
                if self.is_wall(*w) and self.is_inside(*sym_w):
                    self.solution[sym_w[0], sym_w[1]] = 1
                elif self.is_wall(*sym_w) and self.is_inside(*w):
                    self.solution[w[0], w[1]] = 1

    def is_wall(self, x, y, user=False):
        """Checks if point is wall."""
        if user:
            array = self.user_solution
        else:
            array = self.solution
        if x in [-1, self.size[0]]:
            return True
        elif y in [-1, self.size[1]]:
            return True
        elif 0 <= x < self.size[0] and 0 <= y < self.size[1] and array[x, y] == 1:
            return True
        return False

    def is_inside(self, i, j):
        if 0 <= i < self.size[0] and 0 <= j < self.size[1]:
            return True
        else:
            return False

    def is_solved(self):
        """Checks if puzzle is finished: if all squares are -2 or -3"""
        for i in range(0, self.size[0], 2):
            for j in range(0, self.size[1], 2):
                if self.solution[i, j] == 0:
                    return False
        return True

    def correct_solution(self):
        """Corrects solution."""
        for i in range(0, self.size[0]):
            for j in range(0, self.size[1]):
                if self.puzzle[i, j] > 0:
                    queue = define_block(i, j)
                    visited = []
                    while queue:
                        q = queue.pop()
                        visited.append(q)
                        for p in adjacent_squares(*q):
                            p_sym = symmetric_point(i, j, *p)
                            q_sym = symmetric_point(i, j, *q)
                            pos_wall = wall_between(p[0], p[1], q[0], q[1])
                            sym_wall = wall_between(p_sym[0], p_sym[1], q_sym[0], q_sym[1])
                            if not self.is_wall(*pos_wall) and not self.is_wall(*sym_wall) and p not in visited:
                                queue.append(p)
                            elif self.is_wall(*pos_wall) and not self.is_wall(*sym_wall):
                                self.solution[sym_wall[0], sym_wall[1]] = 1
                            elif not self.is_wall(*pos_wall) and self.is_wall(*sym_wall):
                                self.solution[pos_wall[0], pos_wall[1]] = 1
                    block = get_unique(visited)
                    for b in block:
                        self.solution[b[0], b[1]] = self.puzzle[i, j]

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

    def clear_user_board(self):
        for i in range(0, self.size[0], 2):
            for j in range(0, self.size[1], 2):
                self.user_solution[i, j] = 0

    def set_user_value(self, x, y, val):
        """Sets value chosen by user."""
        self.clear_user_board()
        self.user_solution[x, y] = val
        self.update_user_filling()

    def update_user_filling(self):
        """Updates blcoked regions and fills/unfills them."""
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if self.puzzle[i, j] > 0:
                    block = []
                    if self.block_is_closed(define_block(i, j), self.user_solution):
                        block = define_block(i, j)
                    else:
                        queue = define_block(i, j)
                        visited = []
                        search = True
                        while queue and search:
                            p = queue.pop()
                            visited.append(p)
                            next_ones = adjacent_squares(p[0], p[1])
                            for n in next_ones:
                                if self.is_inside(*n) and n not in visited:
                                    if not self.is_wall(*wall_between(p[0], p[1], n[0], n[1]), True):
                                        queue.append(n)
                                    if self.puzzle[n[0], n[1]] > 0 and \
                                            not self.is_wall(*wall_between(p[0], p[1], n[0], n[1])):
                                        search = False
                                        break
                        if search:
                            block = get_unique(np.array(visited))
                    if len(block) > 0:
                        if self.block_is_closed(block, self.user_solution):
                            for b in block:
                                self.user_solution[b[0], b[1]] = self.puzzle[i, j]
        for i, row in enumerate(self.user_solution):
            for j, el in enumerate(row):
                self.fill_color[i, j] = el if i % 2 == 0 and j % 2 == 0 and el > 0 else 0

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
                if not (i % 2 == 0 and j % 2 == 0) and not (i % 2 > 0 and j % 2 > 0):
                    if self.solution[i, j] != self.user_solution[i, j] and self.user_solution[i, j] != 0:
                        if i % 2 == 0:
                            i /= 2
                        else:
                            i = (i - 1)/2
                        if j % 2 == 0:
                            j /= 2
                        else:
                            j = (j - 1)/2
                        return int(i), int(j)
        return -1, -1

    def is_solved_by_user(self):
        """Checks if puzzle is solved by user."""
        count = 0
        for i in range(0, self.size[0]):
            for j in range(0, self.size[1]):
                if not (i % 2 == 0 and j % 2 == 0) and not (i % 2 > 0 and j % 2 > 0):
                    if self.user_solution[i, j] != self.solution[i, j]:
                        count += 1
        if count == 0:
            return True
        else:
            return False
