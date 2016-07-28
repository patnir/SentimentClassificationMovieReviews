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
        print i,

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
    return X

def setFeatures(X, words, dirname, Y):
    for i in os.listdir(dirname):
        if "posSmall" in dirname:
            Y.append(1)
        else:
            Y.append(0)
        if i.endswith(".txt"):
            print i
            X.append(determinePresence("{}/{}".format(dirname, i), words))

def initializeWeights(words):
    weights = numpy.zeros(len(words) + 1)
    # the original weight vector, with Threshold added
    weights[len(words)] = 0
    return weights

def threshold(weights, X):
    # return 1 is the value is greater than the threshold
    # 1 if this indicates a positive review
    # 0 if it indicates a negative review
    T = weights[len(X) - 1]
    result = numpy.dot(weights, numpy.transpose(X))
    if (result > T):
        return 1
    return 0
    
def training(X, words, weights, Y):
    for i in range(len(X)):
        result = threshold(weights, X[i]) 
        if result != Y[i]:
            if result == 1:
                weights = numpy.subtract(weights, X[i])
            else: 
                weights = numpy.add(weights, X[i])
    printArray(weights)
    
def main():
    words = []
    loadData(words) 
    #weights = initializeWeights(words)
    X = []
    Y = []
    setFeatures(X, words, "mix20_rand700_tokens_cleaned/tokens/training/posSmall", Y)
    setFeatures(X, words, "mix20_rand700_tokens_cleaned/tokens/training/negSmall", Y)
    print len(X)
    print len(X[0])
    weights = initializeWeights(words)
    print len(weights)
    training(X, words, weights, Y)
    
if __name__ == "__main__":
    main()