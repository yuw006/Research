# not needed
import spacy
import mysql.connector
import json
from itertools import combinations, permutations
import copy

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="1234567",
  database="framenet"
)
mycursor = mydb.cursor()
nlp = spacy.load("en_core_web_lg")
lemmatizer = nlp.get_pipe("lemmatizer")

labels = {"Entity" :("[Entity]","[/Entity]"), "Agent": ("[Agent]","[/Agent]"), "Theme":("[Theme]","[/Theme]"),\
          "Hidden_object": ("[Hidden_Obj]", "[/Hidden_Obj]"),\
          "Hiding_place": ("[Hiding_Place]","[/Hiding_Place]"), "Verb": ("[Verb]","[/Verb]")}


# sentence: type list of words
# phrases: type list of tuples of labels in order they appear in sentence
# return list of annotated sentence
# v_start start of verb v_back end of verb indices

# verb e1 e_curr
# e1 verb e_curr
# e1 e_curr verb

# verb e_curr e2
# e_curr verb e2
# e_curr e2 verb
# TODO debug this
# @param sentence array of words
def sortFunc(span):
    return span[0]
def splitList( noun_phrases, verb):
    front_list = []
    back_list = []
    for np in noun_phrases:
        if np[1] < verb[0]:
            front_list.append(np)
        else:
            back_list.append(np)
    front_list.sort(key=sortFunc)
    back_list.sort(key=sortFunc)
    return front_list, back_list

def combinePhrases( phrase_list ):
    dict_phrase_list={}
    for i in range(0, len(phrase_list)):
        dict_phrase_list[phrase_list[i][0]] = []
        for j in range(i, len(phrase_list)):
            start = phrase_list[i][0]
            end = phrase_list[j][1]
            dict_phrase_list[start].append((start,end))
    return dict_phrase_list

# @ret list of list of chosen_chunks
def waysToChooseChunks( startKey, dict_of_phrase_lists, num_chunks ):
    list_of_chosen_chunks = []
    if num_chunks == 1:
        for key in dict_of_phrase_lists:
            if key <= startKey:
                continue
            list_of_phrase = dict_of_phrase_lists[key]
            for phrase in list_of_phrase:
                list_of_chosen_chunks.append([phrase])
        return list_of_chosen_chunks
    for key in dict_of_phrase_lists:
        if key <= startKey:
            continue
        list_of_phrase = dict_of_phrase_lists[key]
        for phrase in list_of_phrase:
            list_of_phrase_lists = waysToChooseChunks( phrase[1], dict_of_phrase_lists, num_chunks-1)
            for pl in list_of_phrase_lists:
                list_of_chosen_chunks.append( [phrase] + pl)
    return list_of_chosen_chunks

# mpStart chunkStart chunkEnd mpEnd
# mpStart chunkStart mpEnd chunkEnd
# chunkStart mpStart chunkEnd mpEnd
# chunkStart mpStart mpEnd chunkEnd
def checkChunkBounds( verb, main_phrases, chunk ):
    for mp in main_phrases:
        if chunk[0] <= mp[1] and chunk[0] >= mp[0]:
            return False
        elif chunk[1] <= mp[1] and chunk[1] >= mp[0]:
            return False
    if chunk[0] <= verb[1] and chunk[0] >= verb[0]:
        return False
    elif chunk[1] <= verb[1] and chunk[1] >= verb[0]:
        return False
    return True

# gather other noun chunks together
def otherNounChunks( sentence, verb, main_phrases):
    other_chunks = []
    doc = nlp(sentence)
    for chunk in doc.noun_chunks:
        print(chunk)
        span = (chunk.start, chunk.end-1)
        if checkChunkBounds(verb, main_phrases, span):
            other_chunks.append(span)
    print( other_chunks )
    return other_chunks

# @param list of list of labels
# @ret dict of list of list of labels sorted by number of labels
def getPossibleLabels( list_label_list ):
    new_list = { 0: [[]], 1:[], 2:[], 3:[], 4:[], 5: []}
    for label_list in list_label_list:
        for i in range (1, len(label_list)+1):
            list_comb_tuple = combinations(label_list, i)
            for comb_tuple in list_comb_tuple:
                comb_list = list(comb_tuple)
                list_perm_tuple = permutations(comb_list)
                for perm_tuple in list_perm_tuple:
                    perm_list = list(perm_tuple)
                    if not (perm_list in new_list[i]):
                        new_list[i].append(perm_list)
    return new_list

def annotateSentence( label_keys, ents, sentence):
    new_ents = copy.deepcopy(ents)
    new_sentence = copy.deepcopy(sentence)
    for i in range(0, len(label_keys)):
        new_sentence[new_ents[i][0]] = labels[label_keys[i]][0] + new_sentence[new_ents[i][0]]
        new_sentence[new_ents[i][1]] = new_sentence[new_ents[i][1]] + labels[label_keys[i]][1]
    print( ' '.join(new_sentence))

# main label
# sentence text sentence for SRL
# verb (start_position, end position)
# main_phrases [(start, end),..., (start, end)]
def label( sentence, sentence_arr, verb, main_phrases):

    # find associated LU
    # TODO verb is conjugated
    # TODO if two verbs
    # normal situation
    main_verb = sentence_arr[verb[1]]
    print(sentence_arr)
    doc = nlp(main_verb)
    main_verb = doc[0].lemma_
    print("mainVerb", main_verb)
    sql = "SELECT * FROM framenet WHERE  phrase='" + main_verb + ".v'"
    mycursor.execute(sql)
    relevant_phrases = mycursor.fetchall()

    # get all FEs related to main_verb
    core_roles_list = []
    for phrase in relevant_phrases:
        #list of FEs for one instance of the verb
        phraseFEs = phrase[2]
        phraseFEs = json.loads(phraseFEs)

        #list of core FEs that are either Agent Theme Entity Hiding Place or Hidden Object
        core_phraseFEs = []
        for key in phraseFEs:
            if phraseFEs[key] in labels:
                core_phraseFEs.append(phraseFEs[key])

        core_roles_list.append(core_phraseFEs)
        print(core_phraseFEs)

    labeled_roles = getPossibleLabels(core_roles_list)
    other_phrases = otherNounChunks(sentence, verb, main_phrases)
    front_list, back_list = splitList((other_phrases+main_phrases), verb)
    front_dict = combinePhrases(front_list)
    back_dict = combinePhrases(back_list)
    front_dict.update(back_dict)
    print(labeled_roles)

    sentence_arr[verb[0]] = "[Verb]"+ sentence_arr[verb[0]]
    sentence_arr[verb[1]] = sentence_arr[verb[1]] + "[/Verb]"
    for l_key in labeled_roles:
        list_list_ents = waysToChooseChunks(-1, front_dict, l_key)
        for role_list in labeled_roles[l_key]:
            for list_ents in list_list_ents:
                annotateSentence(role_list, list_ents, sentence_arr)

