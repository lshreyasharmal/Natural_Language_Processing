import random
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
import os
from sklearn.datasets import fetch_20newsgroups
from os import listdir
from os.path import isfile, join
import re
import numpy as np


def build_model():
  
    vec_size = 100
    alpha = 0.025
    window=10
    min_count=5 
    workers=11
    corpus = fetch_20newsgroups(remove=('headers', 'footers', 'quotes'))
    documents = [TaggedDocument((re.sub('[^\w\s]','',corpus.data[i]).lower()).split(), [corpus.target[i]]) for i in range(corpus.filenames.shape[0])]
    model = Doc2Vec(size=vec_size, alpha=alpha, min_alpha=0.00025, min_count=min_count, dm =1,workers=workers,iter=100,window=10)
    model.build_vocab(documents)
    model.train(documents,total_examples=model.corpus_count, epochs=model.iter)
    model.save("d2v.model")
    print("Model Saved")


def get_similarity_score(test_doc,target_doc):
    tokens1 = word_tokenize(test_doc.lower())
    new_vector = model.infer_vector(tokens1,steps=50, alpha=0.25)
    tokens2 = word_tokenize(target_doc.lower())
    target_vector = model.infer_vector(tokens2,steps=50, alpha=0.25)
    from sklearn.metrics.pairwise import cosine_similarity

    return cosine_similarity([new_vector],[target_vector])


folders = []
for (root,dirs,files) in os.walk('.', topdown=False):
    if(len(dirs) > 2):
        folders = dirs
    

#build_model()



model= Doc2Vec.load("d2v.model")


corpus = fetch_20newsgroups(categories=['comp.graphics'], remove=('headers', 'footers', 'quotes'))
Target_Doc = corpus.data[20]


scores_with_same_class = []
for i in range(19):
    doc = corpus.data[i]
    score = get_similarity_score(doc,Target_Doc)
    scores_with_same_class.append([i,float(score[0])])
    

scores_with_other_classes = []
for fol in folders:
    if(fol=='comp.graphics'):
        continue
    corpus = fetch_20newsgroups(categories=[fol], remove=('headers', 'footers', 'quotes'))
    doc1 = corpus.data[0]
    score = get_similarity_score(doc1,Target_Doc)
    scores_with_other_classes.append([fol,float(score[0])])

    
print(scores_with_same_class)
print(scores_with_other_classes)
print("Score of comp.graphics with files of other classes:")
for x in scores_with_other_classes:
    print(x[0] + " : " + str(x[1]))
sc1 = np.array([x[1] for x in scores_with_other_classes])
print(np.mean(sc1))
print("Score of comp.graphics with files of same class:")
for x in scores_with_same_class:
    print(str(x[0]) + " : " + str(x[1]))
sc2 = np.array([x[1] for x in scores_with_same_class])
print(np.mean(sc2))
