#!/usr/bin/env python3
""" Container for puzzle.
"""

import numpy as np

import common.misc as misc

__author__ = 'Adriana Borowa'
__email__ = 'ada.borowa@gmail.com'


class Generator:
    """Generator class for sym-a-pix puzzle."""
    def __init__(self, solver, container):
        self.solver = solver
        self.container = container
        self.size = self.container.size
        self.colors = len(self.container.colors)

    def generate_random(self):
        """
        Generates random sym-a-pix puzzle.
        :returns: None"""
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if self.solver.solution[i, j] == 0 and np.random.random() < 0.25:
                    c = np.random.randint(1, self.colors + 1)
                    if self.populate(i, j):
                        self.container.puzzle[i, j] = c
                        self.solver.solution[i, j] = -2

    def correct_lines(self):
        """Checks if lines were not put in place of dot."""
        for i in range(0, self.size[0]):
            for j in range(0, self.size[1]):
                if not (i % 2 == 0 and j % 2 == 0) and not (i % 2 > 0 and j % 2 > 0):
                    if self.solver.puzzle[i, j] > 0:
                        self.solver.solution[i, j] = -2
                    [a, b], [c, d] = misc.squares_next_to(i, j)
                    corner_dot = self.solver.dot_in_corner(a, b, c, d)
                    if corner_dot != [-1, -1]:
                        self.solver.solution[i, j] = -2

    def populate(self, x, y):
        """
        Given point, creates symmetric shape around.
        :param x: position
        :param y: position
        :return: if it was successful
        """
        frame = misc.define_frame(x, y)
        closed = True
        for f in frame:
            if not self.solver.is_wall(*f):
                closed = False
        if closed:
            return closed
        visited = misc.define_block(x, y)
        for v in visited:
            if self.solver.contains_dot(*v):
                return False
        return True

    def remove_redundant_walls(self):
        """Removes any redundant walls inside blocks."""
        for i in range(0, self.size[0]):
            for j in range(0, self.size[1]):
                if self.solver.puzzle[i, j] > 0:
                    queue = misc.define_block(i, j)
                    visited = []
                    while queue:
                        q = queue.pop()
                        visited.append(q)
                        queue2 = misc.adjacent_squares(*q)
                        for q2 in queue2:
                            if q2 not in visited and \
                                not self.solver.is_wall(*misc.wall_between(q[0], q[1], q2[0], q2[1])) and \
                                    self.solver.is_inside(*q2):
                                queue.append(q2)

                    block = misc.get_unique(np.array(visited))
                    all_walls = []
                    for b in block:
                        all_walls.append(misc.define_frame(b[0], b[1]))
                    all_walls = np.array(all_walls).reshape(-1, 2)
                    red_walls = np.array([x for x in all_walls if misc.count(all_walls, x) > 1])
                    for w in red_walls:
                        self.solver.solution[w[0], w[1]] = 0

    def fill_dots(self):
        """Fills dots in empty blocks."""
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if i % 2 == 0 and j % 2 == 0 and self.solver.solution[i, j] == 0:
                    if self.fill_block(i, j, np.random.randint(1, self.colors + 1)):
                        return

    def fill_block(self, x, y, c):
        """
        Fills unfilled blocks in puzzle with dots.
        :param x: position
        :param y: position
        :param c: color to fill
        :return:
        """
        queue = misc.define_block(x, y)
        visited = []
        while queue:
            q = queue.pop()
            visited.append(q)
            queue2 = misc.adjacent_squares(*q)
            for q2 in queue2:
                if q2 not in visited and \
                    not self.solver.is_wall(*misc.wall_between(q[0], q[1], q2[0], q2[1])) and \
                        self.solver.is_inside(*q2):
                    queue.append(q2)

        block = misc.get_unique(np.array(visited))
        if len(block) == 1:
            b = block[0]
            self.solver.puzzle[b[0], b[1]] = c
            self.solver.solution[b[0], b[1]] = c
        elif len(block) == 2:
            new_dot = misc.wall_between(block[0][0], block[0][1], block[1][0], block[1][1])
            self.solver.puzzle[new_dot[0], new_dot[1]] = c
            self.solver.solution[block[0][0], block[0][1]] = c
            self.solver.solution[block[1][0], block[1][1]] = c
        else:
            # check if symmetric
            xs = [a[0] for a in block]
            ys = [a[1] for a in block]
            dot = [int((min(xs) + max(xs))/2), int((min(ys) + max(ys))/2)]
            symmetric = True
            for b in block:
                sym_b = misc.symmetric_point(dot[0], dot[1], b[0], b[1])
                if [sym_b[0], sym_b[1]] not in block.tolist():
                    symmetric = False
            if symmetric:
                self.solver.puzzle[dot[0], dot[1]] = c
                for b in block:
                    self.solver.solution[b[0], b[1]] = c
            else:
                new_dot = block[np.random.randint(len(block))]
                self.solver.puzzle[new_dot[0], new_dot[1]] = c
                return True
        return False



