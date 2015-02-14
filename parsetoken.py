#!/usr/bin/python

import json
import unicodedata

json_data=open("cred.txt").read()
data = json.loads(json_data)

def findToken():
	token = data['token']
	print token


findToken()


