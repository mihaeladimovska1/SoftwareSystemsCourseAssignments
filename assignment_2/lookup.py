#!/usr/bin/python

#agr1: the inverted index file
#arg2: string of words the user is searching for
#output: the inverted index entry of each of the words in the arg2 string
import sys
import string

if __name__ == "__main__":
    argCount = 3
    if len(sys.argv) < argCount:
        print("Please input: (1) the inverted index file and (2) the string of words you want to search for, separated by a comma.")
        sys.exit(0)

    invIndexFileName = sys.argv[1]
    input_string = sys.argv[2]
    words = input_string.split(',')
    f = open(invIndexFileName, 'r')
    flag = False
    for line in f:
        l = line.split('\t')
        word = l[0].strip()

        if word in words:
            flag = True
            inv_index = l[1];
            print 'The word: ', word, 'appears in ([document, line]): '
            print(inv_index)
    
    if not flag:
        print 'The words: ', words, 'do not appear in any document. '

    f.close()
