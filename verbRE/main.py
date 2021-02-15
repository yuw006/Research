import spacy
from Tree import Tree, Node
nlp = spacy.load("en_core_web_lg")

#number of sentences
i = 19

#files
readfile = open("examples.txt","r")
# readfile format
# sentence number
# sentence
# verb
# relation/ comment

treefile = open("trees.txt","a")
resultfile = open("results.txt","a")

while i > 0:
    sentence_num = readfile.readline()

    if sentence_num == "":
        break

    # for reading from file
    sentence = readfile.readline().strip("\n")
    doc = nlp( sentence )
    verb = readfile.readline().strip("\n")

    #individual tests
    #sentence = "After the bell rang, the children came home from school."
    #doc = nlp(sentence)
    #verb = "rang"

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
        resultfile.write("no verb: " + verb + "in sentence " + sentence_num)


    else:

        #rules
        if tree.growth1(tree.verb):
            resultfile.write("growth1 used\n")

        # this says to recurse but I haven't had a situation where I needed that
        # so I have that on file but it is not tested
        if tree.growth2(tree.verb):
            resultfile.write("growth2 used\n")

        if tree.growth3to4(tree.verb):
            resultfile.write("growth3to4 used\n")

        #this doesn't seem to be used so I don't know if this is right
        if tree.growth5(tree.verb):
            resultfile.write("growth5 used\n")

        if tree.reduction6(tree.verb):
            resultfile.write("reduction6 used\n")

        if tree.reduction7(tree.verb):
            resultfile.write("reduction7 used\n")

        if tree.reduction8to9(tree.verb):
            resultfile.write("reduction8to9 used\n")

        if tree.subj_obj10(tree.verb):
            resultfile.write("subj_obj10 used\n")

        if tree.subj_obj11(tree.verb):
            resultfile.write("subj_obj11 used\n")

        if tree.subj_obj12(tree.verb):
            resultfile.write("subj_obj12 used\n")

        if tree.subj_obj13(tree.verb):
            resultfile.write("subj_obj13 used\n")

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