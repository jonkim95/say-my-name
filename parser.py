# -*- coding: utf-8 -*-
import re
import csv

name_titles = []

with open('file_names.csv', 'rb') as f:
	reader = csv.reader(f)
	for row in reader:
		name_titles.append(str(row[0]))

# ipa_string = r"(\w+) \(.+\[(.+)\].+\)"
# ipa_string = r"(\w+) \(.*\[(.+)\].*\)"
ipa_string = r"(\S+)(\s+|,\s+)\(.*\[(.+)\].*\)"
ipa_string2 = r"(\S+)(\s+|,\s+)\[(.+)\]"

def process_ipa(name, summary):
	m = re.search(ipa_string, summary)
	if m is not None:
		name = m.group(1)
		ipa = m.group(3)
		# print name, '\n'
		# print summary, '\n'
		return name, ipa
	
	m = re.search(ipa_string2, summary)
	if m is not None:
		name = m.group(1)
		ipa = m.group(3)
		return name, ipa



i = 0
start = True
j = 0

with open('summary2.csv', 'rb') as f:
	reader = csv.reader(f)
	for row in reader:
		if len(row) == 0:
			start = True
		elif start:
			summary = row[0]
			name = name_titles[i]
			a = process_ipa(name, summary)
			if a is None:
				j += 1
			else:
				print name, len(name.split(' '))
				print a[0], len(a[0].split(' '))
				print a[1], len(a[1].split(' '))
				print '\n'
				with open('final.csv', 'a') as g:
					if name == a[0]:
						writer = csv.writer(g)
						writer.writerow([name, a[1]])
					elif len(a[1].split(' ')) == len(name.split(' ')):
						writer = csv.writer(g)
						writer.writerow([name, a[1]])
					elif len(a[1].split(' ')) == len(a[0].split(' ')):
						writer = csv.writer(g)
						writer.writerow([a[0], a[1]])
				
			start = False
			i += 1

print j, " Nones"
