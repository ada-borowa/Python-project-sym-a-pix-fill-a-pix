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
        self.puzzle = np.zeros((size, size))
        clf_file = '../../classificators/digit_clf.p'
        self.classifier = pickle.load(open(clf_file, 'rb'))

    def insert(self, image, x, y):
        """
        Inserts data into puzzle.
        :param image: fragment of full image to be processed
        :param x: position
        :param y: position
        :return: None
        """
        image = image[:-2, :]
        image = cv2.resize(image, (15, 15))
        number = self.classifier.predict(image.reshape(1, -1))
        self.puzzle[x, y] = int(number)

    def print_puzzle(self):
        """
        Prints current puzzle.
        :return: None
        """
        for row in self.puzzle:
            txt = ''
            for el in row:
                if el == 100:
                    txt += '_ '
                else:
                    txt += str(int(el)) + ' '
            print(txt)
