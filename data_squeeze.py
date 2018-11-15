input1 = "name.txt"
input2 = "ipa.txt"
outfile = "./combined.txt"

f1 = []
f2 = []

with open(input1) as f:
	for line in f:
		f1.append(line.strip())

with open(input2) as f:
	for line in f:
		f2.append(line.strip())

with open(outfile, 'w') as f:
	for i in range(len(f1)):
		if i >= len(f2): break
		f.write(f1[i] + ' ' + f2[i] + '\n')