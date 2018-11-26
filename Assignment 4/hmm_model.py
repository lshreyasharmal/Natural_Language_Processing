transition_probs = {}
emission_probs = {}
initial_probs = {}
tag_count = {}
words = []
def train_(filename):
	file = open(filename,'r')
	data = file.readlines()
	# print(data)
	prev = ['.','.']
	for line in data:
		line = line.strip()
		line = line.split()

		if(line == []):
			continue
		if(line[0] not in words):
			words.append(line[0])
		if(line[1] not in tag_count.keys()):
			tag_count[line[1]]=1
		else:
			tag_count[line[1]]+=1

		if(prev == ['.','.']):
			if line[1] not in initial_probs.keys():
				initial_probs[line[1]] = 1
			else:
				initial_probs[line[1]]+=1


		if(line[1] not in emission_probs.keys()):
			emission_probs[line[1]] = {}
			emission_probs[line[1]][line[0]]=1
		elif line[0] not in emission_probs[line[1]].keys():
			emission_probs[line[1]][line[0]]=1
		else:
			emission_probs[line[1]][line[0]]+=1


		if(prev[1] not in transition_probs.keys()):
			transition_probs[prev[1]]={}
			transition_probs[prev[1]][line[1]]=1
		elif line[1] not in transition_probs[prev[1]].keys():
			transition_probs[prev[1]][line[1]]=1
		else:
			transition_probs[prev[1]][line[1]]+=1

		prev = line
	# print("")
	# print(transition_probs)
	# print("")
	# print(emission_probs)
	# print("")
	# print(initial_probs)
	# print("")
	# print(tag_count)
	return(transition_probs,emission_probs,initial_probs,tag_count,words)