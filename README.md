# orgy
Follow all users in a github organization from the command line.

Download the files and run from command line. You'll need to comment out the echo command in #6 and uncomment the curl command if you'd like it to work. This is in place to provide a preliminary test to make sure it's working before you get blocked from github for making a bunch of bad requests ;)

Known Issue: There is a pagination limit for github http requests that needs to be resolved. Currently it will only send 30 logins, and then stop. See here: https://developer.github.com/guides/traversing-with-pagination/. Fix in progress.


Note: You'll need a github account with two-factor auth disabled, membership to the organization whose peeps you'd like to follow, python, and potentially a few other things I haven't realized yet.




Work in progress! Please feel free to make a pull request and suggest updates : )
