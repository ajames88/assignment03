# Author Austin James, all rights reserved.

import sys
import os
from collections import defaultdict

alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
        'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

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
        rawLine = y.upper()
        dataLine = rawLine.split()
        for z in dataLine:

            for w in range(len(z)):
                if z[w] not in alphabet:
                    z = z.replace(z[w], " ")

            z = z.replace(" ", "")

            if (z.upper()) not in stopwords:
                parsedFile.append(z)

    dataSet.append(parsedFile)

# -----------------------------------------------------------------------------


# Perform frequency count of words --------------------------------------------

frequencyData = []

for x in dataSet:
    freqs = defaultdict(int)
    for y in x:
        freqs[y] += 1
    sortedFreqs = sorted(freqs.items(), key=lambda(k,v): v, reverse = True)
    frequencyData.append(sortedFreqs)

# -----------------------------------------------------------------------------

# Find 10 most and least frequent words used in each document -----------------
# * All terms with freq = 1 will be included in leastFreqs *
mostFreqsData = []
leastFreqsData = []

for x in frequencyData:
    mostFreqs = []
    leastFreqs = []

    # Apppend the 10 most and least freqs to the appropriate list
    for y in range(9):
        mostFreqs.append(x[y])
        leastFreqs.append(x[(len(x)-(y+1))])

    # Append all terms with freq = 1 to leastFreqs
    for y in x:
        if y[1] == 1:
            if y not in leastFreqs:
                leastFreqs.append(y)

    mostFreqsData.append(mostFreqs)
    leastFreqsData.append(leastFreqs)

# -----------------------------------------------------------------------------

# Pair based on highest frequency words ---------------------------------------

rawHighestClusters = []

for x in range(len(mostFreqsData)-1):
    currentDocument = dataFilenames[x]
    freqs = mostFreqsData[x]
    rawHighestClusters.append([(currentDocument, freqs)])
    for y in range(len(mostFreqsData)-1):
        compareDocument = dataFilenames[y]
        compareFreqs = mostFreqsData[y]
        common = 0
        for z in freqs:
            if z in compareFreqs:
                common += 1
        if common >= 3:
            rawHighestClusters[x].append((compareDocument, compareFreqs))

# -----------------------------------------------------------------------------

# Refine clusters to remove singles -------------------------------------------

highestClusters = []

for x in rawHighestClusters:
    if len(x) > 2:
        highestClusters.append(x)

# -----------------------------------------------------------------------------

# Print clusters --------------------------------------------------------------

for x in highestClusters:
    print("Cluster")
    for y in x:
        print(y[0])
        print(y[1])
    print("\n")

# -----------------------------------------------------------------------------
