# Where processing happens

import spacy
import copy
from prepData.prepData3 import prepData
from objects.DependencyTree import Tree, Node
from objects.word import *
from rules.OtherRules import *
from rules.CondenseRules import *
from objects.Label import *

#from read import args
nlp = spacy.load("en_core_web_lg")

JSON_PATH = "data_frame.json"
data = {
    "phrases":[],
    "isAgent":[]
}

def runall(args):
    #files
    readfile = open("outputs./" + args.read + ".txt","r", encoding="utf-8")
    treefile = open("outputs./" + args.read + "_trees.txt","w",encoding="utf-8")
    resultfile = open("outputs./" + args.read + "_results.txt","w",encoding="utf-8")

    while True:
        tree = None #root of the tree
        doc_num #document number
        sentence_num #sentence_number
        sentence #sentence string
        an_sentence #sentence with role annotated
        sentence_array = [] #sentece array of Words
        sentence_obj_array = [] #annotate sentence array of Words

        doc_num = readfile.readline()
        if doc_num == "":
            break
        sentence_num = readfile.readline()

        # for reading from file
        sentence = readfile.readline().strip("\n")
        an_sentence = readfile.readline()
        isAgent = readfile.readline()
        doc = nlp(sentence)

        #initializes tree
        for token in doc:
            if token.dep_ == "ROOT":
                root = Node(None, token.dep_, token.text, token.pos_, (token.i, token.i))
                tree = Tree(root)
                tree.createTree(token, root)

        #creates sentence array of Words
        for token in doc:
            word_obj = Word(token.i, token.text, sentence_num, doc_num, token.head.text, token.dep_, token.ent_type_, token.pos_, token.tag_, token.vector, token.pos_)
            sentence_obj_array.append(word_obj)
            sentence_array.append(word_obj.token_text)

        #creates annotated sentence array of Words
        doc2 = nlp(an_sentence)
        an_sentence_obj_array = []
        for token in doc2:
            word_obj = Word(token.i, token.text, sentence_num, doc_num, token.head.text, token.dep_, token.ent_type_,
                            token.pos_, token.tag_, token.vector, token.pos_)
            an_sentence_obj_array.append(word_obj)

        # extracts word phrases from sentence
        #TODO: implement loop on rule 1,2
        for v in tree.verb:
            condense0(tree, v)
        for v in tree.verb:
            condense1(tree, v)
        for v in tree.verb:
            condense2(tree, v)
        for v in tree.verb:
            condense3(tree, v)
        for v in tree.verb:
            condense3_5(tree, v)
        for v in tree.verb:
            condense4(tree, v)

        # go to next sentence if tree is not created
        if tree:
            num_verbs = len(tree.verb)
        else:
            continue

        # go through all verb phrases in sentence
        for i in range(num_verbs):
            tree_copy = copy.deepcopy(tree) #save a version of originial tree
            prep_aff = [] #for list of affiliated preps
            verb_aff = [] #for list of affiliated verbs
            verb_span #for the span of the verb
            main_obj #span of obj associated with main verb
            obj_phrases = [] #span of objs in general
            subj_phrase #span of subj

            #writes intital tree to tree file
            if( args.write_tree ):
                treefile.write(sentence_num + sentence+"    verb: " + tree.verb[i].text +"\ninitial Tree:\n")
                tree.levelTraversal(treefile)
                treefile.write("\n")

            #occasionally the tree isn't completely built so this catches it
            if( tree.verb == None):
                if args.write_result:
                    resultfile.write("no verb: " + tree.verb[i].text + " in sentence " + sentence_num)
            else:
                # extract information on main verb
                growth1(tree, tree.verb[i])
                growth2_2(tree, tree.verb[i])
                growth3to4(tree, tree.verb[i])
                growth5(tree, tree.verb[i])
                reduction6(tree, tree.verb[i])
                reduction7(tree, tree.verb[i])
                reduction8to9(tree, tree.verb[i])
                subj_obj10(tree, tree.verb[i])
                subj_obj11(tree, tree.verb[i])
                subj_obj12(tree, tree.verb[i])
                subj_obj13(tree, tree.verb[i])
                #check for negation
                negation = tree.check_negation(tree.verb[i])

                #extract information on associated verb/ preps
                for aff in tree.verb[i].affliation:
                    if aff.dep == "prep":
                        pass
                        growth1(tree, aff)
                        growth2_2(tree, aff)
                        growth3to4(tree, aff)
                        growth5(tree, aff)
                    reduction6(tree, aff)
                    reduction7(tree, aff)
                    reduction8to9(tree, aff)
                    subj_obj10(tree, aff)
                    subj_obj11(tree, aff)
                    subj_obj12(tree, aff)
                    subj_obj13(tree, aff)

                # print to file
                # prints transformed tree
                if args.write_tree:
                    treefile.write("\ntransformed Tree:\n")
                    tree.levelTraversal(treefile)
                    treefile.write("\n")

                verb_span = tree.verb[i].coIndex

                #split words affiliated with tree into two categories
                for aff in tree.verb[i].affliation:
                    if ( aff.pos_tag == "VERB"):
                        verb_aff.append(aff.index)
                    if( tree.has_obj(aff) ):
                        prep_aff.append(aff)

                main_obj = tree.has_obj(tree.verb[i])

                phrases = []

                verb_span.append(tree.verb[i].index)

                if True or (tree.has_subj(tree.verb[i]) and (main_obj or affil)):

                    # prints tree results
                    if args.write_result:
                        resultfile.write("doc id: " + doc_num)
                        resultfile.write("sentence id: " + sentence_num)
                        resultfile.write(sentence + "\n")
                        resultfile.write("verb: " + tree.verb[i].text + "\n \n")

                    phrase_span = tree.getSubjects(resultfile, tree.verb[i], args.write_result)
                    #phrases.append(phrase_span)
                    subj_phrase = phrase_span

                    if( main_obj ):
                        phrase_span = tree.getObjects(resultfile, tree.verb[i], args.write_result)
                        if args.write_result:
                            #negation = tree.check_negation(aff)
                            phrases.append(phrase_span)
                            obj_phrases.append(phrase_span)
                            #resultfile.write("Negation: " + str(negation) + "\n")

                    for aff in affil:
                        if args.write_result:
                            resultfile.write("\n" + aff.text + "\n")
                        phrase_span = tree.getObjects(resultfile, aff, args.write_result)
                        phrases.append(phrase_span)
                        obj_phrases.append(phrase_span)

                del tree
                tree = tree_copy

                #prepare data for ML
                if( args.select_span ):
                    for vsp in verb_span:
                        label(sentence, sentence_array, vsp, phrases)

                for vsp in verb_span:
                    subj_phrase_span,obj_phrase_span=(-1,-1), (-1,-1)
                    if subj_phrase:
                        subj_phrase_span = subj_phrase
                    if obj_phrases:
                        obj_phrase_span = main_obj
                    input_data, output_data = prepData(sentence_obj_array, vsp, an_sentence_obj_array, subj_phrase_span, obj_phrase_span, True)

            if args.write_result:
                resultfile.write("\n")


        del tree
        del tree_copy

    readfile.close()
    resultfile.close()
    treefile.close()

    #with open(JSON_PATH, "w") as fp:
    #    json.dump(str(data), fp, indent=4)

# rules = {
#    "condense1":[],\
#    "growth1":[],"growth2":[],"growth3to4":[],"growth5":[],\
#    "reduction6":[],"reduction7":[],"reduction8to9":[],\
#    "subj_obj10":[],"subj_obj11":[],"subj_obj12":[],"subj_obj13":[]
# }

# if tree.growth1(tree.verb[i]):
#     #resultfile.write("growth1 used\n")
#     rules["growth1"].append(sentence_num)
# # this says to recurse but I haven't had a situation where I needed that
# # so I have that on file but it is not tested
# if tree.growth2_2(tree.verb[i]):
#     #resultfile.write("growth2 used\n")
#     rules["growth2"].append(sentence_num)
#
# if tree.growth3to4(tree.verb[i]):
#     #resultfile.write("growth3to4 used\n")
#     rules["growth3to4"].append(sentence_num)
#
# #this doesn't seem to be used so I don't know if this is right
# if tree.growth5(tree.verb[i]):
#     #resultfile.write("growth5 used\n")
#     rules["growth5"].append(sentence_num)
#
# if tree.reduction6(tree.verb[i]):
#     #resultfile.write("reduction6 used\n")
#     rules["reduction6"].append(sentence_num)
#
# if tree.reduction7(tree.verb[i]):
#     #resultfile.write("reduction7 used\n")
#     rules["reduction7"].append(sentence_num)
#
# if tree.reduction8to9(tree.verb[i]):
#     #resultfile.write("reduction8to9 used\n")
#     rules["reduction8to9"].append(sentence_num)
#
# if tree.subj_obj10(tree.verb[i]):
#     #resultfile.write("subj_obj10 used\n")
#     rules["subj_obj10"].append(sentence_num)
#
# if tree.subj_obj11(tree.verb[i]):
#     #resultfile.write("subj_obj11 used\n")
#     rules["subj_obj11"].append(sentence_num)
#
# if tree.subj_obj12(tree.verb[i]):
#     #resultfile.write("subj_obj12 used\n")
#     rules["subj_obj12"].append(sentence_num)
#
# if tree.subj_obj13(tree.verb[i]):
#     resultfile.write("subj_obj13 used\n")
#     rules["subj_obj13"].append(sentence_num)

# if aff.dep == "prep":
#     tree.growth1(aff)
#     tree.growth2_2(aff)
#     tree.growth3to4(aff)
#     tree.growth5(aff)
# tree.reduction6(aff)
# tree.reduction7(aff)
# tree.reduction8to9(aff)
# tree.subj_obj10(aff)
# tree.subj_obj11(aff)
# tree.subj_obj12(aff)
# tree.subj_obj13(aff)