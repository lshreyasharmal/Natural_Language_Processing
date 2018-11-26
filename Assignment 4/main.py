from hmm_model import train_
from test import viterbi
import pickle 

path = r"C:\\Users\\MyPC\\Desktop\\2015096_Assignment4HMM\\Ass4\\"

# transition_probs,emission_probs,initial_probs,tag_count,words = train_("/home/mypc/Desktop/7th Sem/NLP/Assignments/Ass4/Training set_HMM.txt")
# with open(path+"transition_probs.txt", "wb") as myFile:
# 		pickle.dump(transition_probs, myFile)
# with open(path+"emission_probs.txt", "wb") as myFile:
# 		pickle.dump(emission_probs, myFile)
# with open(path+"initial_probs.txt", "wb") as myFile:
# 		pickle.dump(initial_probs, myFile)
# with open(path+"tag_count.txt", "wb") as myFile:
# 		pickle.dump(tag_count, myFile)
# with open(path+"words.txt", "wb") as myFile:
# 		pickle.dump(words, myFile)

transition_probs = {}
emission_probs = {}
initial_probs = {}
tag_count = {}
words = []
with open(path+"transition_probs.txt", "rb") as myFile:
	transition_probs = pickle.load(myFile)
with open(path+"emission_probs.txt", "rb") as myFile:
	emission_probs = pickle.load(myFile)
with open(path+"initial_probs.txt", "rb") as myFile:
	initial_probs = pickle.load(myFile)
with open(path+"tag_count.txt", "rb") as myFile:
	tag_count = pickle.load(myFile)	
with open(path+"words.txt", "rb") as myFile:
	words = pickle.load(myFile)		

filename = path + "Testing_set_HMM.txt"
file = open(filename,'r')
output_sequence = file.readlines()
print(output_sequence)

tags,path,test_sequence = viterbi(transition_probs,emission_probs,initial_probs,tag_count,output_sequence,words)

open(r"C:\\Users\\MyPC\\Desktop\\2015096_Assignment4HMM\\Ass4\\output.txt", 'w').close()
file = open(r"C:\\Users\\MyPC\\Desktop\\2015096_Assignment4HMM\\Ass4\\output.txt",'a')
for i in range(len(path)):
	sentence = test_sequence[i]+"\t"+tags[path[i]]+"\n"
	if(test_sequence[i]=='.'):
		sentence+='\n'
	file.write(sentence)