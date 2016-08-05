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
    for i in range(int(len(array) / 10)):
        print array[i]

def setFeatures(words, X, Y, dirNeg, dirPos):
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
            print "trianing from", negFiles[i]
            X.append(determinePresence("{}/{}".format(dirNeg, negFiles[i]), words))
            i += 1
            Y.append(0)
        # Positive examples
        else: 
            print "trianing from", posFiles[j]
            X.append(determinePresence("{}/{}".format(dirPos, posFiles[j]), words))
            j += 1
            Y.append(1)
            
    return

def initializeWeights(words):
    weights = numpy.zeros(len(words) + 1)
    # the original weight vector, with Threshold added
    weights[len(words)] = 0
    return weights

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

def training(words, X, Y):
    dirNeg = "mix20_rand700_tokens_cleaned/tokens/neg/training"
    dirPos = "mix20_rand700_tokens_cleaned/tokens/pos/training" 
    setFeatures(words, X, Y, dirNeg, dirPos)
    weights = initializeWeights(words)
    k = 200
    weights = settingWeights(X, words, weights, Y, k)
    new_weights = []
    [new_weights.append(weights[x]) for x in range(len(weights) - 1)]
    T = weights[len(weights) - 1]
    return new_weights, T

def determineTestingPresense(filename, words):
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
    fptr.close()
    return X

def setTestingFeatures(words, X, Y, dirNeg, dirPos):
    negFiles = os.listdir(dirNeg) #Negative Files
    posFiles = os.listdir(dirPos)
    for i in negFiles:
        print "testing from negative", i
        X.append(determineTestingPresense("{}/{}".format(dirNeg, i), words))
        Y.append(0)
    for i in posFiles:
        print "testing from positive", i
        X.append(determineTestingPresense("{}/{}".format(dirPos, i), words))
        Y.append(1)

def accuracyCheck(weights, T, X, Y):
    totalCorrect = 0.0
    for i in range(len(X)):
        result = numpy.dot(weights, numpy.transpose(X[i]))
        if result >= T:
            result = 1
        else:
            result = 0
        print i, "result", result
        if result == Y[i]:
            totalCorrect += 1.0
    print "Percentage correct is"
    print (float(totalCorrect) / float(len(Y))) * 100
    return

def testing(words, weigths, T):
    X = []
    Y = []
    #dirNeg = "mix20_rand700_tokens_cleaned/tokens/training/validationNegSmall"
    #dirPos = "mix20_rand700_tokens_cleaned/tokens/training/validationPosSmall"
    dirNeg = "mix20_rand700_tokens_cleaned/tokens/neg/testing"
    dirPos = "mix20_rand700_tokens_cleaned/tokens/pos/testing"
    setTestingFeatures(words, X, Y, dirNeg, dirPos)
    accuracyCheck(weigths, T, X, Y)
    return

def main():
    words = []
    X = []
    Y = []
    loadWords(words)
    weights, T = training(words, X, Y)
    testing(words, weights, T)
    print "end"
    
if __name__ == "__main__":
    main()