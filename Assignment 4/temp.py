# file1 = open("/home/mypc/Desktop/7th Sem/NLP/Assignments/Ass4/Training set_HMM.txt",'r')
# data = file1.readlines()
# print data
# train_data = []
# for line in data:
# 	line = line.strip()
# 	line = line.split()
# 	if(line==[]):
# 		train_data.append("")
# 	else:
# 		train_data.append(line[0])

# open("/home/mypc/Desktop/7th Sem/NLP/Assignments/Ass4/Testing_set_HMM.txt", 'w').close()
# file2 = open("/home/mypc/Desktop/7th Sem/NLP/Assignments/Ass4/Testing_set_HMM.txt",'a')

# for i in range(len(train_data)):
# 	file2.write(train_data[i]+"\n")

file1 = open("/home/mypc/Desktop/7th Sem/NLP/Assignments/Ass4/Training set_HMM.txt",'r')
file2 = open("/home/mypc/Desktop/7th Sem/NLP/Assignments/Ass4/output.txt",'r')

Training = file1.readlines()
Testing = file2.readlines()

test = []
train = []
for line in Training:
	line = line.strip()
	line = line.split()
	if(line!=[]):
		train.append(line[1])
for line in Testing:
	line = line.strip()
	line = line.split()
	if(line!=[]):
		test.append(line[1])

same = 0
for i in range(len(test)):
	print(train[i]+" "+test[i]+"\n")
	if(test[i]==train[i]):
		same+=1
print("training accuracy :")
print((float(same)*100)/len(test))