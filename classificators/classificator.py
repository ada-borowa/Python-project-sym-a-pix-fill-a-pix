#!/usr/bin/env python3
""" Manages classificator files.
"""

__author__ = 'Adriana Borowa'
__email__ = 'ada.borowa@gmail.com'


def get(classificator):
    """"""
    if classificator == 'digit':
        return open('classificators/digit_clf.p', 'rb')
    elif classificator == 'horizontal':
        return open('classificators/horizclf.p', 'rb')
    elif classificator == 'vertical':
        return open('classificators/vertclf.p', 'rb')
    elif classificator == 'square':
        return open('classificators/sqclf.p', 'rb')
    elif classificator == 'x':
        return open('classificators/xclf.p', 'rb')
    else:
        print('No such classificator: {}'.format(classificator))
