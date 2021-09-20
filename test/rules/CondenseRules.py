# Rules I came up with to find verb phrases

from objects.DependencyTree import *

# for phrases like check off
# TODO figure out a way to assign position value
# @param verb: Node of verb/verb-phrase
# @ret whether list of verbs in sentence has changed
def condense0(self, verb):
    (left, right) = verb.index
    for vc in verb.children:
        if vc.dep == "prt" and not (vc.children):
            verb.text = verb.text + " " + vc.text
            # new
            if vc.index[0] < left:
                left = vc.index[0]
            if vc.index[1] > right:
                right = vc.index[1]

            verb.children.remove(vc)
            verb.index = (left, right)
            del vc
            return True
            break
    return False


# for phrases like will be
# TODO figure out a way to assign position value
# @param verb: Node of verb/verb-phrase
# @ret whether list of verbs in sentence has changed
def condense1(self, verb):
    phrase = ""
    nodes_delete = []
    used = False

    (left, right) = verb.index
    for vc in verb.children:
        if (vc.dep == "aux" or vc.dep == "auxpass") and not (vc.children):
            phrase = phrase + vc.text + " "
            # new
            if vc.index[0] < left:
                left = vc.index[0]
            if vc.index[1] > right:
                right = vc.index[1]
            nodes_delete.append(vc)
            used = True
    verb.index = (left, right)

    while nodes_delete:
        verb.children.remove(nodes_delete[0])
        if nodes_delete[0] in self.verb:
            self.verb.remove(nodes_delete[0])
        del nodes_delete[0]

    verb.text = phrase + verb.text
    return used

# for multiple objects
# TODO figure out a way to assign position value
# @param verb: Node of verb/verb-phrase
# @xc: Node xcomp child of verb
# @ret whether list of verbs in sentence has changed
def condense2_1(self, verb, xc):
    (left, right) = verb.index
    if xc in self.verb:
        verb.affliation.append(xc)
        verb.text = verb.text + " ... " + xc.text
        #if xc.index[0] < left:
        #    left = xc.index[0]
        #if xc.index[1] > right:
        #    right = xc.index[1]
        #verb.index = (left, right)
        self.verb.remove(xc)
        return True
    return False

# verb aux verb
# TODO figure out a way to assign position value
# @param verb: Node of verb/verb-phrase
# @ret whether list of verbs in sentence has changed
def condense2(self, verb):
    used = False
    for child in verb.children:
        if child.dep == "xcomp":  # maybe adcvl

            # check for multiple objects
            for cc in verb.children:
                if cc.dep in objects:
                    used = condense2_1(self, verb, child)
                    return used

            # no multiple objects case
            for cc in child.children:
                verb.children.append(cc)
                cc.parent = verb

            (left, right) = verb.index
            verb.text = verb.text + " " + child.text
            # new
            if child.index[0] < left:
                left = child.index[0]
            if child.index[1] > right:
                right = child.index[1]
            verb.index = (left, right)

            verb.children.remove(child)
            child.parent = None

            if child in self.verb:
                self.verb.remove(child)

            del child
            used = True
            break

    return used


# TODO figure out copula might not this
# TODO figure out a way to assign position value
# @param verb: Node of verb/verb-phrase
# @ret whether list of verbs in sentence has changed
def condense3(self, verb):
    num_adv = 1
    (left, right) = verb.index
    for vc in verb.children:
        # if (vc.dep == "acomp" or vc.dep == "advmod") and not ( vc.pos_tag == "VERB" or vc.pos_tag == "AUX"):
        if (vc.dep == "acomp") and not (vc.pos_tag == "VERB" or vc.pos_tag == "AUX"):
            verb.text = verb.text + " " + vc.text
            if vc.index[0] < left:
                left = vc.index[0]
            if vc.index[1] > right:
                right = vc.index[1]
            verb.index = (left, right)
            for child in vc.children:
                verb.children.append(child)
                child.parent = verb
            verb.children.remove(vc)
            del vc
            return True
    return False


# for prepositions
# @param verb: Node of verb/verb-phrase
# @ret whether list of verbs in sentence has changed
def condense3_5(self, verb):
    num_adv = 1
    for vc in verb.children:
        if (vc.dep == "prep") and not (vc.pos_tag == "VERB" or vc.pos_tag == "AUX"):
            # verb.text = verb.text + " " + vc.text
            verb.affliation.append(vc)
            return True
    return False


# for conjuncted verbs
# TODO figure out a way to assign position value
# @param verb: Node of verb/verb-phrase
# @ret whether list of verbs in sentence has changed
def condense4(self, verb):
    (left, right) = verb.index
    if not self.has_obj(verb):
        for vc in verb.children:
            if vc.dep == "conj" and vc.pos_tag == "VERB":
                condense4(self,vc)
                neg = ""
                for child in vc.children:
                    if child.dep == "neg":
                        neg = child.text
                        break
                verb.text = verb.text + ", " + neg + " " + vc.text
                verb.coIndex.append(vc.index)
                # new
                # if vc.index[0] < left:
                #    left = vc.index[0]
                # if vc.index[1] > right:
                #     right = vc.index[1]
                # verb.index = (left, right)

                for child in vc.children:
                    verb.children.append(child)
                    child.parent = verb
                verb.children.remove(vc)
                self.verb.remove(vc)
                del vc
                break

