from fillapix.imageops.reader import FillAPixReader
from fillapix.solver.solver import FillAPixSolver

img_dir = '../../fill-a-pix_images/'
reader = FillAPixReader(img_dir + 'image5.jpg')
new_puzzle = reader.create_puzzle()
new_puzzle.print_puzzle()
solver = FillAPixSolver(new_puzzle)
solver.solve()
solver.print_solution()
print(solver.correct_fill(), solver.is_solved())