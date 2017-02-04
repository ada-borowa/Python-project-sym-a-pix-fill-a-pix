#!/usr/bin/env python3
""" Classifier builder.
    Gets images from folders with names corresponding to category (100 is empty square).
    Images are not included in this repository.
    Uses SVM.
"""

import glob
import pickle
import numpy as np

import cv2
from sklearn.svm import SVC

__author__ = 'Adriana Borowa'
__email__ = 'ada.borowa@gmail.com'


if __name__ == '__main__':
    # directory containing training data
    data_dir = '../../numbers/'

    dirs = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '100']

    images = []
    labels = []
    for d in dirs:
        for y in sorted(glob.glob(data_dir + d + '/*')):
            img = cv2.imread(y, cv2.IMREAD_GRAYSCALE)
            img = img[:-2, :]
            img = cv2.resize(img, (15, 15))
            images.append(img)
            labels.append(int(d))
    images = np.array(images).reshape((len(labels), -1))
    labels = np.array(labels)
    classifier = SVC(gamma=0.00001)
    classifier.fit(images, labels)
    pickle.dump(classifier, open('digit_clf.p', 'wb'), protocol=2)
