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
    fptr.close()
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
    fptr.close()
    return X

def setFeatures(X, words, dirname, Y):
    for i in os.listdir(dirname):
        if "pos" in dirname:
            Y.append(1)
        else:
            Y.append(0)
        if i.endswith(".txt"):
            print i
            X.append(determinePresence("{}/{}".format(dirname, i), words))
            
  
def determineValidationPresence(filename, words):
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
          
def setValidationFeatures(X, words, dirname, Y):
    for i in os.listdir(dirname):
        if "Pos" in dirname:
            Y.append(1)
        else:
            Y.append(0)
        if i.endswith(".txt"):
            print i
            X.append(determineValidationPresence("{}/{}".format(dirname, i), words))
            
    
def initializeWeights(words):
    weights = numpy.zeros(len(words) + 1)
    # the original weight vector, with Threshold added
    weights[len(words)] = 0
    return weights

def threshold(weights, X):
    # return 1 is the value is greater than the threshold
    # 1 if this indicates a positive review
    # 0 if it indicates a negative review
    T = weights[len(weights) - 1]
    result = numpy.dot(weights, numpy.transpose(X))
    if result >= T:
        return 1
    return 0
    
def training(X, words, weights, Y, k):
    for j in range(k):
        for i in range(len(X)):
            result = threshold(weights, X[i]) 
            if result != Y[i]:
                if result == 1:
                    weights = numpy.subtract(weights, X[i])
                else: 
                    weights = numpy.add(weights, X[i])
                print weights

def testing(words, weights):
    X = []
    Y = []
    setValidationFeatures(X, words, "mix20_rand700_tokens_cleaned/tokens/training/validationNegSmall", Y)
    setValidationFeatures(X, words, "mix20_rand700_tokens_cleaned/tokens/training/validationPosSmall", Y)
#    setValidationFeatures(X, words, "mix20_rand700_tokens_cleaned/tokens/pos/validation", Y)
#    setValidationFeatures(X, words, "mix20_rand700_tokens_cleaned/tokens/neg/validation", Y)
    new_weights = []
    T = weights[len(X) - 1]
    [new_weights.append(weights[i]) for i in range(len(weights) - 1)]
    totalCorrect = 0.0
    for i in range(len(X)):
        result = numpy.dot(new_weights, numpy.transpose(X[i]))
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
    
def main():
    words = []
    loadData(words) 
    #weights = initializeWeights(words)
    X = []
    Y = []
    setFeatures(X, words, "mix20_rand700_tokens_cleaned/tokens/training/negSmall", Y)
    setFeatures(X, words, "mix20_rand700_tokens_cleaned/tokens/training/posSmall", Y)
#    setFeatures(X, words, "mix20_rand700_tokens_cleaned/tokens/pos", Y)
#    setFeatures(X, words, "mix20_rand700_tokens_cleaned/tokens/neg", Y)
    weights = initializeWeights(words)
    # number of repetitions
    k = 10
    training(X, words, weights, Y, k)
    testing(words, weights)
    
    
if __name__ == "__main__":
    main()