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

import operator
import os

words = dict()

def loadData(filename):
    fhand = open(filename)
    i = 0
    for line in fhand:
        line = line.split(" ")
        for i in line:
            if i in words:
                words[i] += 1
            else:
                words[i] = 1
    # sorted_x = sorted(words.items(), key=operator.itemgetter(0))

def goThroughDir(dirname):
    print os.listdir(os.getcwd())
    for i in os.listdir(dirname):
        if i.endswith(".txt"): 
            loadData("{}/{}".format(dirname, i))    

goThroughDir("mix20_rand700_tokens_cleaned/tokens/neg")
goThroughDir("mix20_rand700_tokens_cleaned/tokens/pos")


print words

print len(words)