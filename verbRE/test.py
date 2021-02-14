import spacy
#old version
# subj-like
subjects = ["nsubj", "nsubjpass", "csubj", "csubjpass", "agent", "expl"]
objects = ["dobj", "dative", "attr", "oprd"]
mods = ["nummod", "amod", "nmod", "advmod", "npmod"]
edge_types = {"nsubj": [], "nsubjpass": [], "csubj": [], "csubjpass": [], "agent": [], "expl": [], \
              "dobj": [], "dative": [], "attr": [], "oprd": [], \
              "ccomp": [], "xcomp": [], "acomp": [], \
              "appos": [], "acl": [], "relcl": [], "det": [], "predet": [], "nummod": [], "amod": [], "poss": [],
              "nmod": [], \
              "advmod": [], "advcl": [], "neg": [], "npmod": [], "pobj": [], "pcomp": [], \
              "conj": [], "cc": [], "preconj": [], "prep": [], \
              "aux": [], "auxpass": [], "compound": [], "prt": [], "case": [], "mark": [], \
              "det": [], "meta": [], "paratxis": [], "punct": [], "root": [], \
              "mod": [], "obj": [], "subj": []}


class Node:

    # parent -dep-> node(text,pos_tag) ->children
    def __init__(self, parent, dep, text, pos_tag):
        self.parent = parent
        self.dep = dep
        self.text = text
        self.pos_tag = pos_tag
        self.children = []


class Tree:

    # parent -child.dep-> child
    def __init__(self, root, text):
        self.root = root
        self.verb = None
        self.verb_text = text

    # create a copy of the dep tree
    def createTree(self, node, copy):
        if node.text == self.verb_text:
            self.verb = copy
        for child in node.children:
            new_node = Node(copy, child.dep_, child.text, child.pos_)
            copy.children.append(new_node)
            self.createTree(child, new_node)

    # Tree traversals

    # traverses the tree
    def levelTraversal(self):
        frontier = [self.root]
        print(self.root.dep)
        print(self.root.text)
        while frontier:
            print(' '.join(node.dep for node in frontier))
            print(' '.join(node.text for node in frontier))
            # print(' '.join(node.pos_tag for node in frontier))
            next_level = list()
            for n in frontier:
                for child in n.children:
                    next_level.append(child)
            frontier = next_level

    # traverses the tree
    def levelTraversal2(self):
        frontier = []
        for n in self.verb.children:
            if n.dep == "obj":
                frontier.append(n)
                print(n.dep)
                print(n.text)
        while frontier:
            print(' '.join(node.dep for node in frontier))
            print(' '.join(node.text for node in frontier))
            # print(' '.join(node.pos_tag for node in frontier))
            next_level = list()
            for n in frontier:
                for child in n.children:
                    next_level.append(child)
            frontier = next_level

    def levelTraversal3(self):
        frontier = []
        for n in self.verb.children:
            if n.dep == "subj":
                frontier.append(n)
                print(n.dep)
                print(n.text)
        while frontier:
            print(' '.join(node.dep for node in frontier))
            print(' '.join(node.text for node in frontier))
            # print(' '.join(node.pos_tag for node in frontier))
            next_level = list()
            for n in frontier:
                for child in n.children:
                    next_level.append(child)
            frontier = next_level

    # end of tree traversals

    def growth1(self, verb):
        tags = ["NOUN", "PROPN", "VERB", "NUM", "PRON", "X"]

        # If the edge to the head node is of the type relcl or ccomp
        if (verb.dep == "relcl" or verb.dep == "ccomp"):
            hasSubjChild = False

            # and the existing subj-like child node does not have the POS tag NOUN, /
            # PROPN, VERB, NUM, PRON, or X,
            for i, child in enumerate(verb.children):
                if (child.dep in subjects):
                    hasSubjChild = True
                    sub_child = None
                    # reatches the node
                    if (not child.pos_tag in tags):
                        node = verb.parent.parent
                        node_head = verb.parent

                        verb.parent = node
                        node.children.append(verb)
                        node_head.children.remove(verb)

                        node.children.remove(node_head)
                        verb.children.remove(child)

                        verb.children.append(node_head)
                        node_head.parent = verb
                        node_head.dep = child.dep

            # reataches the node
            if not hasSubjChild:
                node = verb.parent.parent
                node_head = verb.parent

                verb.parent = node
                node.children.append(verb)
                node_head.children.remove(verb)

                node.children.remove(node_head)

                verb.children.append(node_head)
                node_head.parent = verb
                node_head.dep = "nsubj"

    # TODO recurse debug
    def growth2(self, verb):
        # If the current node is part of a conj relation through its head edge,
        if verb.dep == "conj":

            # and no subj-like child node exists
            hasSubjChild = False
            for i, child in enumerate(verb.children):
                if (child.dep in subjects):
                    hasSubjChild = True

            # search for a subj-like child node in the parent (a sibling node)
            if not hasSubjChild:
                node = verb.parent
                for child in node.children:
                    if child.dep in subjects:
                        node.children.remove(child)
                        child.parent = verb
                        verb.children.append(child)

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

        if not hasObjChild:
            for child in verb.children:
                if child.dep == "ccomp" or child.dep == "xcomp":
                    child.dep = "dobj"
                if child.dep == "prep" and child.text == "in":
                    child.dep = "dobj"

        if not hasSubjChild:
            for child in verb.children:
                if child.dep == "ccomp" or child.dep == "xcomp":
                    child.dep = "nsubj"

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

    # this needs some debugging
    # For any two child with same incoming edge type, remove the duplicate edge.
    def reduction6(self, verb):
        for child in verb.children:
            print(child.dep)
            edge_types[child.dep].append(child)

        verb.children = []
        for e in edge_types:
            if len(edge_types[e]) > 1:
                text = ""
                for i in edge_types[e]:
                    text = text + i.text
                    del i
                new_node = Node(verb, e, text, "NONE")
                verb.children.append(new_node)
            elif len(edge_types[e]) > 0:
                verb.children.append(edge_types[e][0])
            edge_types[e] = []

    # Remove tags of type punct, mark, '', meta
    # TODO This is done is a format where the node is the removed and the parent take on the children of the removed node
    def reduction7(self, verb):
        tags = ["punct", "mark", " ", "meta"]
        for child in verb.children:
            if child.dep in tags:
                for c in child.children:
                    verb.children.append(c)
                    c.parent = verb
                verb.children.remove(child)
                del child

    # transform all obj-like relations into obj/
    # all subj-like relations into subj/
    # and all mod-like relations into mod.
    # Merge all obj-like relations into one single obj node,
    # and all subj-like relations into one subj node.
    # this seems to include rule12
    def reduction8to9(self, verb):
        obj_nodes = []
        subj_nodes = []
        text = ""
        children = []
        for child in verb.children:
            if child.dep in objects:
                obj_nodes.append(child)
                child.dep = "obj"
                # verb.children.remove(child)
            elif child.dep in subjects:
                subj_nodes.append(child)
                child.dep = "subj"
                # verb.children.remove(child)

            # setting tags of mods to general one
            elif child.dep in mods:
                child.dep = "mod"

        # merging obj nodes to general one
        if (len(obj_nodes) > 1):
            for o in obj_nodes:
                text = text + " " + o.text
                for c in o.children:
                    children.append(c)
                verb.children.remove(o)
                del o
            new_node = Node(verb, "obj", text, "NONE")
            verb.children.append(new_node)

            for c in children:
                new_node.children.append(c)

            text = ""
            children = []

        # merging subj nodes to general one
        if (len(subj_nodes) > 1):
            for s in subj_nodes:
                text = text + " " + s.text
                for c in s.children:
                    children.append(c)
                verb.children.remove(o)
                del s
            new_node = Node(verb, "subj", text, "NONE")
            verb.children.append(new_node)
            for c in children:
                new_node.children.append(c)

    # for any two child with same type of incoming edge remove the duplicate
    def subj_obj10(self, verb):
        for n in verb.children:
            if n.dep == "obj" or n.dep == "subj":
                for child in n.children:
                    edge_types[child.dep].append(child)

                n.children = []
                for e in edge_types:
                    if len(edge_types[e]) > 1:
                        text = ""
                        for i in edge_types[e]:
                            text = text + " " + i.text
                            del i
                        new_node = Node(n, e, text, "NONE")
                        n.children.append(new_node)
                    elif len(edge_types[e]) > 0:
                        n.children.append(edge_types[e][0])
                    edge_types[e] = []

    # TODO finish this
    # remove tags of det and " "
    def subj_obj11(self, verb):
        tags = ["det", " "]
        for n in verb.children:
            if n.dep == "obj" or n.dep == "subj":
                for child in n.children:
                    if child.dep in tags:
                        for c in child.children:
                            n.children.append(c)
                            c.parent = n
                        n.children.remove(child)
                        del child

    def subj_obj12(self, verb):
        for n in verb.children:
            if n.dep == "obj" or n.dep == "subj":
                for child in n.children:
                    if child.dep in objects:
                        child.dep = "obj"
                    elif child.dep in subjects:
                        child.deo = "subj"
                    # setting tags of mods to general one
                    elif child.dep in mods:
                        child.dep = "mod"

    # TODO check this
    def subj_obj13(self, verb):
        tags = ["relcl", "acl", "advcl"]
        tokens = ["by", "to", "for", "with", "whereby"]
        for n in verb.children:
            if n.dep == "obj" or n.dep == "subj":
                for child in n.children:
                    if child.dep in tags or (child.dep == "prep" and child.text in tokens):
                        n.children.remove(child)
                        verb.children.append(child)
                        child.parent = verb

    def growth2(self, verb):
        # If the current node is part of a conj relation through its head edge,
        if verb.dep == "conj":

            # and no subj-like child node exists
            hasSubjChild = False
            for i, child in enumerate(verb.children):
                if (child.dep in subjects):
                    hasSubjChild = True

            # search for a subj-like child node in the parent (a sibling node)
            if not hasSubjChild:
                node = self.growth2_recurse(self, verb.parent)
                for child in node.children:
                    if child.dep in subjects:
                        node.children.remove(child)
                        child.parent = verb
                        verb.children.append(child)
                        # checking
                        return True
        return False

    def growth2_recurse(self, node):
        if node == None:
            return None
        hasSubjChild = False
        for i, child in enumerate(verb.children):
            if (child.dep in subjects):
                hasSubjChild = True
                return node
        if not hasSubjChild:
            self.growth2_recurse(node.parent)