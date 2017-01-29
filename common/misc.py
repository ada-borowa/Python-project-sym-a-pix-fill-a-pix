"""Miscellaneous common functions."""
import numpy as np

__author__ = 'Adriana Borowa'
__email__ = 'ada.borowa@gmail.com'


def get_unique(a):
    """Returns unique items in nparray
    :param a:  array
    :return: unique elements of array
    """
    if len(a) > 0:
        a = np.array(a)
        b = np.ascontiguousarray(a).view(np.dtype((np.void, a.dtype.itemsize * a.shape[1])))
        _, idx = np.unique(b, return_index=True)
        return a[idx]
    else:
        return np.array([])