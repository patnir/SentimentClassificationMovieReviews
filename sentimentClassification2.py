# -*- coding: utf-8 -*-
"""
Created on Mon Aug 15 20:10:56 2016

@author: Rahul Patni
"""

# Trying sentiment classification again

import os
import random
import numpy

def printArray(array):
    for i in range(len(array)):
        print array[i]

def loadWords(words):
    fptr = open("words.txt")
    for line in fptr:
        words.append(str(line.rstrip()))
    fptr.close()
    return

def determinePresence(filename, words, isTraining):
    fptr = open(filename)
    if isTraining == True:
        X = numpy.zeros(len(words) + 1)
        X[len(words)] = 1
    else:
        X = numpy.zeros(len(words))
    j = 0
    for line in fptr:
        line = line.split(" ")
        for i in line:
            i = i.rstrip()
            if i in words:
                X[j] = 1
            j += 1
    # add an additional feature that is always on to x
    fptr.close()
    return X

def setFeatures(words, X, Y, dirneg, dirPos, isTraining):
    return

def setFeaturesRandomly(words, X, Y, dirNeg, dirPos, isTraining):
    i = 0 # Negative tracker
    j = 0
    negFiles = os.listdir(dirNeg) #Negative Files
    posFiles = os.listdir(dirPos)
    posExamples = len(posFiles)
    negExamples = len(negFiles)
    for k in range(posExamples + negExamples):
        check = random.randint(0, 1)
        # Negative examples
        if (check == 0 or j >= posExamples) and (i < negExamples):
            if isTraining == True:
                print "trianing from", negFiles[i]
            else:
                print "testing from", negFiles[i]
            X.append(determinePresence("{}/{}".format(dirNeg, negFiles[i]), words, isTraining))
            i += 1
            Y.append(0)
        # Positive examples
        else: 
            if isTraining == True:
                print "trianing from", posFiles[j]
            else:
                print "testing from", posFiles[j]
            X.append(determinePresence("{}/{}".format(dirPos, posFiles[j]), words, isTraining))
            j += 1
            Y.append(1)
    return

def threshold(weights, X):
    T = weights[len(weights) - 1]
    result = numpy.dot(weights, numpy.transpose(X))
    if result >= T:
        return 1
    return 0

def settingWeights(X, words, weights, Y, k):
    for j in range(k):
        for i in range(len(X)):
            result = threshold(weights, X[i]) 
            if result != Y[i]:
                if result == 1:
                    weights = numpy.subtract(weights, X[i])
                else: 
                    weights = numpy.add(weights, X[i])
                print weights
    return weights

def initializeWeights(words):
    weights = numpy.zeros(len(words) + 1)
    # the original weight vector, with Threshold added
    weights[len(words)] = 0
    return weights

def training(words, X, Y):
    dirNeg = "data2/tokens/neg"
    dirPos = "data2/tokens/pos" 
    setFeatures(words, X, Y, dirNeg, dirPos, True)
    weights = initializeWeights(words)
    k = 200
    weights = settingWeights(X, words, weights, Y, k)
    new_weights = []
    [new_weights.append(weights[x]) for x in range(len(weights) - 1)]
    T = weights[len(weights) - 1]
    return new_weights, T

def main():
    words = []
    X = []
    Y = []
    loadWords(words)
    weights, T = training(words, X, Y)
    #testing(words, weights, T)
    print T
    print "end"
    
if __name__ == "__main__":
    main()