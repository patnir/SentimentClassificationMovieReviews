# -*- coding: utf-8 -*-
"""
Created on Sun Jul 24 19:32:01 2016

@author: Rahul Patni
"""

# Sentiment classifications

#functions to write
#
#loadData
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

def loadData(words):
    fptr = open("words.txt")
    for line in fptr:
        words.append(str(line.rstrip()))
    return
    
    
def main():
    words = []
    loadData(words)
    print words
    
if __name__ == "__main__":
    main()