import numpy as np
import math
def viterbi(transition_probs,emission_probs,initial_probs,tag_count,output_sequence,words):
	T = len(tag_count)
	W = len(words)

	test_sequence = []
	for line in output_sequence:
		line = line.strip()
		if(line!=""):
			test_sequence.append(line)
	print(test_sequence)
	N = len(test_sequence)
	V = []
	
	initial_sum = sum(initial_probs.values())

	tags = tag_count.keys()

	for i in range(N):
		tmp = []
		for t in range(T):
			tmp.append(0)
		V.append(tmp)


	for k in range(T):

		tag = tags[k]
		init_prob = 0
		emission_prob = 0
		if(tag not in initial_probs.keys()):
			init_prob = -1*math.log(initial_sum)
		else:
			init_prob = math.log(initial_probs[tag])-math.log(initial_sum)
		# if test_sequence[0] not in emission_probs[tag].keys():	
		# 	emission_prob = -1*math.log(tag_count[tag])
		# else:
		emission_prob = math.log(emission_probs[tag][test_sequence[0]])-math.log(tag_count[tag])
		V[0][k]=init_prob+emission_prob

	for i in range(1,N):
		for t in range(T):
			for t_ in range(T):
				trans_prob = 0
				if(tags[t] in transition_probs[tags[t_]].keys()):
					trans_prob = math.log(transition_probs[tags[t_]][tags[t]])- math.log(len(transition_probs[tags[t_]]))
				# else:
				# 	trans_prob = -1*math.log(len(transition_probs[tags[t_]]))
				tmp = V[i-1][t_] + trans_prob
				if(tmp>V[i][t]):
					V[i][t]=tmp
			emission_prob = 0

			if(test_sequence[i] in emission_probs[tags[t]].keys()):
				emission_prob = math.log(emission_probs[tags[t]][test_sequence[i]])-math.log(tag_count[tags[t]])
			# else:
			# 	emission_prob = -1*math.log(tag_count[tags[t]])
			V[i][t] += emission_prob

	path = []
	V = np.array(V)
	path.append(np.argmax(V[N-1]))
	for n in range(N-2,-1,-1):
		x = 0
		path.append(0)
		for t in range(T):
			if(tags[path[N-n-2]] in transition_probs[tags[t]].keys()):
				tmp = V[n][t]+math.log(transition_probs[tags[t]][tags[path[N-n-2]]])-math.log(len(transition_probs[tags[t]]))
			else:
				tmp = V[n][t]-math.log(len(transition_probs[tags[t]]))
			if(tmp >x):
				x=tmp
				path[N-n-1]=t
			
	path = np.array(path)
	path = path[::-1]

	return(tags,path,test_sequence)
