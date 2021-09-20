# This File preps data to be used by lstm (not really needed）

import word
import numpy
from csv import writer
import spacy
import json

SENTENCE_LENGTH = 45
nlp = spacy.load("en_core_web_lg")
lemmatizer = nlp.get_pipe("lemmatizer")
chosen_verbs = ["cause","spark", "generate","create"]
def correctVerb(sentence, verb):
    verbPhrase = ""
    for i in range(verb[0],verb[1]+1):
        verbPhrase += (sentence[i].token_text + " ")
    doc = nlp(verbPhrase)
    for w in doc:
        if w.lemma_ in chosen_verbs:
            return True
    return False

def getOutput(sentence, outputSetence):
    start,end = -1,-1
    for i in outputSetence:
        if i.token_text == "EFFECT":
            if start == -1:
                start = i.token_index
            else:
                end = i.token_index
    output = [0] * SENTENCE_LENGTH
    if start == -1 or end == -1:
        print( "WASSUP", "".join(a.token_text for a in outputSetence))
    for i in range(start,end-1):
        #print(sentence[i].token_text)
        output[i] = 1
    return output
def annotateSentence(sentence, verb, subjs, objs):
    for i in range(verb[0], verb[1]+1):
        sentence[i].pos = [1,0,0]
    for s in subjs:
        for i in range(s[0], s[1]+1):
            sentence[i].pos = [0,1,0]
    for o in objs:
        for i in range(o[0], o[1]+1):
            sentence[i].pos = [0,0,1]
    return sentence

def prepData(sentence, verb, outputSentence, subjs, objs):

    #check if verb corresponds to any of the listed verb return if not
    #print(outputSentence)
    if (not correctVerb(sentence, verb)):
        return None,None
    else:
        #For every word in the sentence get the emedding plus the pos
        sentenceVector = []
        padding = [0] * 303
        i = 0
        sentence = annotateSentence(sentence, verb, subjs, objs);
        for w in sentence:
            wordVector = w.embedding + w.pos
            sentenceVector.append(wordVector)
            i+=1
        while i < SENTENCE_LENGTH:
            sentenceVector.append(padding)
            i+=1
        #data["sentences"].append(sentenceVector)
        #data["labels"].append(getOutput(sentence, outputSentence))
        outPutVector = getOutput(sentence, outputSentence)
        return sentenceVector, outPutVector


