#!/usr/bin/env python3
""" Manages classifier files.
"""

__author__ = 'Adriana Borowa'
__email__ = 'ada.borowa@gmail.com'


def get(classifier):
    """
    Gives SVM classifier file, depending on name.
    :param classifier: name of classifier: [digit, horizontal, vertical, square, x]
    :return: classifier file
    """
    if classifier == 'digit':
        return open('classifiers/digit_clf.p', 'rb')
    elif classifier == 'horizontal':
        return open('classifiers/horizclf.p', 'rb')
    elif classifier == 'vertical':
        return open('classifiers/vertclf.p', 'rb')
    elif classifier == 'square':
        return open('classifiers/sqclf.p', 'rb')
    elif classifier == 'x':
        return open('classifiers/xclf.p', 'rb')
    else:
        print('No such classifier: {}'.format(classifier))


if __name__ == '__main__':
    print('Use get(classifier) function.')
