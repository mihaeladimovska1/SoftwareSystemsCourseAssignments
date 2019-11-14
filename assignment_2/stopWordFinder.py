#!/usr/bin/python

#agr1: the file that countains count for each word (i.e. the part-00000.txt file)
#output: the stop words: words with frequency greater than 0.001

import sys


stopWords = {}
stopTreshhold = 0.001
# Determine how many total words were in the corpus of documents.
def getTotalWordsInStopFile(stopWordFileName):
    f = open(stopWordFileName, 'r')

    count = 0

    for line in f:
        l = line.split('\t')
        count += int(l[1])
    print(count)
    return count


def getStopWords(stopWordFileName):
    f = open(stopWordFileName, 'r')

    count = getTotalWordsInStopFile(stopWordFileName)

    for line in f:
        l = line.split('\t')
        fraction = float(l[1])/count
        if fraction > stopTreshhold:
            stopWords[l[0]] = float(l[1]);#1
    f.close()


if __name__ == "__main__":
    argCount = 2
    if len(sys.argv) < argCount:
        print("Please input the file name for stop words")
        sys.exit(0)


    stopFileName = sys.argv[1]


    getStopWords(stopFileName)#, stopPercent)
    #print(stopWords)
    print(len(stopWords))
    #print(max(stopWords))
    sw_list = []
    for k,v in stopWords.iteritems():
        sw_list.append(k)


    print(sw_list)
    with open("stopwords.txt", "w") as output:
        output.write(str(sw_list))

