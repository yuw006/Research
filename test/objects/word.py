# Word Class contain token attributes
class Word:
    def __init__(self, token_index, token_text, sentence_id, document_id, head_text, dependency, entity_type, upos, x_pos, token_vec, pos): #, start_char, end_char):
        self.token_index = token_index
        self.token_text = token_text
        self.sentence_id = sentence_id
        self.document_id = document_id
        self.head_text = head_text
        self.dependency = dependency
        self.entity_type = entity_type
        self.upos = upos
        self.xpos = x_pos
        self.embedding = list(token_vec)
        self.pos = [0,0,0]
        self.pos_= pos
        # self.start_char = start_char
        # self.end_char = end_char

class Verb:
    def __init__(self):
        self.type = "normal"
        self.spans = []
# class Sentence:
#    def __init__(self):
#        self.sentence = []
#    def appendWord(self, word):
#        self.sentence.append(word)