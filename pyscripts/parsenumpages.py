#!/usr/bin/python

data=open("numpages.txt").read()

def findPages():
	numpages = 'There is a pagination error, please notify the developers : )'
	splitData = data.split('page=')
	for i in splitData:
		str(i)
		if 'rel="last"' in i:
			lines = str(i).splitlines()
			line = lines[0]
			splitLine = line.split('>')
			numpages = splitLine[0]
	print numpages

findPages()