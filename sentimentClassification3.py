# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 23:56:04 2016

@author: Rahul Patni
"""

# Loading training and testing examples first

import os
import random
import numpy
import matplotlib.pyplot as plt

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
                X[j] += 1
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
    accuracy = (float(totalCorrect) / float(len(Y))) * 100
    print accuracy, "%"
    return accuracy

def settingWeights(words, xTrain, yTrain, xTest, yTest):
    weights = initializeWeights(words)
    k = 500
    accuracies = []
    for j in range(k):
        print "for k = ", k
        for i in range(len(xTrain) - 1):
            result = threshold(weights, xTrain[i]) 
            if result != yTrain[i]:
                if result == 1:
                    weights = numpy.subtract(weights, xTrain[i])
                else: 
                    weights = numpy.add(weights, xTrain[i])
        T = weights[len(weights) - 1]
        new_weights = []
        [new_weights.append(weights[x]) for x in range(len(weights) - 1)]
        accuracies.append(accuracyCheck(new_weights, T, xTest, yTest))
    plotData(accuracies)
    return

def plotData(y):
    plt.plot(y)
    plt.ylim(0, 110)
    plt.xlabel('Iterations')
    plt.ylabel('Accuracy %')
    plt.title('How accuracy varies as iterations increase')
    plt.show()

def main():
    words = []
    loadWords(words)
    #dirPosTraining = "data1/tokens/training/pos"
    dirPosTraining = "data2/tokens/posTraining"
    dirNegTraining = "data2/tokens/negTraining"
    xTrain = []
    yTrain = []
    setFeaturesRandomly(words, xTrain, yTrain, dirNegTraining, dirPosTraining, True)
    dirPosTesting = "data2/tokens/posTesting"
    dirNegTesting = "data2/tokens/negTesting"
    xTest = []
    yTest = []
    setFeaturesRandomly(words, xTest, yTest, dirNegTesting, dirPosTesting, False)
    settingWeights(words, xTrain, yTrain, xTest, yTest)
    print "done setting features"
    
    # then set weights
    
    
if __name__ == "__main__":
    main()