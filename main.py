import HTPredBenchCreator

cell_dir = 'C:/Users/anirb/Downloads/dsci__1/cell/'
input_file = 'C:/Users/anirb/Downloads/dsci__1/aes_part.txt'

t = HTPredBenchCreator.Creator(input_file,cell_dir)
print(t.convert())