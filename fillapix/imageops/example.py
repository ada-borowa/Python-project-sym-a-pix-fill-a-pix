from fillapix.imageops.reader import FillAPixReader

img_dir = '../../fill-a-pix_images/'
reader = FillAPixReader(img_dir + 'image2.jpg')
new_puzzle = reader.create_puzzle()
new_puzzle.print_puzzle()
