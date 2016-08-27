# -*- coding: utf-8 -*-
"""
Created on Sat Aug 27 10:17:07 2016

@author: Rahul Patni
"""

# Storing features in file to make testing faster

import re

def loadWords(words):
    fptr = open("words.txt")
    for line in fptr:
        word = str(line.rstrip())
        if re.search('^[a-zA-Z]+$', word):
            words.append(word)
    fptr.close()
    return
    

def merge(A, start, mid, end):
    if end - start == 1:
        if A[start] > A[end]:
            temp = A[start]
            A[start] = A[end]
            A[end] = temp
        return
    B = []
    C = []
    for i in range(start, mid + 1):
        B.append(A[i])
    for i in range(mid + 1, end + 1):
        C.append(A[i])
    j = 0
    k = 0
    for i in range(start, end + 1):
        if  k >= len(C) or (j < len(B) and B[j] <= C[k]):
            A[i] = B[j]
            j += 1
        else:
            A[i] = C[k]
            k += 1
    return
    
def mergeSort(A, start, end):
    if start >= end:
        return
    mid = (start + end) / 2
    mergeSort(A, start, mid)
    mergeSort(A, mid + 1, end)
    merge(A, start, mid, end)
        
    
    
def main():
    #dirTest = "data2/tokens/posTraining"
    words = []
    loadWords(words)
    mergeSort(words, 0, len(words) - 1)
    #xTrain = []
    #yTrain = []
    #setFeaturesRandomly(words, xTrain, yTrain, dirNegTraining, dirPosTraining, True)
    print words
    return
    
main()