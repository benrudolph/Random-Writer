#!/usr/bin/env python

from pyquery import PyQuery as pq
from lxml import etree

import sys
import os
import re
import datetime
import operator

import random
PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))

if len(sys.argv) != 3:
    print 'usage: ./random_writer <text file> <order[1-10]>'

seed = ''
ORDER = int(sys.argv[2])
FILENAME = sys.argv[1]

# This is a dictionary that maps a phrase of ORDER length to following to a tuple of the number of times it has occured in the text and then the probability of the following character
occurences = {}

try:
    f = open(PROJECT_PATH + '/' + FILENAME, 'r')
except IOError:
    print 'No file found. Exiting'
    sys.exit()

text = f.read()
f.close()

for index in range(len(text)-ORDER -1):
    fragment = text[index:index+ORDER]
    following_char = text[index+ORDER]
    if fragment in occurences:
        n_occurences_total, following_char_dict = occurences[fragment]
        n_occurences_total += 1
        if following_char in following_char_dict:
            following_char_dict[following_char] += 1
        else:
            following_char_dict[following_char] = 1
        occurences[fragment] = (n_occurences_total, following_char_dict)
    else:
        following_char_dict = {following_char:1}
        occurences[fragment] = (1, following_char_dict)

max_fragment = ''
max_occurences = -1
for fragment in occurences:
    n_occurences, following_char_dict = occurences[fragment]
    
    if n_occurences > max_occurences:
        max_occurences = n_occurences
        max_fragment = fragment

print max_fragment
seed = max_fragment
new_text = seed
random.seed()
max_iterations = 20000
iterations = 0
while True:
    print seed    
    if seed not in occurences or iterations == max_iterations:
        break
    n_occurences, following_char_dict = occurences[seed]
    char_list = []
    total_hits = 0
    for char in following_char_dict:
        total_hits += following_char_dict[char]
        char_list.append((char, total_hits))
    index = random.randint(0, total_hits)
    for char, hits in char_list:
        if index < hits:
            new_text += char
            seed = seed[1:] + char
            break
    iterations += 1

print new_text
        
    

    

