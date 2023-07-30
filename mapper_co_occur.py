import sys

import string

import os

#binary search library
import bisect

# stopwords are taken from list in the in the ntk library, nltk.corpus.stopwords("english")
default_sw = ['a', 'about', 'above', 'after', 'again', 'against', 'ain', 'all', 'am', 'an', 'and', 'any', 'are', 'aren', "aren't", 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', 'can', 'couldn', "couldn't", 'd', 'did', 'didn', "didn't", 'do', 'does', 'doesn', "doesn't", 'doing', 'don', "don't", 'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', 'hadn', "hadn't", 'has', 'hasn', "hasn't", 'have', 'haven', "haven't", 'having', 'he', 'her', 'here', 'hers', 'herself', 'him', 'himself', 'his', 'how', 'i', 'if', 'in', 'into', 'is', 'isn', "isn't", 'it', "it's", 'its', 'itself', 'just', 'll', 'm', 'ma', 'me', 'mightn', "mightn't", 'more', 'most', 'mustn', "mustn't", 'my', 'myself', 'needn', "needn't", 'no', 'nor', 'not', 'now', 'o', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 're', 's', 'same', 'shan', "shan't", 'she', "she's", 'should', "should've", 'shouldn', "shouldn't", 'so', 'some', 'such', 't', 'than', 'that', "that'll", 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', 'these', 'they', 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 've', 'very', 'was', 'wasn', "wasn't", 'we', 'were', 'weren', "weren't", 'what', 'when', 'where', 'which', 'while', 'who', 'whom', 'why', 'will', 'with', 'won', "won't", 'wouldn', "wouldn't", 'y', 'you', "you'd", "you'll", "you're", "you've", 'your', 'yours', 'yourself', 'yourselves']

#function removes the
def rem_punc(arr):
     rempunc = str.maketrans('', '', string.punctuation)
     for i in range(0, len(arr)):
          arr[i] = arr[i].translate(rempunc)
     return arr

def rem_sw_binary(arr, stopwords=default_sw):
     new_arr=[]
     for i in arr:
          x = i.lower()
          index = bisect.bisect_left(stopwords, x) # to save time with sorted list
          if index < len(stopwords) and stopwords[index] == x:
               pass
          else:
               new_arr.append(i)
     return new_arr

def rem_sw(arr, stopwords):
     new_arr=[]
     for i in arr:
          lc = i.lower()
          if lc in stopwords:
               pass
          else:
               new_arr.append(i)
     return new_arr

def get_pairs(arr):
     ret_tupes = []
     for i in range(0, len(arr)):
          # assumes that the function wants to include words even if used twice
          for j in range(i+1, len(arr)):
               ret_tupes.append((arr[i],arr[j]))
     return ret_tupes

# check if stopwrds list given
give_sw = False
if len(sys.argv) > 2:
     sword_arr = []
     with open(sys.argv[2], 'r') as text_sw:
          stop_words = set()
          for line2 in text_sw:
               line2 = line2.strip()  # removes whitespace either side of our line
               swords = line2.split()
               swords = rem_punc(swords)
               for sword in swords:
                    sword_arr.append(sword)
          give_sw = True
else:
     pass


for root, dir, files in os.walk(sys.argv[1]): # chat gpt
     for file in files:
          with open(os.path.join(root, file), 'r') as text_1:
               for line in text_1:
                    line = line.strip()  # removes whitespace either side of our line
                    words = line.split()  # splitting our line into a list of words
                    words = rem_punc(words)
                    # check for stopwords input
                    if give_sw == True:
                         words = rem_sw(words, sword_arr)
                    else: # default list is suitable for binary search
                         words = rem_sw_binary(words)

                    pairs = get_pairs(words)

                    for p in pairs:
                         print('%s\t%s' % (p, 1))
