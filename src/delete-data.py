# pip install pipenv
# pipenv install requests
from mysecrets import ONELOGIN_CLIENT_ID, ONELOGIN_CLIENT_SECRET

import requests
import json

# 1. Complete the following steps using the OneLogin API.
api_domain = 'https://api.us.onelogin.com'
r = requests.post(api_domain + '/auth/oauth2/v2/token',
  auth=(ONELOGIN_CLIENT_ID, ONELOGIN_CLIENT_SECRET),
  json={
    "grant_type": "client_credentials"
  }
)
response = r.json()

access_token = response['access_token']
headers = {'Authorization': 'Bearer ' + access_token, 'content-type': 'application/json'}

# 2. Get the role named "Test". 
response = requests.get(api_domain + '/api/2/roles?name=Test', headers=headers)
json_data = json.loads(response.content)
test_role_id = 0
user_ids = []
for role in json_data:
    if role["name"] == "Test":
        user_ids = role["users"]
        test_role_id = role["id"]
        break

# 3. Delete test users
requests.delete(api_domain + '/api/2/roles/' + str(test_role_id) + '/users', headers=headers)
for user_id in user_ids:
    response = requests.delete(api_domain + '/api/2/users/' + str(user_id), headers=headers)

# 4. Delete test role
requests.delete(api_domain + '/api/2/roles/' + str(test_role_id), headers=headers)

