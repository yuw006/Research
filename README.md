### The code is not complete so there will be updates
# verbRE
## main.py
 this is the main function:
 - reads inputs
 - applies rules
 - the output functions are commented out
 - to output to a file, pass in the file path to traversal functions (in Tree.py)
## Tree.py
 Node Class:
- a node has: dependency( subj,obj etc ), parents, children, sentence/word, and tag( NOUN, VERB etc )\
Tree Class:
- a tree has: root, verb(word to do relation extraction)
- travere funtions: There are 3 traverse functions that print out the tree to a file in the arguments
- transformations rules: There are 13 rules, some are applied together
