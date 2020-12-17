import HTPredBenchCreator

cell_dir = 'C:/Users/anirb/Downloads/dsci__1/cell/'
input_file = 'C:/Users/anirb/Downloads/dsci__1/'

t = HTPredBenchCreator.Creator(input_file,cell_dir,'s27')
print(t.convert())