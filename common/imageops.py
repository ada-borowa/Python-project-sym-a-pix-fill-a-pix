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
        if rhos[it + 1] - rhos[it] < 10:
            tmp.append(int((rhos[it] + rhos[it+1])/2.0))
            it += 1
        else:
            tmp.append(int(rhos[it]))
        it += 1
    if rhos[-1] - tmp[-1] > 10:
        tmp.append(int(rhos[-1]))
    return tmp


def get_line_positions(img):
    """
    Using Hough transformation detects lines on image
    :param img: Image
    :return: positions of horizontal and vertical lines
    """
    edges = cv2.Canny(img, 50, 150, apertureSize=3)
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

    # for rho in rho_horizontal:
    #     theta = DEGREE_HORIZONTAL
    #     a = np.cos(theta)
    #     b = np.sin(theta)
    #     x0 = a * rho
    #     y0 = b * rho
    #     x1 = int(x0 + 1000 * (-b))
    #     y1 = int(y0 + 1000 * (a))
    #     x2 = int(x0 - 1000 * (-b))
    #     y2 = int(y0 - 1000 * (a))
    #
    #     cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
    #
    # for rho in rho_vertical:
    #     theta = DEGREE_VERTICAL
    #     a = np.cos(theta)
    #     b = np.sin(theta)
    #     x0 = a * rho
    #     y0 = b * rho
    #     x1 = int(x0 + 1000 * (-b))
    #     y1 = int(y0 + 1000 * (a))
    #     x2 = int(x0 - 1000 * (-b))
    #     y2 = int(y0 - 1000 * (a))
    #
    #     cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
    #
    # cv2.imshow('houghlines3.jpg', img)

    return rho_horizontal, rho_vertical
