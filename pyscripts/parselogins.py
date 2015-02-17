#!/usr/bin/python

import re

data=open("members.txt").read()

def findLogins():
	users = data.split('login')
	logins = []
	for user in users:
		str(user)
		loginLine = user.splitlines()[0]
		login = re.sub(r'[^a-zA-Z0-9\-]', '', loginLine)
		logins.append(login)
	logins.pop(0)
	bashArray = ' '.join(logins)
	print bashArray

findLogins()