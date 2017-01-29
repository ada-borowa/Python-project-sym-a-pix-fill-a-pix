#!/usr/bin/env python3
""" Fill-a-pix: Processing operation on images - reading puzzle from image.
"""

import cv2

from common.imageops import get_line_positions
from fillapix.puzzle.container import Container

__author__ = 'Adriana Borowa'
__email__ = 'ada.borowa@gmail.com'


class FillAPixReader:
    """Reader for fill-a-pix puzzle."""
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
        self.rho_horizontal, self.rho_vertical = get_line_positions(self.img_gray, 150)
        puzzle = Container((len(self.rho_horizontal) - 1, len(self.rho_vertical) - 1))

        for i in range(len(self.rho_horizontal) - 1):
            for j in range(len(self.rho_vertical) - 1):
                puzzle.insert(self.cut_image(i, j), i, j)
        return puzzle

    def cut_image(self, x, y):
        """ Cuts part of an image depending on position of lines.
        :param x: position
        :param y: position
        :return: part of an image
        """
        img = self.img_gray[2 + self.rho_horizontal[x]: self.rho_horizontal[x + 1],
                            2 + self.rho_vertical[y]: self.rho_vertical[y + 1] - 1]
        return img

    def get_lines(self):
        """
        Used in visualization of puzzle.
        :return: number of lines of both types.
        """
        return len(self.rho_horizontal), len(self.rho_vertical)
