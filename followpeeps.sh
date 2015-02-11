#!/bin/bash
#This script will automatically follow all of the users in a given Github organization (if you have access). 
# Note: this only works if 2-Factor authorization is disabled.
 
#1
#get username for authentication
echo -n "Enter your Github username and press [ENTER]: "
read name
 
#2
#authenticate user with necesarry permissions
token=$(curl -Ss -u $name -d '{"scopes": ["user", "read:org"], "note": "follow peeeeps"}' https://api.github.com/authorizations) | grep -Po '(?<="token": ")[^"]*'

#4 
#find members of given github organization
echo -n "Enter the Github organization whose peeps you would like to follow and press [ENTER]: "
read org
curl -Ss 'Authorization: token $token' -X GET https://api.github.com/orgs/$org/members > members.txt
 
#5
#need to parse data from GET request for user logins and store in variable <users> here
#!/usr/bin/env python
ARRAY="$(python parselogins.py)"
#will need to stick the output of this pyscript into the ARRAY variable as a list of users separated by a single space (no commas, quotes, etc.)...
 
 
#6
#follow all users
for i in ${ARRAY[@]};
  do 
    #for testing, use echo i, when complete, make actual put requests
    echo $i
 	#curl -i -H 'Authorization: token <token>' -X PUT https://api.github.com/user/following/$i;
 	sleep .01
  done

#7
#clean up
rm ./members.txtt