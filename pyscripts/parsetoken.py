#!/usr/bin/python

# Parses a token for follow peeps from list of authentications.

import json
import unicodedata

json_data=open("cred.txt").read()
data = json.loads(json_data)

def findToken():
	for x in data:
		if x['note'] == "follow peeps":
			token = x['token']
			print token

findToken()