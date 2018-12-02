import spacy
nlp = spacy.load('en_core_web_md')


def lemmatize(token):
    return token.lemma_
def pos_tag(token):
    return token.tag_
def NMR(doc):
    return [(X.text, X.label_) for X in doc.ents]
def get_similarity_score(token1,token2):
    token1 = nlp(token1)
    token2 = nlp(token2)
    return float(token1.similarity(token2))

def sentence_doc_process(doc):
    print("------------------------------------------------")
    print("Lemmatized Sentence:")
    lemmatized_sentence = ""
    for token in doc:
        lemmatized_sentence += lemmatize(token)+" "
    print(lemmatized_sentence)
        
    print("------------------------------------------------")
    print("POS-Tagged Sentence:")
    pos_sentence = ""
    for token in doc:
        pos_sentence += pos_tag(token)+" "
    print(pos_sentence)
    
    print("------------------------------------------------")
    print("Named entity Recognition:")
    print(NMR(doc))



while(True):
    print("###################################################")
    c = int(input("Enter 1: For sentence, 2: document, 3: words and any other key to exit :\n"))
    print("------------------------------------------------")
    if(c==1):
        sentence = input("Please enter a sentence:\n")
        doc = nlp(sentence)
        sentence_doc_process(doc)
        
    elif(c==2):
        path = input("Enter path of the file\n")
        doc = nlp(open(path,'r').read())
        sentence_doc_process(doc)  
        
    elif(c==3):
        words = input("Enter 2 words, space separated:\n")
        print("Similarity Score between the words: "+ str(get_similarity_score(words[0],words[1])))
        print("")
    else:
        break