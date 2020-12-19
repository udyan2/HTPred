import HTPredBenchCreator
import os
import time

cell_dir = 'C:/Users/anirb/Downloads/dsci__1/cell/'
input_file = 'C:/Users/anirb/Downloads/dsci__1/aes_part.txt'

r = HTPredBenchCreator.Creator(input_file, cell_dir)
print(r.convert())

# z = os.listdir(input_file)
# a = 0
#
# currentmillis = int(time.time()*1000)
# for t in z:
#     r = HTPredBenchCreator.Creator(input_file+t,cell_dir)
#     r.convert()
#     a += 1
#
# currentmillis = int(time.time()*1000) - currentmillis
#
# print('Compiled',a,'cells in',currentmillis,'millis')
