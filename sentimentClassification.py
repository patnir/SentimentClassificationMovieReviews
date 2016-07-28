# -*- coding: utf-8 -*-
"""
Created on Sun Jul 24 19:32:01 2016

@author: Rahul Patni
"""

# Sentiment classifications

#functions to write
#
#threshold
#
#compare
#
#optimization algorithm
#
#check against testing data
#
#define weights datastructure

import numpy
import os

def loadData(words):
    fptr = open("words.txt")
    for line in fptr:
        words.append(str(line.rstrip()))
    return
    
def printArray(X):
    for i in X:
        print i

def determinePresence(filename, words):
    fptr = open(filename)
    X = numpy.zeros(len(words))
    j = 0
    for line in fptr:
        line = line.split(" ")
        for i in line:
            i = i.rstrip()
            if i in words:
                X[j] = 1
            j += 1
    return X

def setFeatures(X, words, dirname):
    for i in os.listdir(dirname):
        if i.endswith(".txt"):
            print i
            X.append(determinePresence("{}/{}".format(dirname, i), words))

def initializeWeights(words):
    weights = numpy.zeros(len(words))
    return weights    
    
def main():
    words = []
    loadData(words) 
    #weights = initializeWeights(words)
    X = []
    setFeatures(X, words, "mix20_rand700_tokens_cleaned/tokens/training/posSmall")
    setFeatures(X, words, "mix20_rand700_tokens_cleaned/tokens/training/negSmall")
    print len(X)
    
if __name__ == "__main__":
    main()