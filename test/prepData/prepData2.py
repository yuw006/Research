# This file preps data to be taken by svm and decision tree sorting

import word
import numpy
from csv import writer
import csv
import spacy
import json

PHRASE_LENGTH = 10
nlp = spacy.load("en_core_web_lg")
lemmatizer = nlp.get_pipe("lemmatizer")

chosen_verbs = {"speration":["split","part"], "body_movement":["roll","throw"],"filling":["cover","stuff"]}

#determine the overlapping percentage of two phrases
def phraseOverlap(phrase1, phrase2):
    if (phrase1 == (1000,-1)):
        return 0
    print("obj/subj ", phrase1, "judgedPhrase ", phrase2)
    length = phrase1[1]-phrase1[0] + 1#obj or subj
    #check if outside
    if( phrase1[1] < phrase2[0] ):
        return 0
    elif( phrase1[0] > phrase2[1]):
        return 0
    if( phrase1[0] < phrase2[0] ):
        length2 = (min(phrase1[1],phrase2[1])-phrase2[0]+1)
        if length2 <= 0:
            return 0
        else:
            return length2/length
    elif (phrase1[1] > phrase2[1] ):
        length2 = (max(phrase1[0], phrase2[0])-phrase1[0]+1)
        if length2 <= 0:
            return 0
        else:
            return length2/length

    else:
        return 1

def getPhrase(sentence, outputSetence):
    start,end = -1,-1
    for i in outputSetence:
        if i.token_text == "phraseTag":
            if start == -1:
                start = i.token_index
            else:
                end = i.token_index
    #print(start,end)
    return (start,end-2)

#getting frame of the word
def correctVerb(sentence, verb):
    verbPhrase = ""
    for i in range(verb[0], verb[1] + 1):
        verbPhrase += (sentence[i].token_text + " ")
    doc = nlp(verbPhrase)
    for w in doc:
        if w.lemma_ in chosen_verbs["speration"]:
            return 1
        elif w.lemma_ in chosen_verbs["body_movement"]:
            return 2
        elif w.lemma_ in chosen_verbs["filling"]:
            return 3
    return -1
def getVectors(sentence, phrase):
    i = 0
    sentenceVector = []
    padding = [0] * 303
    for j in range(phrase[0],phrase[1]+1):
        sentenceVector += (sentence[j].embedding + sentence[j].pos)
        i+=1
    while i < PHRASE_LENGTH:
        sentenceVector += padding
        i += 1
    return sentenceVector

def prepData(sentence, verb, outputSentence, subjs, objs, isAgent):
    frame = correctVerb(sentence, verb)
    if (frame == -1):
        return None,None
    else:
        phrase = getPhrase(sentence, outputSentence)
        isSubj = 0
        for subj in subjs:
            isSubj = max(isSubj, phraseOverlap(subj, phrase))
            print("isSubj",isSubj)

        isObj = 0
        #print("this is phrase ", phrase)
        #print("this is objs ", objs)
        for obj in objs:
            isObj = max(isObj, phraseOverlap(obj, phrase))
            print("isObj",isObj)
        if isAgent == "TRUE\n":
            isAgent = 1
        else:
            isAgent = 0
        row = [str(frame),str(isSubj),str(isObj),str(isAgent)]
        with open("data_frame.csv", 'a', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)

            # writing the fields
            csvwriter.writerow(row)
        if phrase[1]-phrase[0]<=PHRASE_LENGTH:
            vec = getVectors(sentence, phrase)
            return vec, isAgent
        return None, None