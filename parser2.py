import csv

i = []
o = []

with open('final/final_for_sure.csv', 'rb') as f:
	reader = csv.reader(f)
	for row in reader:
		i.append(row[0])
		o.append(row[1])

with open('input.csv', 'wb') as f:
	writer = csv.writer(f, delimiter='\n')
	writer.writerow(i)

with open('output.csv', 'wb') as f:
	writer = csv.writer(f, delimiter='\n')
	writer.writerow(o)