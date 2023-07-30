import sys
from operator import itemgetter

cur_pair= None
cur_count = 0

for line in sys.stdin:
     line = line.strip()
     pair, count = line.split('\t', 1) # not sure this should be a 1

     try:
          count = int(count)  # if string makes int
     except ValueError:
          continue

     if pair != cur_pair:
          print(f'{cur_pair}\t{cur_count}')
          cur_pair = pair
          cur_count = count
     else:
          cur_count+=count

# final pair
if cur_pair is not None:
     print(f'{cur_pair}\t{cur_count}')




