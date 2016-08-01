# -*- coding: utf-8 -*-
"""
Created on Mon Aug 01 18:52:38 2016

@author: Rahul Patni
"""

# classification by interchanging training files

import os
import random
import numpy


def loadWords(words):
    fptr = open("words.txt")
    for line in fptr:
        words.append(str(line.rstrip()))
    fptr.close()
    return

def determinePresence(filename, words):
    fptr = open(filename)
    X = numpy.zeros(len(words) + 1)
    j = 0
    for line in fptr:
        line = line.split(" ")
        for i in line:
            i = i.rstrip()
            if i in words:
                X[j] = 1
            j += 1
    # add an additional feature that is always on to x
    X[len(words)] = 1
    fptr.close()
    return X

def printArray(array):
    for i in array:
        print i

def setFeatures(words, X, Y, dirNeg, dirPos, negExamples, posExamples):
    i = 0 # Negative tracker
    j = 0
    negFiles = os.listdir(dirNeg) #Negative Files
    posFiles = os.listdir(dirPos)
    for k in range(posExamples + negExamples):
        check = random.randint(0, 1)
        print check
        # Negative examples
        if (check == 0 or j >= posExamples) and (i < negExamples):
            X.append(determinePresence("{}/{}".format(dirNeg, negFiles[i]), words))
            i += 1
            Y.append(0)
        # Positive examples
        else: 
            X.append(determinePresence("{}/{}".format(dirPos, posFiles[j]), words))
            j += 1
            Y.append(1)
            
    return

def training(words, X, Y):
    dirNeg = "mix20_rand700_tokens_cleaned/tokens/training/negSmall"
    dirPos = "mix20_rand700_tokens_cleaned/tokens/training/posSmall" 
    posExamples = 20
    negExamples = 20
    setFeatures(words, X, Y, dirNeg, dirPos, negExamples, posExamples)

def main():
    words = []
    X = []
    Y = []
    loadWords(words)
    training(words, X, Y)    
    
    
if __name__ == "__main__":
    main()