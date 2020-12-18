import HTPredBenchCreator
import os
import time

current_milli_time = lambda: int(round(time.time() * 1000))

cell_dir = 'C:/Users/anirb/Downloads/dsci__1/cell/'
input_file = 'C:/Users/anirb/Downloads/dsci__1/cell/'

t = os.listdir(input_file)
m = current_milli_time()

for i in range(1000):
    print(i)
    for s in t:
        r = HTPredBenchCreator.Creator(input_file+s,cell_dir)
        r.convert()

m = current_milli_time() - m
print('Reqd time : ',m)