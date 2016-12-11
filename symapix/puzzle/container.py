#!/usr/bin/env python3
""" Container for puzzle.
"""

import cv2
import numpy as np
import pickle

__author__ = 'Adriana Borowa'
__email__ = 'ada.borowa@gmail.com'


class Container:
    """Stores puzzle data."""
    def __init__(self, size):
        """Initailization of container.
           Size: width and height of puzzle
        """
        self.size = size
        # TODO: create empty array with position for squares and lines
        pass

    def insert(self, image, x, y):
        """
        Inserts data into puzzle.
        :param image: fragment of full image to be processed
        :param x: position
        :param y: position
        :return: None
        """
        # TODO: inserting into array: different for square and line (2 functions)
        pass

    def print_puzzle(self):
        """
        Prints current puzzle.
        :return: None
        """
        pass
