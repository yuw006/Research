import spacy
readfile = open("sentences.txt","r")
writefile = open("examples.txt","a")
nlp = spacy.load("en_core_web_lg")
i = 0
while True:
    sentence = readfile.readline()
    if sentence == "":
        break
    doc = nlp(sentence)

    for token in doc:
        if token.pos_ == "VERB":
            writefile.write(str(i)+"\n")
            writefile.write(sentence)
            writefile.write(token.text+"\n")
            writefile.write("relation\n")
            i = i + 1

readfile.close()
writefile.close()



