# this preps data that has unknown frames
import word
import numpy
from csv import writer
import csv
import spacy
import json
import math

nlp = spacy.load("en_core_web_lg")
lemmatizer = nlp.get_pipe("lemmatizer")

NAMED_ENTS = ["PERSON", "NORP", "FAC", "ORG", "GPE", "LOC", "PRODUCT",\
              "EVENT", "WORK_OF_ART", "LAW", "LANGUAGE", "DATE", "TIME", \
              "PERCENT", "MONEY", "QUANTITY", "ORDINAL", "CARDINAL"]
AVG_FILLING_VEC = [0] * 300
AVG_SEPERATING_VEC = [0] * 300
FILLING_VERBS = ["adorn","anoint","cover","dust","load","pack","smear","spread","stuff",\
                 "wrap", "plaster", "drape", "dab", "daub", "inject", "cram", "sow", \
                 "seed", "brush", "hang", "splatter", "spray", "sprinkle", "squirt", "shower",\
                 "drizzle", "heap", "heap", "pump", "jam", "plant", "scatter",\
                 "butter", "asphalt", "surface", "tile", "wallpaper", "coat", "suffuse", "fill",\
                 "strew", "douse", "flood", "crowd", "pave", "varnish", "paint", "glaze", \
                 "emblish", "panel", "wax", "wash", "plank", "yoke", "dress", "accessorize"]
SEPARATING_VERBS = ["bisect","divide","partition","section","segment","split","partition","sever"]
unGrouped_verbs = ["part","segregate","pile","gild","cram"]

def distanceToFillingVerbs(verb):
    AVG_FILLING_VEC=[0]*300
    for v in FILLING_VERBS:
        doc = nlp(v)
        AVG_FILLING_VEC += doc[0].vector
    AVG_FILLING_VEC /= len(FILLING_VERBS)

    doc1 = nlp(verb)
    verb_vector = doc1[0].vector

    dist = 0
    for i in range(0, len(verb_vector)):
        dist1 = 0
        dist1 += verb_vector[i]- AVG_FILLING_VEC[i]
        dist += dist1*dist1

    dist = math.sqrt(dist)

    return dist

def distanceToSeperatingVerbs(verb):
    AVG_SEPERATING_VEC=[0]*300
    for v in SEPARATING_VERBS:
        doc = nlp(v)
        AVG_SEPERATING_VEC += doc[0].vector
    AVG_SEPERATING_VEC /= len(SEPARATING_VERBS)

    doc1 = nlp(verb)
    verb_vector = doc1[0].vector

    dist = 0
    for i in range(0, len(verb_vector)):
        dist1 = 0
        dist1 += verb_vector[i]- AVG_SEPERATING_VEC[i]
        dist += dist1*dist1

    dist = math.sqrt(dist)

    return dist

def getContent(sentence, span):
    ent_list = []
    phrase = ""
    for i in range (span[0],span[1]+1):
        phrase += sentence[i].token_text + " "
    doc = nlp(phrase)
    print(phrase)
    for ent in doc.ents:
        ent_list.append(ent.label_)
    content = []
    for ent in NAMED_ENTS:
        if ent in ent_list:
            content.append("1")
        else:
            content.append("0")
    return content

def correctVerb(sentence, verb):
    verbPhrase = ""
    for i in range(verb[0], verb[1] + 1):
        verbPhrase += (sentence[i].token_text + " ")
    doc = nlp(verbPhrase)
    for w in doc:
        if w.lemma_ in unGrouped_verbs:
            return w.lemma_
        elif w.lemma_ in unGrouped_verbs:
            return w.lemma_
        elif w.lemma_ in unGrouped_verbs:
            return w.lemma_
    return -1

def prepData(sentence, verb, outputSentence, subjs, objs, isFilling):
    word = correctVerb(sentence, verb)
    if (word == -1):
        return None, None
    else:
        vec1 = getContent(sentence, subjs)
        print(vec1)
        vec2 = getContent(sentence, objs)
        print(vec2)
        dist1 = distanceToSeperatingVerbs(word)
        dist2 = distanceToFillingVerbs(word)
        row = (vec1 + vec2)#.append(str(dist1))#.append(str(dist2))
        row.append(str(dist1))
        row.append(str(dist2))
        print(row)
        with open("data_frame.csv", 'a', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)

            # writing the fields
            csvwriter.writerow(row)

        return None, None
