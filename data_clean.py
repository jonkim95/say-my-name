input_f = "ipa.txt"
outfile = "./no_c.txt"

f1 = []
f2 = []

with open(input_f) as f:
	for line in f:
		new_line = ''
		seen_c = False
		for ch in line.strip():
			if not seen_c:
				if ch == 'c':
					seen_c = True
				else:
					new_line += ch
			else:
				seen_c = False
		f1.append(new_line)

with open(outfile, 'w') as f:
	for i in range(len(f1)):
		#if i >= len(f2): break
		f.write(f1[i] + '\n')