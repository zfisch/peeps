from getpass import getpass
from urlparse import urljoin
import urllib2, base64, json, unicodedata
import requests

class GitHubConnection(object):
  GIT_API = "https://api.github.com"

  def __init__(self, username, password, org):
    s = requests.Session()
    s.auth = (username, password)
    self.default_request = s
    self.token = ''
    # s.headers.update({'Accept': 'application/vnd.github.v3+json'})
    self.org = org

      # Start by deleting any previous peeps authorizations b/c github no longer allows retrieval of tokens from pre-existing authorizations
    self.delete_existing_authorization()

  def make_git_api_call(self, string, params, http_verb):
    request_string = urljoin(self.GIT_API, string)
    r = getattr(self.default_request, http_verb)(request_string, data=json.dumps(params))
    return r.json()

  def create_authorization(self):
    params = {"note": "peeps", "scopes": ["user", "read:org"]}
    credentials = self.make_git_api_call('authorizations', params, 'post')
    self.token = credentials['token']
    self.get_members_of_org(self.org)

  def delete_existing_authorization(self):
    old_peeps_id = ''
    existing_authorizations = self.make_git_api_call('authorizations', '', 'get')
    for auth in existing_authorizations:
      if auth['note'] == "peeps":
        old_peeps_id = str(auth['id'])
    request_string = 'authorizations/' + old_peeps_id
    if old_peeps_id:
      self.make_git_api_call(request_string, '', 'delete')

    # after pre-existing auth is deleted, a new one can be made
    self.create_authorization()

  def get_members_of_org(self, organization):
    params = {'Accept': 'application/vnd.github.ironman-preview+json'}
    api_endpoint = '/orgs/' + organization + '/members'
    members = self.make_git_api_call(api_endpoint, params, 'get')
    print members


def main():
  username = raw_input("Enter your github username: ")
  password = getpass("Enter your github password: ")
  org = raw_input("Enter the name of the organization whose members you would like to follow: ")

  conn = GitHubConnection(username, password, org)

if __name__ == "__main__":
    main()

