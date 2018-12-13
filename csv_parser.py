# -*- coding: utf-8 -*-
import csv 
read_file = "ipa.csv"
names = []
with open(read_file, 'rb') as f:
	csv_reader = csv.reader(f)
	for row in csv_reader:
		names.append(row[-1])

with open('name_titles.csv', 'wb') as f:
	for name in names:
		if ':' in name:
			continue
		if len(name) == 1:
			continue
		writer = csv.writer(f)
		writer.writerow([name])

