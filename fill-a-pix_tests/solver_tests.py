import unittest

from fillapix.solver.solver import FillAPixSolver
import numpy as np


class TestSolverSizeOfHood(unittest.TestCase):
    """Tests for size_of_hood function."""

    def setUp(self):
        self.solver = FillAPixSolver(None)

    def test_corner(self):
        """Tests for corner, all corner have neighbourhoods of size 4"""
        self.assertEqual(self.solver.size_of_hood(0, 0), 4)
        self.assertEqual(self.solver.size_of_hood(0, 9), 4)
        self.assertEqual(self.solver.size_of_hood(9, 0), 4)
        self.assertEqual(self.solver.size_of_hood(9, 9), 4)

    def test_border(self):
        """Tests for borders, all borders have neighbourhoods of size 6"""
        self.assertEqual(self.solver.size_of_hood(0, 5), 6)
        self.assertEqual(self.solver.size_of_hood(9, 5), 6)
        self.assertEqual(self.solver.size_of_hood(5, 0), 6)
        self.assertEqual(self.solver.size_of_hood(5, 9), 6)

    def test_inside(self):
        """Tests for other points, all other points have neighbourhoods of size 9"""
        self.assertEqual(self.solver.size_of_hood(2, 3), 9)
        self.assertEqual(self.solver.size_of_hood(4, 3), 9)
        self.assertEqual(self.solver.size_of_hood(8, 2), 9)
        self.assertEqual(self.solver.size_of_hood(5, 5), 9)


class Test2ClueLogic(unittest.TestCase):
    def setUp(self):
        self.solver = FillAPixSolver(None)

    def test_not_filled(self):
        """Test for finding 2 clue logic, without additional filled fields in solution"""
        examples = []
        answers = []
        examples.append(np.array([[100, 100, 100, 100],
                                  [100, 4, 7, 100],
                                  [100, 100, 100, 100]]))
        answers.append(' . - - *\n . - - *\n . - - *\n')
        examples.append(np.array([[100, 100, 100],
                                  [100, 8, 100],
                                  [100, 5, 100],
                                  [100, 100, 100]]))
        answers.append(' * * *\n - - -\n - - -\n . . .\n')
        examples.append(np.array([[100, 2, 4, 100],
                                  [100, 100, 100, 100]]))
        answers.append(' . - - *\n . - - *\n')
        examples.append(np.array([[100, 100, 100, 100],
                                  [100, 3, 100, 100],
                                  [100, 100, 8, 100],
                                  [100, 100, 100, 100]]))
        answers.append(' . . . -\n . - - *\n . - - *\n - * * *\n')
        examples.append(np.array([[100, 100, 100, 100, 100],
                                  [100, 1, 100, 7, 100],
                                  [100, 100, 100, 100, 100]]))
        answers.append(' . . - * *\n . . - * *\n . . - * *\n')
        examples.append(np.array([[100, 100, 100, 100, 100],
                                  [100, 1, 100, 100, 100],
                                  [100, 100, 100, 8, 100],
                                  [100, 100, 100, 100, 100]]))
        answers.append(' . . . - -\n . . - * *\n . . - * *\n - - * * *\n')

        for e, a in zip(examples, answers):
            self.solver.set_puzzle(e)
            for i in range(e.shape[0]):
                for j in range(e.shape[1]):
                    self.solver.find_2_clue_logic(i, j)
            self.assertEqual(self.solver.print_solution(), a)

    def test_some_filled(self):
        examples = []
        answers = []
        solutions = []
        examples.append(np.array([[100, 2, 1, 100],
                                  [100, 100, 100, 100]]))
        solutions.append(np.array([[-1, 0, 0, 0],
                                   [0, 0, 0, 0]]))
        answers.append(' . - - .\n * - - .\n')

        examples.append(np.array([[100, 2, 1, 100],
                                  [100, 100, 100, 100]]))
        solutions.append(np.array([[-1, 0, 0, 0],
                                   [0, 0, -1, -1]]))
        answers.append(' . - - .\n * - . .\n')

        examples.append(np.array([[100, 100, 100, 100],
                                  [100, 2, 4, 100],
                                  [100, 100, 100, 100]]))
        solutions.append(np.array([[0, 0, 0, -1],
                                   [0, 0, 0, 0],
                                   [0, 0, 0, 0]]))
        answers.append(' . - - .\n . - - *\n . - - *\n')

        examples.append(np.array([[100, 100, 100, 100],
                                  [100, 2, 4, 100],
                                  [100, 100, 100, 100]]))
        solutions.append(np.array([[0, 0, 0, 0],
                                   [0, 0, 0, 0],
                                   [1, 0, 0, 0]]))
        answers.append(' . - - *\n . - - *\n * - - *\n')

        examples.append(np.array([[100, 5, 100, 100],
                                  [100, 100, 3, 100],
                                  [100, 100, 100, 100]]))
        solutions.append(np.array([[0, 0, 0, 0],
                                   [0, 0, 0, 0],
                                   [0, 0, 0, 0]]))
        answers.append(' * - - .\n * - - .\n - . . .\n')

        examples.append(np.array([[100, 100, 100, 100, 100],
                                  [100, 2, 100, 7, 100],
                                  [100, 100, 100, 100, 100]]))
        solutions.append(np.array([[0, 0, 0, 0, -1],
                                   [0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0]]))
        answers.append(' . . - * .\n . . - * *\n . . - * *\n')

        examples.append(np.array([[100, 100, 100, 100, 100],
                                  [100, 1, 100, 100, 100],
                                  [100, 100, 100, 7, 100],
                                  [100, 100, 100, 100, 100]]))
        solutions.append(np.array([[0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, -1],
                                   [0, 0, 0, 0, 0]]))
        answers.append(' . . . - -\n . . - * *\n . . - * .\n - - * * *\n')

        for e, a, s in zip(examples, answers, solutions):
            self.solver.set_puzzle(e)
            self.solver.solution = s
            for i in range(e.shape[0]):
                for j in range(e.shape[1]):
                    self.solver.find_2_clue_logic(i, j)
            self.assertEqual(self.solver.print_solution(), a)

    def test_special_case_corner(self):
        example = np.array([[2, 2, 100, 100, 100, 2, 2],
                            [2, 100, 100, 100, 100, 100, 2],
                            [100, 100, 100, 100, 100, 100, 100],
                            [100, 100, 100, 100, 100, 100, 100],
                            [2, 100, 100, 100, 100, 100, 2],
                            [2, 2, 100, 100, 100, 2, 2]])
        answer = ' - - . - . - -\n - - . - . - -\n . . - - - . .\n . . - - - . .\n - - . - . - -\n - - . - . - -\n'
        self.solver.set_puzzle(example)
        for i in range(example.shape[0]):
            for j in range(example.shape[1]):
                self.solver.special_case(i, j)
        self.assertEqual(self.solver.print_solution(), answer)

    def test_special_case_border(self):
        example = np.array([[100, 100, 3, 100, 100],
                            [100, 100, 3, 100, 100],
                            [100, 100, 100, 100, 100],
                            [3, 3, 100, 100, 100],
                            [100, 100, 100, 100, 100],
                            [100, 100, 100, 3, 3],
                            [100, 100, 100, 100, 100],
                            [100, 100, 100, 100, 100],
                            [100, 100, 3, 100, 100],
                            [100, 100, 3, 100, 100]])
        answer = ' - - - - -\n - - - - -\n - . . . -\n - - . - -\n - - . - -\n - - . - -\n - - . - -\n - . . . -\n' \
                 + ' - - - - -\n - - - - -\n'
        self.solver.set_puzzle(example)
        for i in range(example.shape[0]):
            for j in range(example.shape[1]):
                self.solver.special_case(i, j)
        self.assertEqual(self.solver.print_solution(), answer)


class Test3ClueLogic(unittest.TestCase):
    def setUp(self):
        self.solver = FillAPixSolver(None)

    def test_checking_neighbours(self):
        """Test for checking if point has 2 neighbours."""
        example = np.array([[100, 2, 3, 100, 100],
                            [2, 100, 3, 100, 100],
                            [100, 4, 5, 6, 100]])
        self.solver.set_puzzle(example)
        answers = [True, False, True, True, False, True, False, False, False, False, True, False, False, True, False]
        a = 0
        for i in range(example.shape[0]):
            for j in range(example.shape[1]):
                self.assertEqual(self.solver.get_neighbours(i, j)[0], answers[a])
                a += 1

    def test_3_clue_logic(self):
        example = np.array([[100, 100, 100, 100, 100],
                            [1, 100, 100, 100, 100],
                            [100, 100, 100, 100, 100],
                            [100, 2, 100, 100, 100],
                            [100, 100, 100, 1, 100]])
        solution = np.array([[-1, -1, 0, 0, 0],
                             [-1, -1, 0 ,0 ,0],
                             [0, 0, 0, 0, 0],
                             [0, 0, 0, -1, -1],
                             [0, 0, 0, -1, -1]])
        answer = ' . . - - -\n . . - - -\n - - . - -\n . . - . .\n . . - . .\n'
        self.solver.set_puzzle(example)
        self.solver.solution = solution
        for i in range(example.shape[0]):
            for j in range(example.shape[1]):
                self.solver.find_3_clue_logic(i, j)
        self.assertEqual(self.solver.print_solution(), answer)

        example = np.array([[100, 100, 100, 100, 100],
                            [2, 100, 100, 100, 100],
                            [100, 100, 100, 100, 100],
                            [100, 2, 100, 100, 100],
                            [100, 100, 100, 1, 100]])
        solution = np.array([[1, -1, 0, 0, 0],
                             [-1, -1, 0 ,0 ,0],
                             [0, 0, 0, 0, 0],
                             [0, 0, 0, -1, -1],
                             [0, 0, 0, -1, -1]])
        answer = ' * . - - -\n . . - - -\n - - . - -\n . . - . .\n . . - . .\n'
        self.solver.set_puzzle(example)
        self.solver.solution = solution
        for i in range(example.shape[0]):
            for j in range(example.shape[1]):
                self.solver.find_3_clue_logic(i, j)
        self.assertEqual(self.solver.print_solution(), answer)

    def test_ASA(self):
        example = np.array([[100, 100, 100, 100, 100, 100],
                           [100, 4, 6, 100, 2, 100],
                           [100, 100, 100, 100, 100, 100]])
        answer = ' . - - - . .\n . - - - . .\n . - - - . .\n'
        self.solver.set_puzzle(example)
        for i in range(example.shape[0]):
            for j in range(example.shape[1]):
                self.solver.find_ASA(i, j)
        self.assertEqual(self.solver.print_solution(), answer)

if __name__ == '__main__':
    SUITE1 = unittest.TestLoader().loadTestsFromTestCase(TestSolverSizeOfHood)
    print(unittest.TextTestRunner(verbosity=3).run(SUITE1))
