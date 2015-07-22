from getpass import getpass
from urlparse import urljoin
import urllib2, base64, json, unicodedata

class GitHubConnection(object):
  GIT_API = "https://api.github.com"

  def __init__(self, username, password, done_before):
    # PasswordMgr doesn't work, see http://stackoverflow.com/questions/2407126/python-urllib2-basic-auth-problem
    self.base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
    self.get_credentials()

  def make_git_api_call(self, string):
    request_string = urljoin(self.GIT_API, string)
    request = urllib2.Request(request_string)
    request.add_header("Authorization", "Basic %s" % self.base64string)
    try: return urllib2.urlopen(request)
    except urllib2.URLError as e:
      print e.reason

  def get_credentials(self):
    self.credentials = self.make_git_api_call("authorizations")
    find_token(self.credentials)


  def find_token(self, credentials):
    data = json.loads(open(credentials).read())
      for x in data:
        if x['note'] == "follow peeps":
          self.token = x['token']
        else:
          make_credentials(self)

def main():
  username = raw_input("Enter your github username: ")
  password = getpass("Enter your github password: ")
  run_before = ""

  while run_before not in ["y", "n"]:
    run_before = raw_input("Have you run this before? (y/n): ").lower()

  conn = GitHubConnection(username, password, run_before == "y")

if __name__ == "__main__":
    main()

