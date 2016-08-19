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

def setFeatures(words, X, Y, dirNeg, dirPos, isTraining):
    negFiles = os.listdir(dirNeg)
    posFiles = os.listdir(dirPos)
    for i in negFiles:
        if isTraining == True:
                print "trianing from", i
        else:
            print "testing from", i
        X.append(determinePresence("{}/{}".format(dirNeg, i), words, isTraining))
        Y.append(0)
    for j in posFiles:
        if isTraining == True:
                print "trianing from", j
        else:
            print "testing from", j
        X.append(determinePresence("{}/{}".format(dirPos, j), words, isTraining))
        Y.append(1)
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
        for i in range(len(X) - 1):
            result = threshold(weights, X[i]) 
            if result != Y[i]:
                if result == 1:
                    weights = numpy.subtract(weights, X[i])
                else: 
                    weights = numpy.add(weights, X[i])
        new_weights = []
        [new_weights.append(weights[x]) for x in range(len(weights) - 1)]
        T = weights[len(weights) - 1]
        testing(words, new_weights, T)
    return new_weights

def initializeWeights(words):
    weights = numpy.zeros(len(words) + 1)
    # the original weight vector, with Threshold added
    weights[len(words)] = 0
    return weights

def training(words, X, Y):
    #dirNeg = "data2/tokens/negTraining"
    dirNeg = "data1/tokens/training/neg"
    #dirPos = "data2/tokens/posTraining" 
    dirPos = "data1/tokens/training/pos"
    setFeaturesRandomly(words, X, Y, dirNeg, dirPos, True)
    weights = initializeWeights(words)
    k = 1000
    weights = settingWeights(X, words, weights, Y, k)
    new_weights = []
    [new_weights.append(weights[x]) for x in range(len(weights) - 1)]
    T = weights[len(weights) - 1]
    return new_weights, T

def accuracyCheck(weights, T, X, Y):
    totalCorrect = 0.0
    for i in range(len(X)):
        result = numpy.dot(weights, numpy.transpose(X[i]))
        if result >= T:
            result = 1
        else:
            result = 0
        #print i, "result", result
        if result == Y[i]:
            totalCorrect += 1.0
    print "Accuracy:",
    print (float(totalCorrect) / float(len(Y))) * 100, "%"
    return

def testing(words, weigths, T):
    X = []
    Y = []
    #dirNeg = "data2/tokens/negTesting"
    dirNeg = "data1/tokens/training/negSmall"
    #dirPos = "data2/tokens/posTesting"
    dirPos = "data1/tokens/training/posSmall"
    setFeatures(words, X, Y, dirNeg, dirPos, False)
    accuracyCheck(weigths, T, X, Y)
    return

def main():
    words = []
    X = []
    Y = []
    loadWords(words)
    weights, T = training(words, X, Y)
    testing(words, weights, T)
    
if __name__ == "__main__":
    main()