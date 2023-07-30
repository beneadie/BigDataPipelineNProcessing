import sys

import string

import os

def rem_punc(arr):
     rempunc = str.maketrans('', '', string.punctuation)
     for i in range(0, len(arr)):
          arr[i] = arr[i].translate(rempunc)
     return arr


for root, dir, files in os.walk(sys.argv[1]): # chat gpt
     for file in files:
          with open(os.path.join(root, file), 'r') as text_1:
               for line in text_1:
                    line = line.strip()
                    words = line.split()
                    words = rem_punc(words)
                    for i in range(1, len(words)):
                         pair = (words[i-1], words[i])
                         print(f"{pair}\t{1}")
