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
# nltk.download('punkt')
path = "C:\Users\MyPC\Desktop\Ass3\Ass3/"
def create_sentence_tokens():
	print("creating sentence tokens...")
	os.chdir("C:\Users\MyPC\Desktop\Ass3\Ass3/20_newsgroups/rec.motorcycles/")
	all_sentence_tokens = []
	for file in glob.glob("*"):
		f = open(file, 'rb')
		sentences = PunktSentenceTokenizer().tokenize(f.read())
		all_sentence_tokens += sentences
		f.close()
	return all_sentence_tokens

def create_word_tokens():
	print("creating word tokens...")
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


def find_probs_unigram():
	print("calculating frequencies(Unigram)...")
	probs_uni = {}
	total_count = 0
	probs_uni[""]=0
	for sentences in corpus:
		probs_uni[""]+=1
		for words in sentences:	
			probs_uni[words]=probs_uni[words]+1 if words in probs_uni.keys() else 1
			total_count += 1
	with open(path+"unigram_freqs_2.txt", "wb") as myFile:
		pickle.dump(probs_uni, myFile)
	print("calculating probabilties(Unigram)...")
	for word,val in probs_uni.iteritems():
		prob = float(val)/total_count
		probs_uni[word] = prob
	with open(path+"unigram_probs_2.txt", "wb") as myFile:
		pickle.dump(probs_uni, myFile)

	
def find_freqs_bigram():
	print("calculating frequencies(Bigram)...")
	freqs_bi = {}
	for sentences in corpus:
		for i in range(0,len(sentences)):
			if(i==0 and "" not in freqs_bi.keys()):
				freqs_bi[""] = {}
				freqs_bi[""][sentences[i]] = 1
			elif(i==0 and sentences[i] not in freqs_bi[""].keys()):
				freqs_bi[""][sentences[i]] = 1
			elif(i==0 and sentences[i] in freqs_bi[""].keys()):
				freqs_bi[''][sentences[i]] +=1


			if(sentences[i] not in freqs_bi.keys()):
				if(i!=len(sentences)-1):
					freqs_bi[sentences[i]] = {}
					freqs_bi[sentences[i]][sentences[i+1]] = 1
			else:
				if(i!=len(sentences)-1):
					if(sentences[i+1] in freqs_bi[sentences[i]].keys()):
						freqs_bi[sentences[i]][sentences[i+1]] += 1
					else:
						freqs_bi[sentences[i]][sentences[i+1]] = 1
	with open(path+"bigram_freqs_2.txt", "wb") as myFile:
		pickle.dump(freqs_bi, myFile)


def find_freqs_trigram():
	print("calculating frequencies(Trigram)...")
	freqs_tri = {}
	for sentences in corpus:
		if(len(sentences)>=2):
			pair = "" + " " +sentences[0]
			if(pair in freqs_tri.keys()):
				if(sentences[1] in freqs_tri[pair].keys()):
					freqs_tri[pair][sentences[1]] += 1
				else:
					freqs_tri[pair][sentences[1]] = 1
			else:
				freqs_tri[pair] = {}
				freqs_tri[pair][sentences[1]] = 1

		for i in range(2,len(sentences)):
			pair = sentences[i-2] + " " + sentences[i-1]
			if(pair in freqs_tri.keys()):
				if(sentences[i] in freqs_tri[pair].keys()):
					freqs_tri[pair][sentences[i]] += 1
				else:
					freqs_tri[pair][sentences[i]] = 1
			else:
				freqs_tri[pair] = {}
				freqs_tri[pair][sentences[i]] = 1
	with open(path+"trigram_freqs_2.txt", "wb") as myFile:
		pickle.dump(freqs_tri, myFile)


def get_probs_bi():
	print("calculating probabilties(Bigram)")
	freqs_bi = {}
	freqs_uni = {}
	total_count = 0
	with open(path+"bigram_freqs_2.txt",'rb') as myFile:
		freqs_bi = pickle.load(myFile)
	with open(path+"unigram_freqs_2.txt",'rb') as myFile:
		freqs_uni = pickle.load(myFile)
	for key,val_list in freqs_bi.iteritems():
		for word,val in val_list.iteritems():
			total_count += val
	# print total_count
	for key,val_list in freqs_bi.iteritems():
		for word,val in val_list.iteritems():
			freqs_bi[key][word] = (float(val)/total_count)
			freqs_bi[key][word] /= float(freqs_uni[key])
	with open(path+"bigram_probs_2.txt", "wb") as myFile:
		pickle.dump(freqs_bi, myFile)


def get_probs_tri():
	print("calculating probabilties(Trigram)")
	freqs_tri = {}
	freqs_bi = {}
	total_count = 0
	with open(path+"trigram_freqs_2.txt",'rb') as myFile:
		freqs_tri = pickle.load(myFile)
	with open(path+"bigram_freqs_2.txt",'rb') as myFile:
		freqs_bi = pickle.load(myFile)
	for key,val_list in freqs_tri.iteritems():
		for word,val in val_list.iteritems():
			total_count += val
	for key,val_list in freqs_tri.iteritems():
		for word,val in val_list.iteritems():
			freqs_tri[key][word] = (float(val)/total_count)
			ws = key.split()
			f1=""
			f2=""
			if(len(ws)==1):
				f1 = ""
				f2 = ws[0]
			else:
				f1 = ws[0]
				f2 = ws[1]
			freqs_tri[key][word] /= float(freqs_bi[f1][f2])

	with open(path+"trigram_probs_2.txt", "wb") as myFile:
		pickle.dump(freqs_tri, myFile)


def generate_unigram_sentence(length):
	
	sentence = ""
	r = random.randint(1,5)
	i = 1
	k = 0
	for key, value in sorted(probs_uni.iteritems(), key=lambda (k,v): (v,k), reverse=True):
		if(i==r):
			sentence += key
			k+=1
			if(k==length):
				return sentence + "."
			sentence+=" "
		else:
			i+=1

def generate_bigram_sentence(length,sentence=""):
	sentence = ""
	prev = ""
	curr_length = 0
	while(True):
		next_word = ""
		if(prev not in probs_bi.keys()):
			prev = generate_bigram_sentence(1).replace(".","")
		k = min(len(probs_bi[prev]),5)
		r = random.randint(1,k)
		i = 0
		for key,value in sorted(probs_bi[prev].iteritems(),key=lambda (k,v):(v,k), reverse= True):
			next_word = key
			i+=1
			if(i==r):	
				break
		sentence += next_word
		curr_length +=1
		prev = next_word
		if(curr_length==length):
			sentence+="."
			return sentence
		sentence+=" "

def generate_trigram_sentence(length):

	sentence = generate_bigram_sentence(1).replace(".","") + ' '

	prev = ""+ " " + sentence.split()[0]
	curr_length = 1
	if(length==1):
		sentence = sentence.replace(" ","") + "."
		return sentence
	while(True):
		# print sentence
		next_word = ""
		while(prev not in probs_tri.keys()):
			temp = prev.split()[1]
			temp += " " + generate_bigram_sentence(1,temp).replace(".","")
			prev = temp

		k = min(len(probs_tri[prev]),5)
		r = random.randint(1,k)
		i = 0
		for key,value in sorted(probs_tri[prev].iteritems(),key=lambda (k,v):(v,k), reverse= True):
			next_word = key
			i+=1
			if(i==r):	
				break
		sentence += next_word
		curr_length +=1
		# print prev
		prev = prev + " " + next_word
		prev = prev.split()[-2] + " " +prev.split()[-1]
		if(curr_length==length):
			sentence+="."
			return sentence
		sentence+=" "




all_sentence_tokens = create_sentence_tokens()
corpus = create_word_tokens()

find_probs_unigram()

find_freqs_bigram()
get_probs_bi()

find_freqs_trigram()
get_probs_tri()

probs_uni = {}
with open(path+"unigram_probs_2.txt", "rb") as myFile:
	probs_uni = pickle.load(myFile)
probs_bi = {}
with open(path+"bigram_probs_2.txt", "rb") as myFile:
	probs_bi = pickle.load(myFile)
probs_tri = {}
with open(path+"trigram_probs_2.txt", "rb") as myFile:
	probs_tri = pickle.load(myFile)
	
while(True):
	n = input("Enter length of sentence you want: ")
	print
	if(n>0):
		print "unigram sentence:"
		print generate_unigram_sentence(n)
		print
		print "bigram sentences:"
		print generate_bigram_sentence(n)
		print generate_bigram_sentence(n)
		print
		print "trigram sentences:"
		print generate_trigram_sentence(n)
		print generate_trigram_sentence(n)
		print
	else:
		print "n should be greater than 0"


print("--- %s seconds ---" % (time.time() - start_time))