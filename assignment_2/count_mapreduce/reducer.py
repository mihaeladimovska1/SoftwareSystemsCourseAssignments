#!/usr/bin/env python
"""reducer.py"""

from operator import itemgetter
import sys

current_word = None
current_count = 0
word = None


# Go through all of the items in the dictionary.
# If the word has already been seen, increment the count.
# If not, add it.

for line in sys.stdin:
    # remove whitespace
    line = line.strip()
    try:
        word, count = line.split('\t', 1)
        count = int(count)
    except ValueError:
        # count was not a number, so silently
        # ignore/discard this line
        continue

    
    if current_word == word:
        current_count += count
    else:
        if current_word:
      
            print '%s\t%s' % (current_word, current_count)
        current_count = count
        current_word = word

if current_word == word:
    print '%s\t%s' % (current_word, current_count)
