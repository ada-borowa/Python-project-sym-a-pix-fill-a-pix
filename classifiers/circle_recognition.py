#!/usr/bin/env python3
""" Classifier builder.
    Gets images from folders with names corresponding to category (100 is empty square).
    Images are not included in this repository.
    Uses SVM.
"""

import glob
import os
import pickle

import cv2
import numpy as np
from sklearn.svm import SVC

__author__ = 'Adriana Borowa'
__email__ = 'ada.borowa@gmail.com'

if __name__ == '__main__':
    # directory containing training data
    data_dir = '../../classes/'

    dirs = ['horiz', 'sq', 'vert', 'x']
    dirs_label = ['_empty', '_circle']
    labels = [0, 1]

    for d in dirs:
        images = []
        labels = []
        empty_size = len([name for name in os.listdir(data_dir + d + dirs_label[0])])
        circle_size = len([name for name in os.listdir(data_dir + d + dirs_label[1])])
        sample = np.random.choice(int(empty_size), int(2 * empty_size))
        for l, dl in enumerate(dirs_label):
            for i, y in enumerate(sorted(glob.glob(data_dir + d + dl + '/*'))):
                if l == 1 or l == 0 and i in sample:
                    img = cv2.imread(y, cv2.IMREAD_GRAYSCALE)
                    img = cv2.resize(img, (20, 20))
                    images.append(img)
                    labels.append(l)
        images = np.array(images).reshape((len(labels), -1))
        labels = np.array(labels)
        classifier = SVC(gamma=0.00001)
        classifier.fit(images, labels)
        pickle.dump(classifier, open(d + 'clf.p', 'wb'), protocol=2)
