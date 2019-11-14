#!/usr/bin/python

import fileinput
import sys

file_name = ''   
new_content = ''       
delim = '\t'    
line_no = 0

# Go through each line and append the line number to it
# the line number is the first thing in every line then; 
# the line number is delimited by a tab from the rest of the text. 
for line in fileinput.input():
    file_name = fileinput.filename()
    line_no += 1
    new_content += str(line_no) + delim + line

f = open(file_name + 'Pr', 'w')

f.write(new_content)
f.close()