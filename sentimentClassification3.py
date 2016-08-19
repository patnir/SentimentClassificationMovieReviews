# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 23:56:04 2016

@author: Rahul Patni
"""

# Loading training and testing examples first

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
  
def main():
    words = []
    loadWords(words)
    dirPosTraining = "data1/tokens/training/pos"
    dirNegTraining = "data1/tokens/training/neg"
    xTrain = []
    yTrain = []
    setFeaturesRandomly(words, xTrain, yTrain, dirNegTraining, dirPosTraining, True)
    dirPosTesting = "data1/tokens/training/posSmall"
    dirNegTesting = "data1/tokens/training/negSmall"
    xTest = []
    yTest = []
    setFeaturesRandomly(words, xTest, yTest, dirNegTesting, dirPosTesting, False)
    print "done setting features"
    # then set weights
    
    
if __name__ == "__main__":
    main()