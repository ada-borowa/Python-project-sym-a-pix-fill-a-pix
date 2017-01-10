#!/usr/bin/env python3
""" Sym-a-pix: Processing operation on images - reading puzzle from image.
"""

import cv2

from common.imageops import get_line_positions
from symapix.puzzle.container import Container

__author__ = 'Adriana Borowa'
__email__ = 'ada.borowa@gmail.com'


class SymAPixReader:
    """Reader for sym-a-pix puzzle."""
    def __init__(self, filename):
        """ Reads puzzle from picture.
        :param filename: name of file with image of puzzle.
        :return: None
        """
        self.img_rgb = cv2.imread(filename, cv2.IMREAD_COLOR)
        if self.img_rgb is None:
            raise IOError('File not found')
        self.img_gray = cv2.cvtColor(self.img_rgb, cv2.COLOR_BGR2GRAY)
        self.img_edges = None
        self.rho_vertical = []
        self.rho_horizontal = []

    def create_puzzle(self):
        """
        Creates new puzzle. Detects lines on image.
        :return: puzzle
        """
        self.rho_horizontal, self.rho_vertical = get_line_positions(self.img_gray)
        puzzle = Container((len(self.rho_horizontal) - 1, len(self.rho_vertical) - 1))
        # normal
        for x in range(len(self.rho_horizontal) - 1):
            for y in range(len(self.rho_vertical) - 1):
                puzzle.insert(self.cut_image(x, y, 0), x, y, 0)
        # shifted in x
        for x in range(1, len(self.rho_horizontal) - 1):
            for y in range(len(self.rho_vertical) - 1):
                puzzle.insert(self.cut_image(x, y, 1), x, y, 1)
        # shifted in y
        for x in range(len(self.rho_horizontal) - 1):
            for y in range(1, len(self.rho_vertical) - 1):
                puzzle.insert(self.cut_image(x, y, 2), x, y, 2)
        # shifted in both
        for x in range(1, len(self.rho_horizontal) - 1):
            for y in range(1, len(self.rho_vertical) - 1):
                puzzle.insert(self.cut_image(x, y, 3), x, y, 3)
        return puzzle

    def cut_image(self, x, y, mode=0):
        """ Cuts part of an image depending on position of lines.
        :param x: position
        :param y: position
        :param mode: mode=0 - cuts normally, mode=1 cuts shifted in x, mode=2 cuts shifted in y, mode=3 cuts shifted
        in x and y
        :return: part of an image
        """
        if mode == 0:
            i1, i2 = 2 + self.rho_horizontal[x], self.rho_horizontal[x + 1] - 1
            j1, j2 = 2 + self.rho_vertical[y], self.rho_vertical[y + 1] - 1
        elif mode == 1:
            assert (0 < x < len(self.rho_horizontal) - 1)
            i1, i2 = 2 + (self.rho_horizontal[x - 1] + self.rho_horizontal[x]) / 2.0, \
                     (self.rho_horizontal[x] + self.rho_horizontal[x + 1]) / 2.0 - 1
            j1, j2 = 2 + self.rho_vertical[y], self.rho_vertical[y + 1] - 1
        elif mode == 2:
            assert (0 < y < len(self.rho_vertical) - 1)
            i1, i2 = 2 + self.rho_horizontal[x], self.rho_horizontal[x + 1] - 1
            j1, j2 = 2 + (self.rho_vertical[y - 1] + self.rho_vertical[y]) / 2.0 - 1, \
                     (self.rho_vertical[y] + self.rho_vertical[y + 1]) / 2.0 - 1
        elif mode == 3:
            assert(0 < x < len(self.rho_horizontal) - 1 and 0 < y < len(self.rho_vertical) - 1)
            i1, i2 = 2 + (self.rho_horizontal[x - 1] + self.rho_horizontal[x]) / 2.0, \
                     (self.rho_horizontal[x] + self.rho_horizontal[x + 1]) / 2.0 - 1
            j1, j2 = 2 + (self.rho_vertical[y - 1] + self.rho_vertical[y]) / 2.0 - 1, \
                     (self.rho_vertical[y] + self.rho_vertical[y + 1]) / 2.0 - 1
        else:
            i1, i2, j1, j2 = 0, 0, 0, 0
        i1, i2, j1, j2 = int(i1), int(i2), int(j1), int(j2)
        return self.img_rgb[i1: i2, j1: j2]

    def get_lines(self):
        """Used in visualization: return number of lines of both types."""
        return len(self.rho_horizontal), len(self.rho_vertical)
