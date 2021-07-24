"""
15-110 Hw6 - Social Media Analytics Project
Name: Logan Saito
AndrewID: lsaito
"""

import hw6_social_tests as test

project = "Social" # don't edit this

### WEEK 1 ###

import pandas as pd
import nltk
nltk.download('vader_lexicon', quiet=True)
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np

def makeDataFrame(filename):
    frame_df = pd.read_csv(filename)
    return frame_df

def parseName(fromString):
    parsedstr = fromString.strip("From: ")
    parsedlst = parsedstr.split(" (")
    name = parsedlst[0]
    return name

def parsePosition(fromString):
    parsedPos = fromString.split("(")
    parsedPos.pop(0)
    title = parsedPos[0]
    pos = title.split(" from")
    return pos[0]

def parseState(fromString):
    fromStr = fromString.replace(")", " ")
    parsedst = fromStr.split("from ")
    state = str(parsedst[1])
    state = state.strip(" ")
    return state

endChars = [ " ", "\n", "#", ".", ",", "?", "!", ":", ";", ")" ]

def findHashtags(message):
    taglst = []
    for i in range(len(message)):
        if message[i] == '#':
            j = i + 1
            while j < len(message) and message[j] not in endChars:
                j += 1
            taglst.append(message[i : j])

    return taglst

def getRegionFromState(stateDf, state):
    row = stateDf.loc[stateDf["state"] == state, "region"]
    region = row.values[0]
    return region

def addColumns(data, stateDf):
    namelst = []
    positionlst = []
    statelst = []
    regionlst = []
    hashtaglst = []

    for index, row in data.iterrows():
        labeldata = row["label"]
        colName = parseName(labeldata)
        namelst.append(colName)
        colPos = parsePosition(labeldata)
        positionlst.append(colPos)
        colSt = parseState(labeldata)
        statelst.append(colSt)
        colReg = getRegionFromState(stateDf, colSt)
        regionlst.append(colReg)
        textdata = row["text"]
        colHas = findHashtags(textdata)
        hashtaglst.append(colHas)

    data["name"] = namelst
    data["position"] = positionlst
    data["state"] = statelst
    data["region"] = regionlst
    data["hashtags"] = hashtaglst
    return None




### WEEK 2 ###

def findSentiment(classifier, message):
    score = classifier.polarity_scores(message)['compound']
    if score < -0.1:
        return "negative"
    if score > 0.1:
        return "positive"
    else:
        return "neutral"

def addSentimentColumn(data):
    classifier = SentimentIntensityAnalyzer()
    sentimentlst = []
    for index, row in data.iterrows():
        textdata2 = row["text"]
        colSent = findSentiment(classifier, textdata2)
        sentimentlst.append(colSent)
    data["sentiment"] = sentimentlst
    return None

def getDataCountByState(data, colName, dataToCount):
    dcount = {}
    if colName == "" and dataToCount == "":
        for index, row in data.iterrows():
            if row["state"] in dcount :
                dcount[row["state"]] += 1
            else:
                dcount[row["state"]] = 1
        return dcount
    else:
        for index, row in data.iterrows():
            if row[colName] == dataToCount:
                if row["state"] in dcount :
                    dcount[row["state"]] += 1
                else:
                    dcount[row["state"]] = 1
        return dcount

def getDataForRegion(data, colName):
    outerDict = {}
    totalWordsS = []
    totalWordsW = []
    totalWordsMw = []
    totalWordsNe = []
    for index, row in data.iterrows():
        outerDict[row["region"]] = {}
        if row["region"] == "South":
            spacedEntry1 = row[colName].split(" ")
            totalWordsS += spacedEntry1
        if row["region"] == "West":
            spacedEntry2 = row[colName].split(" ")
            totalWordsW += spacedEntry2
        if row["region"] == "Midwest":
            spacedEntry3 = row[colName].split(" ")
            totalWordsMw += spacedEntry3
        if row["region"] == "Northeast":
            spacedEntry4 = row[colName].split(" ")
            totalWordsNe += spacedEntry4
    for i in range(len(totalWordsS)):
        if totalWordsS[i] in outerDict:
            pass
        else:
            outerDict["South"][totalWordsS[i]] = totalWordsS.count(totalWordsS[i])
    for i in range(len(totalWordsW)):
        if totalWordsW[i] in outerDict:
            pass
        else:
            outerDict["West"][totalWordsW[i]] = totalWordsW.count(totalWordsW[i])
    for i in range(len(totalWordsMw)):
        if totalWordsMw[i] in outerDict:
            pass
        else:
            outerDict["Midwest"][totalWordsMw[i]] = totalWordsMw.count(totalWordsMw[i])
    for i in range(len(totalWordsNe)):
        if totalWordsNe[i] in outerDict:
            pass
        else:
            outerDict["Northeast"][totalWordsNe[i]] = totalWordsNe.count(totalWordsNe[i])
    return outerDict

def getHashtagRates(data):
    tagDict = {}
    taglst = []
    for index, row in data.iterrows():
        for i in row["hashtags"]:
            if i in tagDict:
                tagDict[i] += 1
            else:
                tagDict[i] = 1
    return tagDict

def mostCommonHashtags(hashtags, count):
    common = {}
    while len(common) < count:
        mostValue = 0
        key1 = 0
        for key in hashtags:
            if hashtags[key] >  mostValue and key not in common:
                mostValue = hashtags[key]
                key1 = key
        common[key1] = mostValue
    return common

def getHashtagSentiment(data, hashtag):
    score = 0
    count = 0
    for index, row in data.iterrows():
        tags = findHashtags(row["text"])
        if hashtag in tags:
            if row["sentiment"] == "positive":
                score += 1
                count += 1
            elif row["sentiment"] == "negative":
                score -= 1
                count += 1
            else:
                score += 0
                count += 1
    return score / count

### WEEK 3 ###

def graphStateCounts(stateCounts, title):
    keylst = []
    vallst = []
    for key in stateCounts:

        keylst.append(key)
        vallst.append(stateCounts[key])

    fig, ax = plt.subplots()
    ind = range(len(vallst))
    rects1 = ax.bar(ind, vallst)
    plt.xticks(rotation = "vertical")
    ax.set_title(title)
    ax.set_xticks(ind)
    ax.set_xticklabels(keylst)

    plt.show()
    return None

def graphTopNStates(stateCounts, stateFeatureCounts, n, title):
    rates = {}
    state = 0
    for state in stateFeatureCounts:
        frequencyrate = stateFeatureCounts[state] / stateCounts[state]
        rates[state] = frequencyrate

    commonStates = {}
    while len(commonStates) < n:
        mostValue = 0
        key1 = 0
        for state in rates:
            if rates[state] >  mostValue and state not in commonStates:
                mostValue = rates[state]
                key1 = state
        commonStates[key1] = mostValue
    graphStateCounts(commonStates, title)
    return None

def graphRegionComparison(regionDicts, title):
    featurelst = []
    for region in regionDicts:
        for feature in regionDicts[region]:
            if feature in featurelst:
                continue
            else:
                featurelst.append(feature)
    regionlst = []
    for region in regionDicts:
        regionlst.append(region)
    regionFeaturelst = []
    for region in regionDicts:
        templst = []
        for feature in featurelst:
            if feature in regionDicts[region]:
                templst.append(regionDicts[region][feature])
            else:
                templst.append(0)
        regionFeaturelst.append(templst)
    sideBySideBarPlots(featurelst, regionlst, regionFeaturelst, title)
    return None

def graphHashtagSentimentByFrequency(df):
    hashCounts = getHashtagRates(df)
    fiftyTags = mostCommonHashtags(hashCounts, 50)
    hashtaglst = []
    frequencylst = []
    scoreslst = []
    for hashtag in fiftyTags:
        hashtaglst.append(hashtag)
        frequencylst.append(hashCounts[hashtag])
        score = getHashtagSentiment(df, hashtag)
        scoreslst.append(score)
    scatterPlot(frequencylst, scoreslst, hashtaglst, "Hashtag Sentiment v. Frequency")



    return None


#### WEEK 3 PROVIDED CODE ####
"""
Expects 3 lists - one of x labels, one of data labels, and one of data values - and a title.
You can use it to graph any number of datasets side-by-side to compare and contrast.
"""
def sideBySideBarPlots(xLabels, labelList, valueLists, title):
    x = np.arange(len(xLabels)) # gets the indexes of the bars
    width = 0.8 / len(labelList)  # the width of the bars
    fig, ax = plt.subplots()
    for index in range(len(valueLists)):
        ax.bar(x - 0.4 + width*(index+0.5), valueLists[index], width, label=labelList[index])
    ax.set_xticks(x)
    ax.set_xticklabels(xLabels)
    plt.xticks(rotation="vertical")
    ax.legend()
    plt.title(title)
    fig.tight_layout()
    plt.show()

"""
Expects two lists of probabilities and a list of labels (words) all the same length
and plots the probabilities of x and y, labels each point, and puts a title on top.
Expects that the y axis will be from -1 to 1. If you want a different y axis, change plt.ylim
"""
def scatterPlot(xValues, yValues, labels, title):
    fig, ax = plt.subplots()

    plt.scatter(xValues, yValues)

    # make labels for the points
    for i in range(len(labels)):
        plt.annotate(labels[i], # this is the text
                    (xValues[i], yValues[i]), # this is the point to label
                    textcoords="offset points", # how to position the text
                    xytext=(0, 10), # distance from text to points (x,y)
                    ha='center') # horizontal alignment can be left, right or center

    ax.plot([0, 1], [0.5, 0.5], color='black', transform=ax.transAxes)
    plt.title(title)
    plt.ylim(-1, 1)
    plt.show()


### RUN CODE ###

# This code runs the test cases to check your work

if __name__ == "__main__":

    print("\n" + "#"*15 + " WEEK 1 TESTS " +  "#" * 16 + "\n")
    test.week1Tests()
    print("\n" + "#"*15 + " WEEK 1 OUTPUT " + "#" * 15 + "\n")
    test.runWeek1()

    ## Uncomment these for Week 2 ##

    print("\n" + "#"*15 + " WEEK 2 TESTS " +  "#" * 16 + "\n")
    test.week2Tests()
    print("\n" + "#"*15 + " WEEK 2 OUTPUT " + "#" * 15 + "\n")
    test.runWeek2()

    ## Uncomment these for Week 3 ##
    print("\n" + "#"*15 + " WEEK 3 OUTPUT " + "#" * 15 + "\n")
    test.runWeek3()