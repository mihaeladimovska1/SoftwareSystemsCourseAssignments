#!/usr/bin/python
#!/usr/bin/env python

from operator import itemgetter
import sys
from ast import * 


current_word = None
current_count = 0
inv_index = {}
word = None
# Go through all of the items in the dictionary.
# If the word has already been seen, increment the count, add the new filename and the new line the word appears at.
# If not, add it.
for line in sys.stdin:
    line = line.strip()
    word, file_name, line_no = line.split('\t', 3)
    if current_word == word:
        
        inv_index[current_word].extend([ '(' + file_name + ',' + line_no + ')'])

    else:
        if current_word:

            print '%s\t%s' % (current_word, str(inv_index[current_word]))
        
        current_word = word
        inv_index[word] = (['(' + file_name + ',' + line_no + ')'])



if current_word == word:
    print '%s\t%s' % (current_word, str(inv_index[current_word]))
