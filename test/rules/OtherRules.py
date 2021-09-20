# rules given be tetre (modified)

from objects.DependencyTree import *

def growth1(self, verb):
    tags = ["NOUN", "PROPN", "VERB", "NUM", "PRON", "X"]

    # If the edge to the head node is of the type relcl or ccomp
    if verb.dep == "relcl" or verb.dep == "ccomp":
        has_subj_child = False
        # and the existing subj-like child node does not have the POS tag NOUN, /
        # PROPN, VERB, NUM, PRON, or X,
        for i, child in enumerate(verb.children):
            if child.dep in subjects:
                has_subj_child = True
                # reatches the node
                if not child.pos_tag in tags:
                    growth1_2(self, verb)
                    verb.children.remove(child)
                    # checking
                    return True
        # reataches the node
        if not has_subj_child:
            growth1_2(self, verb)
            # checking
            return True
    return False

# rearranges tree
def growth1_2(self, verb):
    node_head = verb.parent
    if verb.parent.parent:
        parent_parent = verb.parent.parent
        verb.parent = parent_parent
        parent_parent.children.append(verb)
        parent_parent.children.remove(node_head)
    else:
        verb.parent = None
        self.root = verb
        verb.dep = "root"
    node_head.children.remove(verb)

    verb.children.append(node_head)
    node_head.parent = verb
    node_head.dep = "subj"

############rule2#############
def is_ancestor_of(self, ancestor, descendant):
    node = descendant
    while node:
        if node == ancestor:
            return True
        node = node.parent
    return False

def growth2_recurse(self, node, verb):
    if not node:
        return None, None

    for i, child in enumerate(node.children):
        if (child.dep in subjects) and (not is_ancestor_of(self, child, verb)):
            return node, child
    # keep searching
    return growth2_recurse(self, node.parent, verb)

def growth2_2(self, verb):
    # If the current node is part of a conj relation through its head edge,
    if verb.dep == "conj":

        # and no subj-like child node exists
        has_subj_child = False
        for child in verb.children:
            if child.dep in subjects:
                has_subj_child = True

        # search for a subj-like child node in the parent (a sibling node)
        if not has_subj_child:
            node, subj = growth2_recurse(self, verb.parent, verb)
            if node:
                node.children.remove(subj)
                subj.parent = verb
                verb.children.append(subj)
                # checking
                return True
    return False

# This needs some debugging
# If no obj-like child node exists, transform nodes xcomp or/
# ccomp in a dobj. If no subj-like child node exists, transform nodes xcomp/
# or ccomp in a nsubj.
# If no obj-like child node exists, transform prep relation/
# whose preposition word is ‘in’ in a dobj node.
def growth3to4(self, verb):
    hasObjChild = False
    for child in verb.children:
        if child.dep in objects:
            hasObjChild = True
            break

    hasSubjChild = False
    for child in verb.children:
        if child.dep in subjects:
            hasSubjChild = True
            break

    returnVal = False
    if not hasObjChild:
        for child in verb.children:
            if child.dep == "ccomp" or child.dep == "xcomp":
                child.dep = "dobj"
                returnVal = True
            # if child.dep == "prep" and (child.text == "in"): # edit this
            #    child.dep = "dobj"
            #    returnVal = True

    if not hasSubjChild:
        for child in verb.children:
            if child.dep == "ccomp" or child.dep == "xcomp":
                child.dep = "nsubj"
                returnVal = True

    return returnVal

# This needs some debugging
# If no obj-like child edge exists, a subj-like child edge exists, and the head edge is of the subj-like type, move the head node as to be
# its dobj-like child.
def growth5(self, verb):
    hasObjChild = False
    for child in verb.children:
        if child.dep in objects:
            hasObjChild = True
            break
    hasSubjChild = False
    for child in verb.children:
        if child.dep in subjects:
            hasSubjChild = True
            break
    if (not hasObjChild) and hasSubjChild and (verb.dep in subjects):

        node = verb.parent
        verb.children.append(node)
        node.dep = "dobj"
        verb.parent = node.parent
        node.parent = verb
        node.children.remove(verb)
        if not (node == self.root):
            verb.parent.children.remove(node)
            verb.parent.children.append(verb)
        else:
            self.root == verb
        # checking
        return True
    return False

# TODO figure out a way to assign position value
# this needs some debugging
# For any two child with same incoming edge type, remove the duplicate edge.
def reduction6(self, verb):
    returnVal = False
    for child in verb.children:
        # print(child.dep)
        if not (child.dep == "prep" or child.pos_tag == "VERB"):
            edge_types[child.dep].append(child)

    verb.children = []
    # new
    (left, right) = (999,-1)
    for e in edge_types:
        if len(edge_types[e]) > 1:
            returnVal = True
            text = ""
            for node in edge_types[e]:
                text = text + " " + node.text
                # new
                if node.index[0] < left:
                    left = node.index[0]
                if node.index[1] > right:
                    right = node.index[1]
                del node
            new_node = Node(verb, e, text, "NONE",(left, right)) # TODO: change this
            verb.children.append(new_node)
        elif len(edge_types[e]) > 0:
            verb.children.append(edge_types[e][0])
        edge_types[e] = []
    print(returnVal)
    return returnVal

# Remove tags of type punct, mark, '', meta
# TODO This is done is a format where the node is the removed and the parent take on the children of the removed node
def reduction7(self, verb):
    returnVal = False
    tags = ["punct", "mark", "", "meta"]
    for child in verb.children:
        if child.dep in tags:
            returnVal = True
            for c in child.children:
                verb.children.append(c)
                c.parent = verb
            verb.children.remove(child)
            del child
    return returnVal

# transform all obj-like relations into obj/
# all subj-like relations into subj/
# and all mod-like relations into mod.
# Merge all obj-like relations into one single obj node,
# and all subj-like relations into one subj node.
# this seems to include rule12
# TODO figure out a way to assign position value
def reduction8to9(self, verb):
    returnVal = False
    obj_nodes = []
    subj_nodes = []
    text = ""
    children = []

    for child in verb.children:

        if child.dep in objects:
            obj_nodes.append(child)
            child.dep = "obj"
            returnVal = True

        elif child.dep in subjects:
            subj_nodes.append(child)
            child.dep = "subj"
            returnVal = True

        # setting tags of mods to general one
        elif child.dep in mods:
            returnVal = True
            child.dep = "mod"

    # new
    (left, right) = (888,-1)
    # merging obj nodes to general one
    if (len(obj_nodes) > 1):
        for o in obj_nodes:
            text = text + " " + o.text
            # new
            if o.index[0] < left:
                left = o.index[0]
            if o.index[1] > right:
                right = o.index[1]

            for c in o.children:
                children.append(c)
            verb.children.remove(o)
            o.parent = None
            del o
        new_node = Node(verb, "obj", text, "NONE", (left, right)) # TODO: change this
        verb.children.append(new_node)

        for c in children:
            new_node.children.append(c)
            c.parent = new_node

        text = ""
        children = []

    # merging subj nodes to general one
    left, right = 777, -1
    if (len(subj_nodes) > 1):
        returnVal = True
        for s in subj_nodes:
            text = text + " " + s.text
            # new
            if s.index[0] < left:
                left = s.index[0]
            if s.index[1] > right:
                right = s.index[1]

            for c in s.children:
                children.append(c)
            verb.children.remove(s)
            s.parent = None
            del s
        new_node = Node(verb, "subj", text, "NONE", (left, right))
        verb.children.append(new_node)

        for c in children:
            new_node.children.append(c)
            c.parent = new_node

    return returnVal

# for any two child with same type of incoming edge remove the duplicate
# TODO figure out a way to assign position value
def subj_obj10(self, verb):
    returnVal = False

    for n in verb.children:
        if n.dep == "obj" or n.dep == "subj":
            for child in n.children:
                edge_types[child.dep].append(child)

            n.children = []
            (left, right) = (666, -1)
            for e in edge_types:
                if len(edge_types[e]) > 1:
                    returnVal = True
                    text = ""
                    for i in edge_types[e]:
                        text = text + " " + i.text
                        # new
                        if i.index[0] < left:
                            left = i.index[0]
                        if i.index[1] > right:
                            right = i.index[1]

                        del i
                    new_node = Node(n, e, text, "NONE", (left,right))
                    n.children.append(new_node)
                elif len(edge_types[e]) > 0:
                    n.children.append(edge_types[e][0])
                edge_types[e] = []

    return returnVal

# TODO finish this
# remove tags of det and " "
def subj_obj11(self, verb):
    returnVal = False
    tags = ["det", ""]
    for n in verb.children:
        if n.dep == "obj" or n.dep == "subj":
            for child in n.children:
                # keep no to check for negation
                if (child.dep == "det" and not (child.text == "no" or child.text == "No")) or child.dep == "":
                    returnVal = True
                    # if child.dep in tags:
                    for c in child.children:
                        n.children.append(c)
                        c.parent = n
                    n.children.remove(child)
                    del child
    return returnVal

def subj_obj12(self, verb):
    returnVal = False
    for n in verb.children:
        if n.dep == "obj" or n.dep == "subj":
            for child in n.children:
                if child.dep in objects:
                    child.dep = "obj"
                    returnVal = True
                elif child.dep in subjects:
                    child.dep = "subj"
                    returnVal = True
                # setting tags of mods to general one
                elif child.dep in mods:
                    child.dep = "mod"
                    returnVal = True
    return returnVal

# TODO check this
def subj_obj13(self, verb):
    returnVal = False
    tags = ["relcl", "acl", "advcl"]
    tokens = ["by", "to", "for", "with", "whereby"]
    for n in verb.children:
        if n.dep == "obj" or n.dep == "subj":
            for child in n.children:
                if child.dep in tags or (child.dep == "prep" and child.text in tokens):
                    n.children.remove(child)
                    verb.children.append(child)
                    child.parent = verb
                    returnVal = True
    return returnVal