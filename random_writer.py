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

# This is a dictionary that maps a phrase of ORDER length to a tuple of the number of
# times it has occured and a dictionary of characters that have followed and the number 
# of times they've occured
# 
# Example:
# occurrences[fragment] = (number_of_times_fragment_has_occured_in_text, {characters_that_follow_the_fragment: number_of_times_those_characters_occurred})
occurrences = {}

try:
    # Open text file for reading
    f = open(FILENAME, 'r')
except IOError:
    print 'No file found. Exiting'
    sys.exit()

text = f.read()
f.close()
# Go through each character in the inputted text
for index in range(len(text)-ORDER -1):
    fragment = text[index:index+ORDER] #the size of the fragment depends on the ORDER entered, the higher the order the more "sense" the output will have
    following_char = text[index+ORDER]
    if fragment in occurrences: 
        n_occurrences_total, following_char_dict = occurrences[fragment]
        n_occurrences_total += 1
        if following_char in following_char_dict:
            following_char_dict[following_char] += 1
        else:
            following_char_dict[following_char] = 1
        occurrences[fragment] = (n_occurrences_total, following_char_dict)
    else:
        following_char_dict = {following_char:1}
        occurrences[fragment] = (1, following_char_dict)

max_fragment = ''
max_occurrences = -1
# Find the most frequent frequently occurring fragment
for fragment in occurrences:
    n_occurrences, following_char_dict = occurrences[fragment]
    
    if n_occurrences > max_occurrences:
        max_occurrences = n_occurrences
        max_fragment = fragment

print max_fragment
seed = max_fragment
new_text = seed
random.seed()
max_iterations = 20000 # If you have large input this will cut off the number of iterations so the output isn't really long,
iterations = 0
# Create the output text
while True:
    if seed not in occurrences or iterations == max_iterations:
        break
    n_occurrences, following_char_dict = occurrences[seed]
    char_list = []
    total_hits = 0
    for char in following_char_dict:
        total_hits += following_char_dict[char]
        char_list.append((char, total_hits))
    # Randomly determine the next seed
    index = random.randint(0, total_hits)
    for char, hits in char_list:
        if index < hits:
            new_text += char
            # Take one char off the start and add the randomly chosen following character to create the new seed
            seed = seed[1:] + char
            break
    iterations += 1

print new_text
        
    

    

