#!/usr/bin/python

import json
import unicodedata

json_data=open("members.txt").read()
data = json.loads(json_data)

def findLogins():
	string = ""
	for x in data:
		loginName = unicodedata.normalize("NFKD", x["login"]).encode('ascii', 'ignore')
		string += loginName + ' '
	print string


findLogins()


