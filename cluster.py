# Author Austin James, all rights reserved.

print("\n")

import sys
import os
from collections import defaultdict
import math

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

            if ((z.upper()) not in stopwords) and (z != ""):
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

# Create a set of each documents highest and lowest frequency words -----------

highestFreqWords = []
lowestFreqWords = []

for x in mostFreqsData:
    for y in x:
        word = y[0]
        if word not in highestFreqWords:
            highestFreqWords.append(word)

for x in leastFreqsData:
    for y in x:
        word = y[0]
        if word not in lowestFreqWords:
            lowestFreqWords.append(word)

# -----------------------------------------------------------------------------

# Create the frequency vector for each documents highest and lowest frequency
# words

highestFreqVectors = []
lowestFreqVectors = []

for x in dataFilenames:
    highVector = []
    lowVector = []
    for y in highestFreqWords:
        highVector.append(0)
    for y in lowestFreqWords:
        lowVector.append(0)
    highestFreqVectors.append(highVector)
    lowestFreqVectors.append(lowVector)

for x in range(len(mostFreqsData)):
    for y in mostFreqsData[x]:
        indexOfWord = highestFreqWords.index(y[0])
        highestFreqVectors[x][indexOfWord] = y[1]

for x in range(len(leastFreqsData)):
    for y in leastFreqsData[x]:
        indexOfWord = lowestFreqWords.index(y[0])
        lowestFreqVectors[x][indexOfWord] = y[1]

# -----------------------------------------------------------------------------

# Normalize all frequency vectors ---------------------------------------------

for x in highestFreqVectors:
    sum = 0.0
    for y in x:
        sum += y*y
    normfactor = math.sqrt(sum)
    normfactor = 1/normfactor
    for y in range(len(x)):
        x[y] = float(x[y])*normfactor

for x in lowestFreqVectors:
    sum = 0.0
    for y in x:
        sum += y*y
    normfactor = math.sqrt(sum)
    normfactor = 1/normfactor
    for y in range(len(x)):
        x[y] = float(x[y])*normfactor

# -----------------------------------------------------------------------------

# Compute cosine similarities of all documents to all other documents ---------

highFreqSimilarities = []
lowFreqSimilarities = []

highAcceptableSimilarity = 0.5
lowAcceptableSimilarity = 0.126
identicalSimilarity = 0.99

for x in dataFilenames:
    highFreqSimilarities.append([])
    lowFreqSimilarities.append([])

for x in highestFreqVectors:
    for y in highestFreqVectors:
        similarity = 0.0
        for i in range(len(x)):
            similarity += x[i]*y[i]
        docIndex = highestFreqVectors.index(x)
        if (similarity >= highAcceptableSimilarity) and (similarity <= identicalSimilarity):
            highFreqSimilarities[docIndex].append(similarity)
        else:
            highFreqSimilarities[docIndex].append(0.0)

for x in lowestFreqVectors:
    for y in lowestFreqVectors:
        similarity = 0.0
        for i in range(len(x)):
            similarity += x[i]*y[i]
        docIndex = lowestFreqVectors.index(x)
        if (similarity >= lowAcceptableSimilarity) and (similarity <= identicalSimilarity):
            lowFreqSimilarities[docIndex].append(similarity)
        else:
            lowFreqSimilarities[docIndex].append(0.0)

# -----------------------------------------------------------------------------

# Find how many documents each document is similar to -------------------------

highRelations = []
lowRelations = []

print("     Document                    TF Relations   ITF Relations")

for x in range(len(highFreqSimilarities)):
    highRelateds = 0
    lowRelateds = 0
    for y in highFreqSimilarities[x]:
        if y > 0:
            highRelateds += 1
    for y in lowFreqSimilarities[x]:
        if y > 0:
            lowRelateds += 1
    docTitle = dataFilenames[x]
    print(docTitle+":\t\t"+str(highRelateds)+"\t\t"+str(lowRelateds))
    highRelations.append(highRelateds)
    lowRelations.append(lowRelateds)

sumHighRelations = 0
sumLowRelations = 0

for x in range(len(highRelations)):
    sumHighRelations += highRelations[x]
    sumLowRelations += lowRelations[x]

aveHighRelations = float(sumHighRelations)/float(len(dataFilenames))
aveLowRelations = float(sumLowRelations)/float(len(dataFilenames))

print("\n")
print("Average High Relations per Document: "+str(aveHighRelations))
print("Average Low Relations per Document: "+str(aveLowRelations))

# -----------------------------------------------------------------------------

print("\n")
