import HTPredBenchCreator
import os
import time

cell_dir = 'C:/Users/anirb/Downloads/dsci__1/aes_cells_included/'
input_file = 'C:/Users/anirb/Downloads/dsci__1/S_396.txt'

currentmillis = int(time.time()*1000)
r = HTPredBenchCreator.Creator(input_file, cell_dir)
print(r.convert())
currentmillis = int(time.time()*1000) - currentmillis
print('Converted in',currentmillis,'millis')


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
