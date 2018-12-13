# -*- coding: utf-8 -*-
import requests
import wikipedia
import re
import csv

name_titles = []

with open('name_titles2.csv', 'rb') as f:
	reader = csv.reader(f)
	for row in reader:
		if row[0] != 'page_title':
			name_titles.append(str(row[0]))

ipa_string = r"(\w+) \(.+\[(.+)\].+\)"

def process_page(page_name):
	try:
		summary = wikipedia.WikipediaPage(title = page_name).summary
		return page_name, summary
	except:
		print page_name
		return None

	m = re.search(ipa_string, summary)
	if m is not None:
		name = m.group(1)
		ipa = m.group(2)

		if len(ipa.split()) == len(page_name.split()):
			return page_name, ipa
		else: 
			return name, ipa

i = 0
for title in name_titles:
	if process_page(title) is not None:
		name, summary = process_page(title)
		print name, summary, i
		with open('file_names.csv', 'a') as f:
			writer = csv.writer(f)
			if name:
				try:
					writer.writerow([name])
				except:
					writer.writerow([''])
			else: 
				writer.writerow([''])
		with open('summary2.csv', 'a') as f:
			writer = csv.writer(f)
			if summary:
				try:
					writer.writerow([summary.encode('utf-8')])
					writer.writerow('')
				except:
					writer.writerow(['None'])
			else: 
				writer.writerow(['None'])
		i += 1

with open('names_and_summary.csv', 'wb') as f:
	for name in names:
		writer = csv.writer(f)
		writer.writerow([name, summary])
