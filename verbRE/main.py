import spacy
from Tree import Tree, Node
nlp = spacy.load("en_core_web_lg")
i = 19
#readfile
rf = open("examples.txt","r")
tf = open("trees.txt","a")
f = open("results.txt","a")
while i == 19:#i > 0:
    sentence = rf.readline()
    if sentence == "":
        break
    #doc = nlp( rf.readline().strip("\n"))
    doc = nlp("After the bell rang, the children came home from school.")
    verbPhrase = rf.readline()
    #verbPhrase = verbPhrase.strip("\n")
    verbPhrase = "rang"
    tree = None
    root = None
    root2 = None
    num = 0

    for token in doc:
        if token.dep_ == "ROOT":
            root = Node(None, token.dep_, token.text, token.pos_)
            root2 = token
            tree = Tree(root,verbPhrase)
            tree.createTree(token,root)


#frontier=[root2]
#print(root2.dep_)
#print(root2.text)
#while frontier:
#    print(' '.join(node.dep_ for node in frontier))
#    print(' '.join(node.text for node in frontier))
#    #print(' '.join(node.pos_tag for node in frontier))
#    next_level = list()
#   for n in frontier:
#        for child in n.children:
#            next_level.append(child)
#    frontier = next_level
#print("***********************")
    tf.write(sentence)
    tree.levelTraversal(tf)

    f.write(sentence)
    if( tree.verb == None):
        f.write("no verb: " + verbPhrase + "in sentence " + sentence)


    else:
        if tree.growth1(tree.verb):
            #print 1
            f.write("growth1 used")
        if tree.growth2(tree.verb):
            #print 2
            f.write("growth2 used")
        tree.growth3to4(tree.verb)
        if tree.growth5(tree.verb):
            #print 5
            f.write("growth5 used")
        f.write("\n")
        tree.reduction6(tree.verb)
        tree.reduction7(tree.verb)
        tree.reduction8to9(tree.verb)
        tree.subj_obj10(tree.verb)
        tree.subj_obj11(tree.verb)
        tree.subj_obj12(tree.verb)
        tree.subj_obj13(tree.verb)

        tree.levelTraversal(tf)
        f.write("verb: " + verbPhrase)
        f.write("\n")
        tree.levelTraversal3(f)
        tree.levelTraversal2(f)
    del tree
    rf.readline()
    i = i - 1
rf.close()
f.close()
tf.close()