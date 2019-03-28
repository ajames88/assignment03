# Author Austin James, all rights reserved.

print("\n")

import sys
import os
from collections import defaultdict
import math

dataSetFilepath = "./dataSet"

outputFile = "output.txt"

out = open(outputFile, "w")

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

            if ((z.upper()) not in stopwords) and (z != "") and (len(z) > 1):
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

# Find 10 most frequent words used in each document ---------------------------
# * All terms with freq = 1 will be included in leastFreqs *
mostFreqsData = []

for x in frequencyData:
    mostFreqs = []

    # Apppend the 10 most and least freqs to the appropriate list
    for y in range(9):
        mostFreqs.append(x[y])

    mostFreqsData.append(mostFreqs)

# -----------------------------------------------------------------------------

# Create a set of each documents highest frequency words ----------------------

highestFreqWords = []

for x in mostFreqsData:
    for y in x:
        word = y[0]
        if word not in highestFreqWords:
            highestFreqWords.append(word)

out.write("Dimensions in frequency vector space: "+str(len(highestFreqWords)))
out.write("\n\n")
# -----------------------------------------------------------------------------

# Create the frequency vector for each documents highest frequency words ------

highestFreqVectors = []

for x in dataFilenames:
    highVector = []
    for y in highestFreqWords:
        highVector.append(0)
    highestFreqVectors.append(highVector)

for x in range(len(mostFreqsData)):
    for y in mostFreqsData[x]:
        indexOfWord = highestFreqWords.index(y[0])
        highestFreqVectors[x][indexOfWord] = y[1]

# -----------------------------------------------------------------------------

# Compute the idf value for each of the highest frequency terms ---------------

docFreq = []
idfValues = []

for x in highestFreqWords:
    docFreq.append(0)

for x in highestFreqVectors:
    for y in range(len(x)):
        if x[y] > 0:
            docFreq[y] += 1

for x in docFreq:
    idfValues.append((1+math.log10((len(dataFilenames)/x))))

# -----------------------------------------------------------------------------

# Multiply each term frequency by its idf value -------------------------------

freqVectors = []

for x in dataFilenames:
    freqVectors.append([])

for x in range(len(highestFreqVectors)):
    for y in range(len(highestFreqVectors[x])):
        freqVectors[x].append(highestFreqVectors[x][y]*idfValues[y])

# -----------------------------------------------------------------------------

# Normalize all frequency vectors ---------------------------------------------

for x in freqVectors:
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

highAcceptableSimilarity = 0.325
identicalSimilarity = 0.99

for x in dataFilenames:
    highFreqSimilarities.append([])

for x in freqVectors:
    for y in freqVectors:
        similarity = 0.0
        for i in range(len(x)):
            similarity += x[i]*y[i]
        docIndex = freqVectors.index(x)
        if (similarity >= highAcceptableSimilarity) and (similarity <= identicalSimilarity):
            highFreqSimilarities[docIndex].append(similarity)
        else:
            highFreqSimilarities[docIndex].append(0.0)

# -----------------------------------------------------------------------------

# Find how many documents each document is similar to -------------------------

highClusters = []

numHighRelations = []

for x in range(len(highFreqSimilarities)):
    highClusters.append([])
    highRelateds = 0
    doc = mostFreqsData[x]
    docWords = []
    for a in doc:
        docWords.append(a[0])
    similarWords = []
    for y in range(len(highFreqSimilarities[x])):
        if highFreqSimilarities[x][y] > 0:
            highRelateds += 1
            highClusters[x].append(dataFilenames[y])
            cur = mostFreqsData[y]
            curWords = []
            for b in cur:
                curWords.append(b[0])
            for z in docWords:
                if (z in curWords) and (z not in similarWords):
                    similarWords.append(z)
    if highRelateds > 0:
        docTitle = dataFilenames[x]
        out.write(docTitle+"\n")
        out.write("TFIDF Relations: "+str(highRelateds)+"\n")
        out.write("Cluster: "+str(highClusters[x])+"\n")
        out.write("Similar Words: "+str(similarWords)+"\n\n")
    numHighRelations.append(highRelateds)

sumHighRelations = 0

for x in range(len(numHighRelations)):
    sumHighRelations += numHighRelations[x]

aveHighRelations = float(sumHighRelations)/float(len(dataFilenames))

out.write("\n")
out.write("Average relations per Document: "+str(aveHighRelations))
out.write("\n")

# -----------------------------------------------------------------------------

out.close()
