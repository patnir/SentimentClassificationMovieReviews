# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 17:39:09 2016

@author: Rahul Patni
"""

# Sentiment Classification

#d = dict()
#
#for i in range(100):
#    key = i % 10
#    if key in d:
#        d[key] += 1
#    else:
#        d[key] = 1
#        
#print d

import os
import re

words = dict()

def loadData(filename):
    fhand = open(filename)
    i = 0
    for line in fhand:
        line = line.split(" ")
        for i in line:
            x = re.findall('[a-zA-Z!]+', i)
            if x != []:
                i = str(i)
                if i in words:
                    words[i] += 1
                else:
                    words[i] = 1
    fhand.close()
    # sorted_x = sorted(words.items(), key=operator.itemgetter(0))

def goThroughDir(dirname):
    print os.listdir(os.getcwd())
    for i in os.listdir(dirname):
        if i.endswith(".txt"): 
            loadData("{}/{}".format(dirname, i))    

def ChoosePivot(A, left, right):
    #return random.randint(left, right)
    median = int((left + right) / 2)
    medianValue = max(min(A[left],A[right]), min(max(A[left],A[right]),A[median]))

    if (medianValue == A[left]):
        return left
    if (medianValue == A[right]):
        return right
    return median

def QuickSort(A, left, right):
    if left >= right:
        return
    i = left + 1
    j = left + 1
    pivot = ChoosePivot(A, left, right)
    Swap(A, pivot, left)
    while j <= right:
        if A[j] < A[left]:
            Swap(A, i, j)
            i += 1
        j += 1
    Swap(A, left, i - 1)
    QuickSort(A, left, i - 2)
    QuickSort(A, i, right)
    return
   
def Swap(A, i, j):
    temp = A[i]
    A[i] = A[j]
    A[j] = temp
    return

goThroughDir("mix20_rand700_tokens_cleaned/tokens/neg")
goThroughDir("mix20_rand700_tokens_cleaned/tokens/pos")

#goThroughDir("sample")

x = list(words.items())

wordsList = []
occurences = []

for i in x:
    if (int(i[1] >= 4)):
        wordsList.append(i[0])
        occurences.append(i[1])
    
print len(wordsList)
print occurences

fptr = open("words.txt", "w")
for i in wordsList:
    fptr.write("{}\n".format(i))
fptr.close()