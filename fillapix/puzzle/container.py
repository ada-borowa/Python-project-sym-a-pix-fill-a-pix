#!/usr/bin/env python3
""" Container for puzzle.
"""

import cv2
import numpy as np
import pickle

from classifiers import classifier

__author__ = 'Adriana Borowa'
__email__ = 'ada.borowa@gmail.com'


class Container:
    """Stores puzzle data."""
    def __init__(self, size, from_file=True):
        """Initialization of container.
           Size: width and height of puzzle
        """
        self.size = size
        self.puzzle = np.zeros((size[0], size[1]))
        if from_file:
            self.classifier = pickle.load(classifier.get('digit'))

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

    def get_board(self):
        """
        Getter for puzzle board
        :return: puzzle board
        """
        return self.puzzle

    def generate_random(self):
        """
        Generates random fill-a-pix puzzle.
        :return: solution of generated puzzle
        """
        self.puzzle += 100
        solution = np.zeros(self.size)
        for i, row in enumerate(self.puzzle):
            for j, el in enumerate(row):
                if np.random.random() < 0.5:
                    curr = len([[a, b] for a in range(max(0, i - 1), min(i + 2, self.size[0]))
                               for b in range(max(0, j - 1), min(j + 2, self.size[1]))
                               if solution[a, b] == 1])

                    small = [[a, b] for a in range(max(0, i - 1), min(i + 2, self.size[0]))
                             for b in range(max(0, j - 1), min(j + 2, self.size[1]))
                             if solution[a, b] == 0]
                    if curr < len(small):
                        el = np.random.randint(curr, len(small) + 1)
                        self.puzzle[i, j] = el
                        while curr < el:
                            for (x, y) in small:
                                if solution[x, y] == 0:
                                    if np.random.random() < 0.9:
                                        solution[x, y] = 1
                                        curr += 1
                                        if el == curr:
                                            break
                        for (x, y) in small:
                            if solution[x, y] == 0:
                                solution[x, y] = -1

        solution[solution == -1] = 0
        return solution

