string1 = raw_input()
string2 = raw_input()

n = len(string1)
m = len(string2)

dp = []

for i in range(0,n+1):
	row = []
	for j in range(0,m+1):
		row.append(0)
	dp.append(row)

for i in range(0,n+1):
	dp[i][0]=i
for j in range(0,m+1):
	dp[0][j]=j

for i in range(1,n+1):
	for j in range(1,m+1):
		if string1[i-1] == string2[j-1]:
			dp[i][j] = dp[i-1][j-1]
		else:
			dp[i][j] = min(dp[i-1][j]+1,dp[i][j-1]+1,dp[i-1][j-1]+2)

minimum_edit_distane =  dp[n][m]
print ""
print "Cost = " + str(minimum_edit_distane)



i = n
j = m



alignment = []

while(i!=0 or j!=0):

	temp = []
		
	if i>=0 and j>=0 and dp[i][j]==dp[i-1][j-1] and string1[i-1]==string2[j-1]:
		temp.append(string1[i-1])
		temp.append(string2[j-1])
		temp.append("No Change")
		i = i-1
		j = j-1
	elif dp[i][j]==dp[i-1][j-1]+2:
		temp.append(string1[i-1])
		temp.append(string2[j-1])
		temp.append("Substitution")
		i = i-1
		j = j-1
	elif dp[i][j] == dp[i-1][j]+1 and i>=0:
		temp.append(string1[i-1])
		temp.append("*")
		temp.append("Deletion")
		i = i-1
	elif dp[i][j] == dp[i][j-1]+1 and j>=0:
		temp.append("*")
		temp.append(string2[j-1])
		temp.append("Insertion")
		j = j-1

	alignment.append(temp)


print ""
print "Alignment:"
for one in reversed(alignment):
	print one[0] + " " + one[1] + " " + one[2]
print ""