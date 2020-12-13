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
headers = headers = {'Authorization': 'Bearer ' + access_token, 'content-type': 'application/json'}

# 2. Create a role named "Test". 
role_data = {
    "name":"Test"
}

response = requests.post(api_domain + '/api/2/roles', headers=headers, data=json.dumps(role_data))
json_data = json.loads(response.content)
test_role_id = json_data['id']

# 3. Create a couple of users. 
user_data = {
    "email": "amelie.gagnon@myemail.com",
    "firstname": "Amélie",
    "lastname": "Gagnon",
    "username": "Amélie Gagnon",
    "role_ids":[
            str(test_role_id)
         ]
}

response = requests.post(api_domain + '/api/2/users', headers=headers, data=json.dumps(user_data))
json_data = json.loads(response.content)
user1_id = json_data['id']
response = requests.put(api_domain + '/api/2/users', headers=headers, data=json.dumps(user_data))

user_data = {
    "email": "thomas.tremblay@myemail.com",
    "firstname": "Thomas",
    "lastname": "Tremblay",
    "username": "Thomas Tremblay",
    "role_ids":[
            str(test_role_id)
         ]
}

response = requests.post(api_domain + '/api/2/users', headers=headers, data=json.dumps(user_data))
json_data = json.loads(response.content)
user2_id = json_data['id']

# 4. Delete data
# response = requests.delete(api_domain + '/api/2/users/' + str(user1_id), headers=headers)
# response = requests.delete(api_domain + '/api/2/users/' + str(user2_id), headers=headers)

