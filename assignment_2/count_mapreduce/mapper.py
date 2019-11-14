#!/usr/bin/env python
"""mapper.py"""

import sys
import string

for line in sys.stdin:
    # remove whitespace
    line = line.strip()
    # split the line into words
    words = line.split()
    # increase counters
    for word in words:
        print '%s\t%s' % (word.translate(None, string.punctuation).lower(), 1)
