# Author Austin James, all rights reserved.

import sys
import os

# Read in the list of stopwords from 'stopwords.txt' --------------------------

read = open("./stopwords.txt", "r")

stopwords = []

for x in read:
    word = x.strip()
    stopwords.append(word.upper())

# The list of stopwords is now contained in the list stopwords ----------------

# Parse student document ------------------------------------------------------

dataSetFilepath = "./studentDocuments"

dataFilenames = os.listdir(dataSetFilepath)

dataSet = []

for x in dataFilenames:
    dataFile = dataSetFilepath+"/"+x
    file = open(dataFile, "r")
    parsedFile = []
    for y in file:
        dataLine = y.split()
        for z in dataLine:
            if (z.upper()) not in stopwords:
                parsedFile.append(z)
    dataSet.append(parsedFile)

# -----------------------------------------------------------------------------
