#!/usr/bin/env python3
""" Main window of Sym-a-pix and Fill-a-pix solver/generator program.
"""

from PyQt4 import QtGui

__author__ = 'Adriana Borowa'
__email__ = 'ada.borowa@gmail.com'


class GenerateFillDialog(QtGui.QMainWindow):
    """Dialog window where user can set size of new puzzle"""
    def __init__(self, parent):
        """Initialization of class."""
        super(GenerateFillDialog, self).__init__()
        self.ok_btn = QtGui.QPushButton('OK')
        self.width_value = QtGui.QSpinBox()
        self.height_value = QtGui.QSpinBox()
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        """Dialog window"""
        self.setWindowTitle('Fill-a-pix: generate game')
        self.resize(200, 120)
        cw = QtGui.QWidget()
        self.setCentralWidget(cw)
        l = QtGui.QGridLayout()
        height_label = QtGui.QLabel('Height: ')
        width_label = QtGui.QLabel('Width: ')

        self.height_value.setMinimum(5)
        self.height_value.setMaximum(20)
        self.height_value.setValue(10)
        self.width_value.setMinimum(5)
        self.width_value.setMaximum(20)
        self.width_value.setValue(10)
        l.addWidget(height_label, *(0, 0))
        l.addWidget(self.height_value, *(0, 1))
        l.addWidget(width_label, *(1, 0))
        l.addWidget(self.width_value, *(1, 1))

        self.ok_btn.clicked.connect(self.send_values)
        l.addWidget(self.ok_btn, *(2, 1))
        cw.setLayout(l)

    def send_values(self):
        """Function to send user's values to generating function."""
        height = self.height_value.value()
        width = self.width_value.value()
        self.parent.generate_new_fill(width, height)
        self.height_value.setValue(10)
        self.width_value.setValue(10)
        self.close()
