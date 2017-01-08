#!/usr/bin/env python3
""" Common image operations.
"""

import numpy as np
import math
import cv2

__author__ = 'Adriana Borowa'
__email__ = 'ada.borowa@gmail.com'

DEGREE_VERTICAL = 0
DEGREE_HORIZONTAL = 1.5708
EPS = 0.0001


class IncorrectFileException(Exception):
    """ To be raised when puzzle is not a square.
    """
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


def get_unique_lines(rhos):
    """
    Joins lines that are to close to each other.
    :param rhos: list of line' positions
    :return: list without duplicates
    """
    rhos.sort()
    tmp = []
    it = 0
    while it < len(rhos) - 1:
        if rhos[it + 1] - rhos[it] < 3:
            tmp.append(int((rhos[it] + rhos[it+1])/2.0))
            it += 1
        else:
            tmp.append(int(rhos[it]))
        it += 1
    if rhos[-1] - tmp[-1] > 3:
        tmp.append(int(rhos[-1]))
    return tmp


def get_line_positions(img):
    """
    Using Hough transformation detects lines on image
    :param img: Image
    :return: positions of horizontal and vertical lines
    """
    edges = cv2.Canny(img, 50, 150, apertureSize=3)

    lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)
    if lines is None:
        lines = cv2.HoughLines(edges, 1, np.pi / 180, 100)

    rho_horizontal = []
    rho_vertical = []
    for row in lines:
        rho, theta = row[0]
        if math.fabs(theta - DEGREE_HORIZONTAL) < EPS:
            rho_horizontal.append(rho)
        elif math.fabs(theta - DEGREE_VERTICAL) < EPS:
            rho_vertical.append(rho)

    rho_horizontal = get_unique_lines(rho_horizontal)
    rho_vertical = get_unique_lines(rho_vertical)

    return rho_horizontal, rho_vertical
