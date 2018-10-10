import glob
import os
import nltk
import pickle
from math import log
import time
import operator
start_time = time.time()
import re, string, unicodedata
import contractions
import random
import inflect
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.tokenize.punkt import PunktSentenceTokenizer
from collections import Counter
from random import randint
import re

path = "C:\Users\MyPC\Desktop\Ass3\Ass3/"

def create_sentence_tokens(class_num):
	if(class_num == 1):
		os.chdir("C:\Users\MyPC\Desktop\Ass3\Ass3/20_newsgroups/comp.graphics/")
	else:
		os.chdir("C:\Users\MyPC\Desktop\Ass3\Ass3/20_newsgroups/rec.motorcycles/")
	all_sentence_tokens = []
	for file in glob.glob("*"):
		f = open(file, 'rb')
		sentences = PunktSentenceTokenizer().tokenize(f.read())
		all_sentence_tokens += sentences
		f.close()
	return all_sentence_tokens

def create_word_tokens(all_sentence_tokens):
	corpus = []
	for sentence in all_sentence_tokens:
		temp = []
		words = nltk.word_tokenize(sentence)
		for word in words:
			word = re.sub(r'\W+', '', word)
			word = re.sub(r'_+', '', word)
			if(word!=''):
				temp.append(word.lower())
		if(len(temp)!=0):
			corpus.append(temp)
	return corpus

def create_unigrams(class_num):
	unigram_frequencies = {}
	corpus = []
	if(class_num==1):
		corpus = corpus1
	else:
		corpus = corpus2

	unigram_frequencies[""]=0
	for sentence in corpus:
		unigram_frequencies[""] +=1
		for word in sentence:
			if(word in unigram_frequencies.keys()):
				unigram_frequencies[word]+=1
			else:
				unigram_frequencies[word]=1
	if(class_num==1):
		with open(path+"unigram_frequencies_1.txt", "wb") as myFile:
			pickle.dump(unigram_frequencies,myFile)
	else:
		with open(path+"unigram_frequencies_2.txt", "wb") as myFile:
			pickle.dump(unigram_frequencies,myFile)
	return unigram_frequencies

def create_bigrams(class_num):
	unigram_frequencies = {}
	corpus = []
	if(class_num==1):
		unigram_frequencies = unigram_frequencies_1
		corpus = corpus1
	else:
		unigram_frequencies = unigram_frequencies_2
		corpus = corpus2

	bigram_probabilities_smoothed = {}

	for sentence in corpus:
		prev = ""
		for word in sentence:
			if(prev in bigram_probabilities_smoothed.keys()):
				if word in bigram_probabilities_smoothed[prev].keys():
					bigram_probabilities_smoothed[prev][word] += 1
				else:
					bigram_probabilities_smoothed[prev][word] = 2
			else:
				bigram_probabilities_smoothed[prev] = {}
				bigram_probabilities_smoothed[prev][word] = 2
			prev = word

	V = len(unigram_frequencies)
	for first_word in bigram_probabilities_smoothed.keys():
		denominator = V + unigram_frequencies[first_word]
		for second_word in bigram_probabilities_smoothed[first_word].keys():
			bigram_probabilities_smoothed[first_word][second_word] = bigram_probabilities_smoothed[first_word][second_word]*1.0/denominator

	if(class_num==1):
		with open(path+"bigram_probs_smoothed_1.txt", "wb") as myFile:
			pickle.dump(bigram_probabilities_smoothed,myFile)
	else:
		with open(path+"bigram_probs_smoothed_2.txt", "wb") as myFile:
			pickle.dump(bigram_probabilities_smoothed,myFile)
	return bigram_probabilities_smoothed

def preprocess(doc):
	sentences = PunktSentenceTokenizer().tokenize(doc)
	corpus = []
	for sentence in sentences:
		temp = []
		words = nltk.word_tokenize(sentence)
		for word in words:
			word = re.sub(r'\W+', '', word)
			word = re.sub(r'_+', '', word)
			if(word!=''):
				temp.append(word.lower())
		if(len(temp)!=0):
			corpus.append(temp)
	return corpus

def predict(doc):

	doc = preprocess(doc)
	p1 = 0
	p2 = 0
	for sentence in doc:
		prev = ""
		for word in sentence:
			if(prev in bigram_probs_1.keys()):
				if(word in bigram_probs_1[prev].keys()):
					p1 += log(bigram_probs_1[prev][word])
				else:
					denominator = len(unigram_freqs_1) + unigram_freqs_1[prev]
					p1 += log(1.0/denominator)
			elif prev in unigram_freqs_1.keys():
				denominator = len(unigram_freqs_1) + unigram_freqs_1[prev]
				p1 += log(1.0/denominator)
			else:
				denominator = len(unigram_freqs_1) + total_words1
				p1 += log(1.0/denominator)

			if(prev in bigram_probs_2.keys()):
				if(word in bigram_probs_2[prev].keys()):
					p2 += log(bigram_probs_2[prev][word])
				else:
					denominator = len(unigram_freqs_2) + unigram_freqs_2[prev]
					p2 += log(1.0/denominator)
			elif prev in unigram_freqs_2.keys():
				denominator = len(unigram_freqs_2) + unigram_freqs_2[prev]
				p2 += log(1.0/denominator)
			else:
				denominator = len(unigram_freqs_2) + total_words2
				p2 += log(1.0/denominator)
			prev = word
	print p1 
	print p2
	if p1>=p2:
		return 1
	return 2



#already pickled
# all_sentence_tokens1 = create_sentence_tokens(1)
# corpus1 = create_word_tokens(all_sentence_tokens1)
# unigram_frequencies_1 = create_unigrams(1)
# bigram_probabilities_smoothed_1 = create_bigrams(1)
# all_sentence_tokens2 = create_sentence_tokens(2)
# corpus2 = create_word_tokens(all_sentence_tokens2)
# unigram_frequencies_2 = create_unigrams(2)
# bigram_probabilities_smoothed_2 = create_bigrams(2)

bigram_probs_1 = {}
bigram_probs_2 = {}
unigram_freqs_1 = {}
unigram_freqs_2 = {}
with open(path+"unigram_frequencies_1.txt", "rb") as myFile:
	unigram_freqs_1=pickle.load(myFile)
with open(path+"unigram_frequencies_2.txt", "rb") as myFile:
	unigram_freqs_2=pickle.load(myFile)
with open(path+"bigram_probs_smoothed_1.txt", "rb") as myFile:
	bigram_probs_1=pickle.load(myFile)
with open(path+"bigram_probs_smoothed_2.txt", "rb") as myFile:
	bigram_probs_2=pickle.load(myFile)
total_words1 = 0
total_words2 = 0
for word in unigram_freqs_1.keys():
	total_words1 += unigram_freqs_1[word]
for word in unigram_freqs_2.keys():
	total_words2 += unigram_freqs_2[word]

while(True):
	n = int(raw_input("choose 1 for sentence input and 2 for document path input: "))
	if(n==1):
		ipsentence = raw_input("enter a sentence: ")
		print predict(ipsentence)
	else:
		path = raw_input("enter path name: ")
		file = raw_input("enter file name :")
		os.chdir("C:\Users\MyPC\Desktop\Ass3\Ass3/20_newsgroups/comp.graphics/")
		f = open(file,'rb')
		doc = f.read()
		print predict(doc)


print("--- %s seconds ---" % (time.time() - start_time))