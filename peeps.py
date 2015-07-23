from getpass import getpass
from urlparse import urljoin
import json
import requests

class GitHubConnection(object):

  def __init__(self, username, password, org):
    default_req = requests.Session()
    default_req.auth = (username, password)
    # Custom Accept header suggested by GitHub, see: https://developer.github.com/v3/media/#request-specific-version
    default_req.headers.update({'Accept': 'application/vnd.github.v3+json'})
    self.default_request = default_req
    self.token = ''
    self.org = org

    # Start by deleting any previous peeps authorizations b/c github doest not allow retrieval of tokens from pre-existing authorizations
    self.delete_existing_authorization()

  def make_github_api_call(self, request_string, params, http_verb):
    return getattr(self.default_request, http_verb)(request_string, data=json.dumps(params))

  def create_authorization(self):
    params = {"note": "followpeepsscriptv2", "scopes": ["user", "read:org"]}
    credentials = self.make_github_api_call('https://api.github.com/authorizations', params, 'post').json()
    self.token = credentials['token']
    self.get_members_of_org(self.org)

  def delete_existing_authorization(self):
    # deletes an existing authorization for peeps if it exists
    old_peeps_id = None
    existing_authorizations = self.make_github_api_call('https://api.github.com/authorizations', '', 'get').json()
    if existing_authorizations:
      for auth in existing_authorizations:
        if auth['note'] == "followpeepsscriptv2":
          old_peeps_id = str(auth['id'])
          request_string = 'https://api.github.com/authorizations/' + old_peeps_id
          self.make_github_api_call(request_string, '', 'delete')
          break

    # after pre-existing auth is deleted, a new one can be made
    self.create_authorization()

  def get_members_of_org(self, organization):
    # GitHub paginates results, so we must make multiple requests and build up a collection of users from each individual response
    params = {'Accept': 'application/vnd.github.ironman-preview+json'}
    request_string = 'https://api.github.com/orgs/' + organization + '/members'

    def get_next_page_of_members(request_string):
      members_response = self.make_github_api_call(request_string, params, 'get')
      for member in members_response.json():
        self.follow_user(member['login'])
      if 'next' in members_response.links:
        get_next_page_of_members(members_response.links['next']['url'])

    get_next_page_of_members(request_string)


  def follow_user(self, username):
    print "Would follow user if enabled: ", username
    # first check if already following username, returns 204 if following, 404 if not following.
    # request_url = 'https://api.github.com/user/following/' + username
    # not_following_user = self.make_github_api_call(request_url, '', 'get')

    # # if user is not being followed, follow them.
    # if not_following_user:
      # params = {'Content-Length': 0, "Authorization": "token " + str(self.token)}
      # self.make_github_api_call(request_url, params, 'put')

def main():
  username = raw_input("Enter your github username: ")
  password = getpass("Enter your github password: ")
  org = raw_input("Enter the name of the organization whose members you would like to follow: ")

  conn = GitHubConnection(username, password, org)

if __name__ == "__main__":
    main()

