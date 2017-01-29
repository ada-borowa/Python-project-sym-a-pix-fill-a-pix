#!/usr/bin/env python3
""" Main window of Sym-a-pix and Fill-a-pix solver/generator program.
"""

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt
import sys

from fillapix.puzzle import container as fc
from symapix.puzzle import container as sc
from symapix.imageops.reader import SymAPixReader
from symapix.solver.solver import SymAPixSolver
from symapix.puzzle.generator import Generator
from fillapix.imageops.reader import FillAPixReader
from fillapix.solver.solver import FillAPixSolver
from gui.generate_fill_dialog import GenerateFillDialog
from gui.generate_sym_dialog import GenerateSymDialog

__author__ = 'Adriana Borowa'
__email__ = 'ada.borowa@gmail.com'

SIZE = 800
SQUARE = 30
EPS = 5


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        """Initialization of class."""
        super(MainWindow, self).__init__()
        self.gfd = GenerateFillDialog(self)
        self.gsd = GenerateSymDialog(self)
        self.status_bar = self.statusBar()
        self.l = QtGui.QVBoxLayout()
        self.content = QtGui.QVBoxLayout()

        self.button_part = QtGui.QHBoxLayout()
        self.curr_game_label = QtGui.QLabel('Currently playing: no game')
        self.curr_game = 0
        self.solve_btn = QtGui.QPushButton('Solve')
        self.clear_btn = QtGui.QPushButton('Clear')
        self.check_btn = QtGui.QPushButton('Check')

        self.puzzle_part = QtGui.QVBoxLayout()
        self.painter = QtGui.QPainter()
        self.board = QtGui.QLabel()
        self.pix_map = QtGui.QPixmap(SIZE, SIZE)

        self.puzzle = None
        self.solver = None
        self.vertical_lines = 0
        self.horizontal_lines = 0
        self.game_size = []

        self.init_gui()

    def init_gui(self):
        """Initialization of UI."""
        # Window setup
        self.setWindowTitle('Puzzles')
        self.resize(SIZE, SIZE + 100)
        cw = QtGui.QWidget()
        self.setCentralWidget(cw)
        cw.setLayout(self.l)

        # Menu setup
        # Sym-a-pix actions
        load_sym = QtGui.QAction('Load puzzle', self)
        load_sym.setStatusTip('Sym-a-pix: Load puzzle from file.')
        load_sym.triggered.connect(self.load_sym_from_file)

        gen_sym = QtGui.QAction('Generate puzzle', self)
        gen_sym.setStatusTip('Sym-a-pix: Generate random puzzle.')
        gen_sym.triggered.connect(self.generate_sym)

        # Fill-a-pix actions
        load_fill = QtGui.QAction('Load puzzle', self)
        load_fill.setStatusTip('Fill-a-pix: Load puzzle from file.')
        load_fill.triggered.connect(self.load_fill_from_file)

        gen_fill = QtGui.QAction('Generate puzzle', self)
        gen_fill.setStatusTip('Fill-a-pix: Generate random puzzle.')
        gen_fill.triggered.connect(self.generate_fill)

        menu_bar = self.menuBar()
        sym_menu = menu_bar.addMenu('&Sym-a-pix')
        sym_menu.addAction(load_sym)
        sym_menu.addAction(gen_sym)

        fill_menu = menu_bar.addMenu('&Fill-a-pix')
        fill_menu.addAction(load_fill)
        fill_menu.addAction(gen_fill)

        # Window's content setup
        self.content.addWidget(self.curr_game_label)
        # Canvas
        self.pix_map.fill(Qt.white)

        self.board.setPixmap(self.pix_map)
        self.board.setMouseTracking(True)
        self.puzzle_part.addWidget(self.board)
        self.content.addLayout(self.puzzle_part)
        # Buttons
        self.solve_btn.clicked.connect(self.solve_game)
        self.clear_btn.clicked.connect(self.clear_game)
        self.check_btn.clicked.connect(self.check_game)
        self.button_part.addWidget(self.solve_btn)
        self.button_part.addWidget(self.clear_btn)
        self.button_part.addWidget(self.check_btn)
        self.button_part.setAlignment(Qt.AlignTop)
        self.content.addLayout(self.button_part)

        self.l.addLayout(self.content)
        self.show()

    def load_sym_from_file(self):
        """Loads sym-a-pix puzzle from file."""
        self.status_bar.showMessage('Solving...')
        file_name = QtGui.QFileDialog.getOpenFileName(self, 'Zapisz plik', '.')
        try:
            self.change_curr_game(1)
            reader = SymAPixReader(file_name)
            self.puzzle = reader.create_puzzle()
            self.horizontal_lines, self.vertical_lines = reader.get_lines()
            self.solver = SymAPixSolver(self.puzzle)
            self.game_size = self.solver.size
            self.solver.solve()
            self.draw_game()
            self.status_bar.showMessage('Loaded puzzle from file: {}'.format(file_name.split('/')[-1]))
        except IOError:
            self.status_bar.showMessage('Cannot read file: {}'.format(file_name.split('/')[-1]))

    def generate_sym(self):
        """Opens dialog where user can set size of puzzle to be generated."""
        self.gsd.show()

    def generate_new_sym(self, width, height, color):
        """
        Generates new puzzle, puzzle is then showed to user.
        :param width: width of puzzle
        :param height: height of puzzle
        :param color: number of colors used
        :return:
        """
        self.change_curr_game(1)
        self.puzzle = sc.Container((height, width))
        self.puzzle.set_colors(color)
        self.horizontal_lines, self.vertical_lines = width + 1, height + 1
        self.solver = SymAPixSolver(self.puzzle)
        self.game_size = self.solver.size
        generator = Generator(self.solver, self.puzzle)
        generator.generate_random()
        self.solver.solve()
        generator.fill_dots()
        self.draw_game()

    def load_fill_from_file(self):
        """Loads fill-a-pix puzzle from file."""
        self.status_bar.showMessage('Solving...')
        file_name = QtGui.QFileDialog.getOpenFileName(self, 'Zapisz plik', '.')
        try:
            self.change_curr_game(2)
            reader = FillAPixReader(file_name)
            self.puzzle = reader.create_puzzle()
            self.horizontal_lines, self.vertical_lines = reader.get_lines()
            self.solver = FillAPixSolver(self.puzzle)
            self.game_size = self.solver.size
            self.solver.solve()
            self.draw_game()
            self.status_bar.showMessage('Loaded puzzle from file: {}'.format(file_name.split('/')[-1]))
        except IOError:
            self.status_bar.showMessage('Cannot read file: {}'.format(file_name.split('/')[-1]))

    def generate_fill(self):
        """Opens dialog where user can set size of puzzle to be generated."""
        self.gfd.show()

    def generate_new_fill(self, width, height):
        """
        Generates new puzzle, puzzle is then showed to user.
        :param width: width of puzzle
        :param height: height of puzzle
        :return:
        """
        self.change_curr_game(2)
        self.puzzle = fc.Container((height, width))
        solution = self.puzzle.generate_random()
        self.horizontal_lines, self.vertical_lines = width + 1, height + 1
        self.solver = FillAPixSolver(self.puzzle)
        self.game_size = self.solver.size
        self.solver.set_solution(solution)
        self.draw_game()

    def change_curr_game(self, game):
        """Sets value of label with current game."""
        self.curr_game = game
        if self.curr_game == 0:
            self.curr_game_label.setText('Currently playing: no game')
        elif self.curr_game == 1:
            self.curr_game_label.setText('Currently playing: Sym-a-pix')
        elif self.curr_game == 2:
            self.curr_game_label.setText('Currently playing: Fill-a-pix')

    def mousePressEvent(self, event):
        """Overwrites QWidget function: catches mouse press events.
        Depending on type of game performs action.
        After that checks if game is solved."""
        if self.curr_game == 1:
            x, y = self.get_painter_pos(event.x(), event.y())
            if x % SQUARE < EPS:
                self.change_line(int((x - x % SQUARE) / SQUARE * 2 - 1), int((y - y % SQUARE) / SQUARE * 2))
            elif SQUARE - EPS < x % SQUARE:
                self.change_line(int((x - x % SQUARE + SQUARE) / SQUARE * 2 - 1), int((y - y % SQUARE) / SQUARE * 2))
            elif y % SQUARE < EPS:
                self.change_line(int((x - x % SQUARE) / SQUARE * 2), int((y - y % SQUARE) / SQUARE * 2 - 1))
            elif SQUARE - EPS < y % SQUARE:
                self.change_line(int((x - x % SQUARE) / SQUARE * 2), int((y - y % SQUARE + SQUARE) / SQUARE * 2 - 1))
            self.draw_game()

        elif self.curr_game == 2:
            x, y = self.get_painter_pos(event.x(), event.y())
            if 0 <= x < self.vertical_lines - 1 and 0 <= y < self.horizontal_lines - 1:
                self.change_square(x, y)
                self.draw_game()

        self.check_solved()

    def get_painter_pos(self, i, j):
        """Given position of mouse click and type of game, returns clicked line or  square position."""
        i = (i - 5) * ((self.vertical_lines + 1) * SQUARE) / 800
        j = (j - 55) * ((self.horizontal_lines + 1) * SQUARE) / 800
        if self.curr_game == 1:
            if i > SQUARE and j > SQUARE:
                return i - SQUARE, j - SQUARE
            else:
                return -1, -1

        elif self.curr_game == 2:
            if i > SQUARE and j > SQUARE:
                return int((i - SQUARE) / SQUARE), int((j - SQUARE) / SQUARE)
            else:
                return -1, -1

    def draw_game(self):
        """Chooses what game to draw."""
        self.draw_lines()
        if self.curr_game == 1:
            self.draw_sym()
            self.draw_border()
        elif self.curr_game == 2:
            self.draw_fill()

    def draw_sym(self):
        """Draws sym-a-pix game."""
        self.draw_squares_sym()
        self.draw_solution_lines()
        self.draw_circles()

    def draw_fill(self):
        """Draws fill-a-pix game."""
        self.draw_squares_fill()
        self.draw_numbers()

    def draw_lines(self):
        """Draws lines of game."""
        self.pix_map.fill(Qt.white)
        self.painter.begin(self.pix_map)
        self.painter.setWindow(0, 0, (self.vertical_lines + 1) * SQUARE, (self.horizontal_lines + 1) * SQUARE)
        for line in range(1, self.horizontal_lines + 1):
            if self.curr_game == 2:
                self.painter.setPen(Qt.black)
            else:
                self.painter.setPen(Qt.lightGray)
            self.painter.drawLine(SQUARE, line * SQUARE, self.vertical_lines * SQUARE, line * SQUARE)
        for line in range(1, self.vertical_lines + 1):
            if self.curr_game == 2:
                self.painter.setPen(Qt.black)
            else:
                self.painter.setPen(Qt.lightGray)
            self.painter.drawLine(line * SQUARE, SQUARE, line * SQUARE, self.horizontal_lines * SQUARE)
        self.painter.end()
        self.board.setPixmap(self.pix_map)

    def draw_border(self):
        """Draws border of the sym-a-pix game."""
        self.painter.begin(self.pix_map)
        self.painter.setWindow(0, 0, (self.vertical_lines + 1) * SQUARE, (self.horizontal_lines + 1) * SQUARE)
        for line in range(1, self.horizontal_lines + 1):
            if line in [1, self.horizontal_lines]:
                pen = QtGui.QPen()
                pen.setColor(Qt.black)
                pen.setWidth(3)
                self.painter.setPen(pen)
                self.painter.drawLine(SQUARE, line * SQUARE, self.vertical_lines * SQUARE, line * SQUARE)
        for line in range(1, self.vertical_lines + 1):
            if line in [1, self.vertical_lines]:
                pen = QtGui.QPen()
                pen.setColor(Qt.black)
                pen.setWidth(3)
                self.painter.setPen(pen)
                self.painter.drawLine(line * SQUARE, SQUARE, line * SQUARE, self.horizontal_lines * SQUARE)
        self.painter.end()
        self.board.setPixmap(self.pix_map)

    def draw_solution_lines(self):
        """Draws user selected lines in sym-a-pix game."""
        curr_user_solution = self.solver.get_user_solution()
        self.painter.begin(self.pix_map)
        self.painter.setWindow(0, 0, (self.vertical_lines + 1) * SQUARE, (self.horizontal_lines + 1) * SQUARE)
        pen = QtGui.QPen()
        pen.setColor(Qt.darkGray)
        pen.setWidth(3)
        self.painter.setPen(pen)
        for i, row in enumerate(curr_user_solution):
            for j, el in enumerate(row):
                if not (i % 2 == 0 and j % 2 == 0) and not (i % 2 == 1 and j % 2 == 1):
                    try:
                        if curr_user_solution[j, i] == 1:
                            if i % 2 == 0:
                                self.painter.drawLine(SQUARE * (i/2 + 1), SQUARE * (j/2+1.5),
                                                      SQUARE * (i/2 + 2), SQUARE * (j/2+1.5))
                            elif j % 2 == 0:
                                self.painter.drawLine(SQUARE * (i/2+1.5), SQUARE * (j/2 + 1),
                                                      SQUARE * (i/2+1.5), SQUARE * (j/2 + 2))
                    except IndexError:
                        pass
        self.painter.end()
        self.board.setPixmap(self.pix_map)

    def draw_numbers(self):
        """Draws numbers in fill-a-pix game."""
        curr_user_solution = self.solver.get_user_solution()
        self.painter.begin(self.pix_map)
        self.painter.setWindow(0, 0, (self.vertical_lines + 1) * SQUARE, (self.horizontal_lines + 1) * SQUARE)
        font = QtGui.QFont('Arial')
        font.setPointSize(22)
        self.painter.setFont(font)
        for i, row in enumerate(self.solver.puzzle):
            for j, el in enumerate(row):
                if el < 100:
                    val = str(int(el))
                    if curr_user_solution[i, j] == 1:
                        self.painter.setPen(Qt.white)
                    else:
                        self.painter.setPen(Qt.black)
                    self.painter.drawText(1.25 * SQUARE + j * SQUARE, 1.85 * SQUARE + i * SQUARE, val)
        self.painter.end()
        self.board.setPixmap(self.pix_map)

    def draw_circles(self):
        """Draws circles in sym-a-pix."""
        colors = self.puzzle.get_colors()
        self.painter.begin(self.pix_map)
        self.painter.setWindow(0, 0, (self.vertical_lines + 1) * SQUARE, (self.horizontal_lines + 1) * SQUARE)
        for i, row in enumerate(self.solver.puzzle):
            for j, el in enumerate(row):
                if el > 0:
                    color = colors[int(el) - 1]
                    if color[0] == 0 and color[1] == 0 and color[2] == 0:
                        self.painter.setPen(Qt.lightGray)
                    else:
                        self.painter.setPen(Qt.black)
                    self.painter.setBrush(QtGui.QColor(color[2], color[1], color[0]))
                    self.painter.drawEllipse(QtCore.QPoint(SQUARE * 1.5 + SQUARE * j / 2.0,
                                                           SQUARE * 1.5 + SQUARE * i / 2.0), 5, 5)
        self.painter.end()
        self.board.setPixmap(self.pix_map)

    def change_square(self, i, j):
        """Changes color of square and value of user solution in solver."""
        i, j = j, i
        curr_val = self.solver.get_user_value(i, j)
        if curr_val == 1:
            self.solver.set_user_value(i, j, -1)
        else:
            self.solver.set_user_value(i, j, curr_val + 1)

    def change_line(self, i, j):
        """Changes line selected by user. Line unselected <-> line selected."""
        i, j = j, i
        val = self.solver.get_user_value(i, j)
        if val is not None:
            self.solver.set_user_value(i, j, (val + 1) % 2)

    def draw_squares_sym(self):
        """Fills squares in sym-a-pix game, if they are part of closed block."""
        self.painter.begin(self.pix_map)
        self.painter.setWindow(0, 0, (self.vertical_lines + 1) * SQUARE, (self.horizontal_lines + 1) * SQUARE)
        color_board = self.solver.get_color_board()
        colors = self.solver.get_colors()
        for i, row in enumerate(color_board):
            for j, el in enumerate(row):
                if i % 2 == 0 and j % 2 == 0 and el > 0:
                    c = colors[el - 1]
                    self.painter.setBrush(QtGui.QColor(c[2], c[1], c[0]))
                    self.painter.setPen(QtGui.QColor(c[2], c[1], c[0]))
                    self.painter.drawRect(SQUARE * (j/2 + 1), SQUARE * (i/2 + 1),
                                          SQUARE, SQUARE)
        self.painter.end()
        self.board.setPixmap(self.pix_map)

    def draw_squares_fill(self):
        """Draws squares in fill-a-pix game: filled, unfilled, unsure."""
        self.painter.begin(self.pix_map)
        self.painter.setWindow(0, 0, (self.vertical_lines + 1) * SQUARE, (self.horizontal_lines + 1) * SQUARE)
        curr_user_solution = self.solver.get_user_solution()
        for i, row in enumerate(curr_user_solution):
            for j, el in enumerate(row):
                if el == -1:
                    self.painter.setBrush(Qt.lightGray)
                elif el == 1:
                    self.painter.setBrush(Qt.black)
                if el != 0:
                    self.painter.drawRect(SQUARE * (j + 1), SQUARE * (i + 1),
                                          SQUARE, SQUARE)
        self.painter.end()
        self.board.setPixmap(self.pix_map)

    def solve_game(self):
        """Gives solution to user."""
        self.solver.set_solved()
        self.draw_game()

    def clear_game(self):
        """Clears game to initial state."""
        self.solver.clear_user_solution()
        self.draw_game()

    def check_game(self):
        """Let's user allow if there are any mistakes."""
        x, y = self.solver.check_user_solution()
        if x > -1 and y > -1:
            self.status_bar.showMessage('You have mistake in: ({}, {})'.format(y + 1, x + 1))
        else:
            self.status_bar.showMessage('Correct!')

    def check_solved(self):
        """Checks if user solved the game."""
        if self.solver is not None:
            if self.solver.is_solved_by_user():
                self.painter.begin(self.pix_map)
                self.painter.setWindow(0, 0, (self.vertical_lines + 1) * SQUARE, (self.horizontal_lines + 1) * SQUARE)
                font = QtGui.QFont('Arial')
                font.setPointSize(22)
                self.painter.setFont(font)
                self.painter.setPen(Qt.red)
                self.painter.drawText(SQUARE, SQUARE, 'SOLVED!')
                self.painter.end()
                self.board.setPixmap(self.pix_map)


def main_window():
    """Runs game's main window."""
    app = QtGui.QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
