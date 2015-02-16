#!/usr/bin/python

# Parses a token for follow peeps from a newly created, single authentication.

import json

json_data=open("cred.txt").read()
data = json.loads(json_data)

def findToken():
	if data['note'] == "follow peeps":
		token = data['token']
		print token
	else:
		print 'There is an error in retrieving your token!'

findToken()