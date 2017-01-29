#!/usr/bin/env python3
""" Container for puzzle.
"""

import cv2
import numpy as np
import pickle
import math
from classifiers import classifier

__author__ = 'Adriana Borowa'
__email__ = 'ada.borowa@gmail.com'


# Colors possible to use when creating random game.
COLORS = [[0, 0, 0], [255, 255, 255], [60, 69, 177],
          [17, 23, 105], [60, 133, 177], [127, 202, 247],
          [116, 75, 46], [69, 39, 16], [62, 135, 46],
          [113, 189, 97]]


def dist(x, y):
    """Turns bgr points to float, returns distance between points"""
    x = np.array(x, float)
    y = np.array(y, float)
    return math.sqrt((x[0]-y[0])**2 + (x[1] - y[1])**2 + (x[2] - y[2])**2)


class Container:
    """Stores puzzle data."""
    def __init__(self, size):
        """Initailization of container.
           :param: size: width and height of puzzle
           :returns: None
        """
        self.size = (size[0] * 2 - 1, size[1] * 2 - 1)
        # print(self.size)
        self.puzzle = np.zeros((self.size[0], self.size[1])) - 1
        self.colors = []
        self.sq_clf = pickle.load(classifier.get('square'))
        self.horiz_clf = pickle.load(classifier.get('horizontal'))
        self.vert_clf = pickle.load(classifier.get('vertical'))
        self.x_clf = pickle.load(classifier.get('x'))

    def set_puzzle(self, puzzle):
        """
        Sets puzzle from given array
        :param puzzle: new puzzle
        :return:
        """
        self.puzzle = puzzle

    def get_board(self):
        """Returns puzzle board."""
        return self.puzzle

    def set_colors(self, color):
        """Sets possible colors depending on number chosen by user."""
        self.colors = COLORS[: color]

    def insert(self, img_rgb, x, y, mode):
        """
        Inserts data into puzzle.
        :param img_rgb: fragment of full image to be processed in rgb
        :param x: position
        :param y: position
        :param mode: part of puzzle, 0 - window, 1 - horizontal line, 2 - vertical line, 3 - line crossing
        :return: None
        """
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        image = cv2.resize(img_gray, (20, 20))
        number = 0
        i, j = 0, 0
        if mode == 0:
            number = self.sq_clf.predict(image.reshape(1, -1))
            i = 2 * x
            j = 2 * y
        elif mode == 1:
            number = self.horiz_clf.predict(image.reshape(1, -1))
            i = 2 * x - 1
            j = 2 * y
        elif mode == 2:
            number = self.vert_clf.predict(image.reshape(1, -1))
            i = 2 * x
            j = 2 * y - 1
        elif mode == 3:
            number = self.x_clf.predict(image.reshape(1, -1))
            i = 2 * x - 1
            j = 2 * y - 1
        if number > 0:
            number = self.get_color(img_rgb)
        self.puzzle[i, j] = int(number)

    def print_puzzle(self):
        """
        Prints current puzzle.
        :return: None
        """
        for i, row in enumerate(self.puzzle):
            txt = ''
            for j, el in enumerate(row):
                if el == 0:
                    if i % 2 == 0 and j % 2 == 0:
                        txt += '  '
                    elif i % 2 == 0 and j % 2 > 0:
                        txt += '| '
                    elif i % 2 > 0 and j % 2 == 0:
                        txt += '_ '
                    elif i % 2 > 0 and j % 2 > 0:
                        txt += '+ '
                else:
                    txt += str(int(el)) + ' '
            print(txt)

    def get_color(self, img):
        """Reads color of dot on image and adds to list of colors (if color is not on it, yet)"""
        w, h, _ = img.shape
        color = img[int(w/2.0), int(h/2.0)]
        curr = 0
        if len(self.colors) == 0:
            self.colors.append(color)
            return 1
        for i, c in enumerate(self.colors):
            if dist(c, color) < 10:
                curr = i + 1
                break
        if curr == 0:
            self.colors.append(color)
            return len(self.colors)
        else:
            return curr

    def get_colors(self):
        """Returns list of colors."""
        return self.colors
