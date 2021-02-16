import spacy
from Tree import Tree, Node
nlp = spacy.load("en_core_web_lg")

#number of sentences
i = 1

#files
readfile = open("examples.txt","r")
# readfile format
# sentence number
# sentence
# verb
# relation/ comment
statfile = open("stats.txt","a")
treefile = open("trees.txt","a")
resultfile = open("results.txt","a")
rules = {
    "growth1":[],"growth2":[],"growth3to4":[],"growth5":[],\
    "reduction6":[],"reduction7":[],"reduction8to9":[],\
    "subj_obj10":[],"subj_obj11":[],"subj_obj12":[],"subj_obj13":[]
}
while i > 0:
    sentence_num = readfile.readline()

    if sentence_num == "":
        break

    # for reading from file
    #sentence = readfile.readline().strip("\n")
    #doc = nlp( sentence )
    #verb = readfile.readline().strip("\n")

    #individual tests
    sentence = "Japan may be a tough market for outsiders to penetrate, and the U.S. is hopelessly behind Japan in certain technologies."
    doc = nlp(sentence)
    verb = "is"

    tree = None
    root = None
    #root2 = None
    num = 0

    #initializes tree
    for token in doc:
        if token.dep_ == "ROOT":
            root = Node(None, token.dep_, token.text, token.pos_)
            #root2 = token
            tree = Tree(root, verb)
            tree.createTree(token, root)


    #writes intital tree to tree file
    treefile.write(sentence_num + sentence+"    verb: " + verb +"\ninitial Tree:\n")
    tree.levelTraversal(treefile)
    treefile.write("\n")

    #writes to results file
    resultfile.write(sentence_num + sentence + "\n")

    #occasionally the tree isn't completely built so this catches it
    if( tree.verb == None):
        resultfile.write("no verb: " + verb + " in sentence " + sentence_num)


    else:

        #rules
        if tree.growth1(tree.verb):
            resultfile.write("growth1 used\n")
            rules["growth1"].append(sentence_num)
        # this says to recurse but I haven't had a situation where I needed that
        # so I have that on file but it is not tested
        if tree.growth2(tree.verb):
            resultfile.write("growth2 used\n")
            rules["growth2"].append(sentence_num)

        if tree.growth3to4(tree.verb):
            resultfile.write("growth3to4 used\n")
            rules["growth3to4"].append(sentence_num)

        #this doesn't seem to be used so I don't know if this is right
        if tree.growth5(tree.verb):
            resultfile.write("growth5 used\n")
            rules["growth5"].append(sentence_num)

        if tree.reduction6(tree.verb):
            resultfile.write("reduction6 used\n")
            rules["reduction6"].append(sentence_num)

        if tree.reduction7(tree.verb):
            resultfile.write("reduction7 used\n")
            rules["reduction7"].append(sentence_num)

        if tree.reduction8to9(tree.verb):
            resultfile.write("reduction8to9 used\n")
            rules["reduction8to9"].append(sentence_num)

        if tree.subj_obj10(tree.verb):
            resultfile.write("subj_obj10 used\n")
            rules["subj_obj10"].append(sentence_num)

        if tree.subj_obj11(tree.verb):
            resultfile.write("subj_obj11 used\n")
            rules["subj_obj11"].append(sentence_num)

        if tree.subj_obj12(tree.verb):
            resultfile.write("subj_obj12 used\n")
            rules["subj_obj12"].append(sentence_num)

        if tree.subj_obj13(tree.verb):
            resultfile.write("subj_obj13 used\n")
            rules["subj_obj13"].append(sentence_num)

        #check for negation
        negation = tree.check_negation(tree.verb)

        # print to file

        # prints transformed tree
        treefile.write("\ntransformed Tree:\n")
        tree.levelTraversal(treefile)
        treefile.write("\n")

        # prints results
        resultfile.write("\nverb: " + verb + "\n")
        resultfile.write("\n: subj:\n")
        tree.levelTraversal3(resultfile)
        resultfile.write("\n: obj:\n")
        tree.levelTraversal2(resultfile)
        resultfile.write("\nNegation: " + str(negation) + "\n")



    del tree
    readfile.readline()
    i = i - 1

readfile.close()
resultfile.close()
treefile.close()

for key in rules:
    statfile.write(key + "\n")
    for i in rules[key]:
        statfile.write(i + "\n")

statfile.close()
