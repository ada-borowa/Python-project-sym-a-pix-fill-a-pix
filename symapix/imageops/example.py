from symapix.imageops.reader import SymAPixReader
from symapix.solver.solver import SymAPixSolver

img_dir = '../../sym-a-pix_images/'
reader = SymAPixReader(img_dir + 'image1.jpg')
new_puzzle = reader.create_puzzle()
# new_puzzle.print_puzzle()
solver = SymAPixSolver(new_puzzle)
print()
# solver.print_solution()
solver.solve()
solver.print_solution()