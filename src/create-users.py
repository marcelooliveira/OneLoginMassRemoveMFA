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

# 5. Create a role named "Test". 
role_data = {
    "name":"Test"
}

response = requests.post(api_domain + '/api/2/roles', headers=headers, data=json.dumps(role_data))
json_data = json.loads(response.content)
test_role_id = json_data['id']

# 6. Create some users. 
r = range(5)
for n in r:
    user_data = {
        "email": "user" + str(n + 1) + "@myemail.com",
        "firstname": "user",
        "lastname": ["one", "two", "three", "four", "five"][n],
        "username": "user" + str(n + 1),
        "password": "useruser" + str(n + 1),
        "password_confirmation": "useruser" + str(n + 1),
        "role_ids":[
                str(test_role_id)
            ]
    }

    response = requests.post(api_domain + '/api/2/users', headers=headers, data=json.dumps(user_data))
    json_data = json.loads(response.content)

