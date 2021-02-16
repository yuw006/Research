### The code is not complete so there will be updates
# verbRE
## main.py
 - reads inputs
 &nbsp;&nbsp;*examples.txt produced from extractVerb*\
 &nbsp;&nbsp;*typed sentence and verb*
 - applies rules
 - the output functions\
 &nbsp;&nbsp;*results.txt the sentence, verb, subj, obj, negation*
 
<details>
<summary>example</summary>
<pre>
In contrast to BlinkDB, SciBORQ does not support error constraints, and does not provide guarantees on the error margins for results.
growth2 used
reduction8to9 used

verb: provide

: subj:
subj
SciBORQ
subj
SciBORQ

: obj:
obj
guarantees
obj
guarantees
prep
on
pobj
margins
det compound prep
the error for
pobj
results

Negation: True
</pre>
</details>
 
 &nbsp;&nbsp;*stats.txt the rules and which sentences used the rules*\
 &nbsp;&nbsp;*trees.txt parse tree pre/post transformed* 
 
<details>
<summary>example</summary>
<pre>
53
In contrast to BlinkDB, SciBORQ does not support error constraints, and does not provide guarantees on the error margins for results.    verb: provide
initial Tree:
ROOT
support
ROOT
support
prep punct nsubj aux neg dobj punct cc conj punct
In , SciBORQ does not constraints , and provide .
pobj compound aux neg dobj
contrast error does not guarantees
prep prep
to on
pobj pobj
BlinkDB margins
det compound prep
the error for
pobj
results


transformed Tree:
ROOT
support
ROOT
support
prep punct aux neg dobj punct cc conj punct
In , does not constraints , and provide .
pobj compound subj obj neg aux
contrast error SciBORQ guarantees not does
prep prep
to on
pobj pobj
BlinkDB margins
det compound prep
the error for
pobj
results
</pre>
</details>
 
 - to output to a file, pass in the file path to traversal functions
## Tree.py
### Node Class:
- a node has: dependency( subj,obj etc ), parents, children, sentence/word, and tag( NOUN, VERB etc )\
### Tree Class:
- a tree has: root, verb(word to do relation extraction)
- travere funtions: There are 3 traverse functions that print out the tree to a file in the arguments
- transformations rules: There are 13 rules, some are applied together

# extractVerb
this takes in a file called "sentences.txt" that has a list of sentences\
outputs a file called "examples.txt" that follows the format:\
&nbsp;&nbsp;*sentence number*\
&nbsp;&nbsp;*sentence*\
&nbsp;&nbsp;*verb to perform RE on*\
&nbsp;&nbsp;*relation or some comment you might have space holder:[relation]*\
ps remember to add a newline at the end of the file

