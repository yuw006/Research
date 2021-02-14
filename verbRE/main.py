import spacy
from Tree import Tree, Node
nlp = spacy.load("en_core_web_lg")
i = 19
#I commented out all the files to read and write to you can add in your own, or if it's too messy I can do that
#rf = open("examples.txt","r")
#tf = open("trees.txt","a")
#f = open("results.txt","a")
while i == 19:#i > 0:
    sentence = rf.readline()
    if sentence == "":
        break
    #this is the sentence to parse
    doc = nlp("After the bell rang, the children came home from school.")
    verbPhrase = rf.readline()
    #this is the verb to search with
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

    tf.write(sentence)
    tree.levelTraversal(tf)

    f.write(sentence)
    if( tree.verb == None):
        f.write("no verb: " + verbPhrase + "in sentence " + sentence)


    else:
        if tree.growth1(tree.verb):
            #this is for testing feel free to disable
            #f.write("growth1 used")
            pass
        if tree.growth2(tree.verb):
            #this is for testing feel free to disable
            #f.write("growth2 used")
            pass
        tree.growth3to4(tree.verb)
        if tree.growth5(tree.verb):
            #this is for testing feel free to disable
            #f.write("growth5 used")
            pass
        
        #f.write("\n")
        tree.reduction6(tree.verb)
        tree.reduction7(tree.verb)
        tree.reduction8to9(tree.verb)
        tree.subj_obj10(tree.verb)
        tree.subj_obj11(tree.verb)
        tree.subj_obj12(tree.verb)
        tree.subj_obj13(tree.verb)

        #tree.levelTraversal(tf)
        #f.write("verb: " + verbPhrase)
        #f.write("\n")
        #tree.levelTraversal3(f)
        #tree.levelTraversal2(f)
    del tree
    #rf.readline()
    i = i - 1
#rf.close()
#f.close()
#tf.close()
