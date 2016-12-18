from symapix.imageops.reader import SymAPixReader

img_dir = '../../sym-a-pix_images/'
reader = SymAPixReader(img_dir + 'image1.jpg')
new_puzzle = reader.create_puzzle()
new_puzzle.print_puzzle()
