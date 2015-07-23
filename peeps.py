from getpass import getpass
from urlparse import urljoin
import json
import requests

class GitHubConnection(object):

  def __init__(self, username, password, org, team):
    default_req = requests.Session()
    default_req.auth = (username, password)
    # Custom Accept header suggested by GitHub, see: https://developer.github.com/v3/media/#request-specific-version
    default_req.headers.update({'Accept': 'application/vnd.github.v3+json'})
    self.default_request = default_req
    self.token = ''
    self.org = org
    self.team = team

    # Start by deleting any previous peeps authorizations because github does not allow retrieval of tokens.
    self.delete_existing_authorization()

  def make_github_api_call(self, request_string, params, http_verb):
    try:
      return getattr(self.default_request, http_verb)(request_string, data=json.dumps(params))
    except requests.exceptions.RequestException as e:
      print e
      sys.exit(2)

  def create_authorization(self):
    params = {"note": "followpeepsscriptv2", "scopes": ["user", "read:org"]}
    credentials = self.make_github_api_call('https://api.github.com/authorizations', params, 'post').json()
    self.token = credentials['token']
    if self.team == None:
      self.get_members_of_org(self.org)
    else:
      self.get_members_of_team(self.team)

  def delete_existing_authorization(self):
    # Deletes an existing authorization for peeps if it exists.
    old_peeps_id = None
    existing_authorizations = self.make_github_api_call('https://api.github.com/authorizations', '', 'get').json()
    if existing_authorizations:
      for auth in existing_authorizations:
        if auth['note'] == "followpeepsscriptv2":
          old_peeps_id = str(auth['id'])
          request_string = 'https://api.github.com/authorizations/' + old_peeps_id
          self.make_github_api_call(request_string, '', 'delete')
          break

    self.create_authorization()


  def get_next_page_of_members(self, request_string, params):
    members_response = self.make_github_api_call(request_string, params, 'get')
    if members_response.status_code == 404:
      print "Error: Could not find members of: '" + organization + "'."
      members_response.raise_for_status()
    if members_response.status_code == 403:
      print "Error: You do not have permission to access to this group."
      members_response.raise_for_status()
    for member in members_response.json():
      self.follow_user(member['login'])
    if 'next' in members_response.links:
      self.get_next_page_of_members(members_response.links['next']['url'], params)

  def get_members_of_org(self, organization):
    # GitHub paginates results, so we must make multiple requests and follow users from each response.
    params = {'Accept': 'application/vnd.github.ironman-preview+json'}
    request_string = 'https://api.github.com/orgs/' + organization + '/members'
    self.get_next_page_of_members(request_string, params)


  def get_members_of_team(self, team):
    # GitHub paginates results, so we must make multiple requests and follow users from each response.
    team_id = ''
    params = {'Accept': 'application/vnd.github.ironman-preview+json'}
    request_string = 'https://api.github.com/orgs/' + self.org + '/teams'
    teams_response = self.make_github_api_call(request_string, params, 'get')
    if teams_response.status_code == 403:
      print "Error: You must have admin rights to the organization."
      teams_response.raise_for_status()
    else:
      for individual_team in teams_response.json():
        if individual_team['name'].lower() == team:
          team_id = individual_team['id']
        break
      if team_id == '':
        print "Sorry, team '" + team + "' could not be found in organization '" + self.org + "'."
      if team_id != '':
        request_string = 'https://api.github.com/teams/' + str(team_id) + '/members'
        self.get_next_page_of_members(request_string, params)

  def follow_user(self, username):
    print "Would follow user if enabled: '" + username + "'."

    #################################################
    # UNCOMMENT THE CODE BELOW TO ENABLE FOLLOWING! #
    #################################################

    # # First check if already following user before sending a follow request.
    # request_url = 'https://api.github.com/user/following/' + username
    # check_follow_status = self.make_github_api_call(request_url, '', 'get')

    # # If a user is not currently followed, the server will respond with a 404.
    # if check_follow_status.status_code == 404:
    #   params = {'Content-Length': 0, "Authorization": "token " + str(self.token)}
    #   follow_user_response = self.make_github_api_call(request_url, params, 'put')

    #   # If a user is successfully followed, the server will respond with a 204.
    #   if follow_user_response.status_code == 204:
    #     print "You are now following: '" + username + "'."
    #   else:
    #     print "Error: There was a problem following: ", username

def main():
  username = raw_input("Enter your github username: ")
  password = getpass("Enter your github password: ")
  team_or_organization = ''

  while team_or_organization not in ["t", "o"]:
    team_or_organization = raw_input("Enter 't' to follow members of a team or 'o' to follow members of an organization: ").lower()

  if team_or_organization == 'o':
    org = raw_input("Enter the name of the organization whose members you would like to follow: ")
    team = None
  else:
    team = raw_input("Enter the name of the team: ").lower()
    org = raw_input("Enter the name of the organization in which the team resides: ")

  conn = GitHubConnection(username, password, org, team)

if __name__ == "__main__":
    main()

