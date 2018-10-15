# https://stackoverflow.com/questions/491085/how-can-i-pass-a-filename-as-a-parameter-into-my-module
import re
import sys



def count_paras():
	newlines = re.findall(r'(\n{2})+',contents)
	# print(len(newlines))
	return len(newlines)
def count_sentences():
	expression = re.compile(r'(\.|\?|\!|(\.\")|(\?\")|(\!\"))(\s)+((\W?)[A-Z]|$)')
	sentences = re.findall(expression,contents)
	special_exp = re.findall(r'((D|M|J|S)r\.)|(Ms.)',contents)
	# print(len(sentences)-len(special_exp))
	return len(sentences)-len(special_exp)
def count_words():
	expression = re.compile(r'((\d+\,\d+)|\w+(((\-|\.|\'|\")*?\w+)*))')
	words = re.findall(expression,contents)
	# print(words)
	# print(len(words))
	return len(words)
def count_word_start(word):
	temp = word
	first_char = (temp.capitalize())[0]
	word = word[1:len(word)]
	expression = re.compile(r'(^|(\.|\?|\!|\.\"|\?\"|\!\"|[)])\s+)(%c%s|\"%c%s)(\s)'%(first_char,word,first_char,word))
	words = re.findall(expression,contents)
	# print(len(words))
	return len(words)
def count_word_end(word):
	expression = re.compile(r'(\s)(%s)(\.|\?|\!|\.\"|\?\"|\!\")($|\s+[A-Z]?)'%(word),re.I)
	words = re.findall(expression,contents)
	# print(len(words))
	return len(words)
def count_word_anywhere(word):
	word.replace(".","")
	word.replace("-","")
	contents.replace(".","")
	contents.replace(",","")
	contents.replace(";","")
	contents.replace(":","")
	contents.replace("\'","")
	contents.replace("\"","")
	contents.replace("-","")
	contents.replace("(","")
	contents.replace(")","")
	contents.replace("{","")
	contents.replace("}","")
	expression = re.compile(r'(^|\s+|\")%s(\s+|$|\")'%(word),re.I)
	words = re.findall(expression,contents)
	return len(words)


file_name = sys.argv[1]
fp = open(file_name)
contents = fp.read()
contents_copy = contents
print(count_paras())
print(count_sentences())
print(count_words())
while(1):
	word = raw_input("enter word : ")
	print "end"
	print count_word_end(word)
	print "start" 
	print count_word_start(word)
	print "anywhere"
	print count_word_anywhere(word)