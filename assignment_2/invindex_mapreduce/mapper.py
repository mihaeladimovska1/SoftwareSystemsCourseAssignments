#!/usr/bin/python
#!/usr/bin/env python


import sys
import string
import os
import fileinput
hadoopstring = 'hdfs://namenode:9000/'
stop_words = ['What', 'O,', 'all', 'hath', 'yet', 'had', 'should', 'to', 'he', "I'll", 'them', 'his', 'Of', 'thee', 'know', 'they', 'not', 'now', 'him', 'like', 'did', 'this', 'she', 'For', 'me,', 'some', 'see', 'are', 'our', 'out', 'what', 'for', 'That', 'I', 'then', 'He', 'be', 'we', 'do', 'This', 'never', 'here', 'let', 'O', 'come', 'by', 'on', 'would', 'thou', 'of', 'or', 'love', 'one', 'your', 'from', 'her', 'their', 'My', 'there', 'But', 'And', 'was', 'more', 'you,', 'that', 'but', 'So', 'with', 'than', 'must', 'me', 'To', 'these', 'say', 'us', 'will', 'can', 'were', 'my', 'and', 'give', 'is', 'am', 'it', 'an', 'How', 'as', 'good', 'at', 'have', 'in', 'You', 'if', 'no', 'make', 'when', 'how', 'take', 'which', 'you', 'With', 'A', 'shall', 'may', 'upon', 'most', 'sir,', 'Enter', 'such', 'The', 'man', 'a', 'thy', 'It', 'As', 'so', 'In', 'the', 'If']


for line in fileinput.input():
    file_name = os.environ['map_input_file']
    #we don't want the hadoop padding of the filename
    if file_name.startswith(hadoopstring):
        file_name = file_name.replace(hadoopstring, '')
    line = line.strip() 
    words = line.split()
    line_no = words[0]
    
    #print(words)
    for word in words[1:]:
        #remove punctuation
        word = word.translate(None, string.punctuation).lower()
        if word in stop_words or word == "":
            continue
        else:
            try:
                print ('%s\t%s\t%s' %( word, file_name, line_no))
            except KeyError:
                input_file = os.environ['map_input_file']

        