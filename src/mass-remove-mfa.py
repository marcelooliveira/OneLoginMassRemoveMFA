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


# 3. Get OneLoginMFAGroup group
response = requests.get(api_domain + '/api/1/groups', headers=headers)
json_data = json.loads(response.content)
group_id = json_data['data'][0]['id']

# 4. Create a couple of users. 
user_data = {
    "email": "amelie.gagnon@myemail.com",
    "firstname": "Amélie",
    "lastname": "Gagnon",
    "username": "Amélie Gagnon",
    "role_ids":[
            str(test_role_id)
         ],
    "group_id": str(group_id),
    "phone": "+5511998215929"
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
         ],
    "group_id": str(group_id)
}

response = requests.post(api_domain + '/api/2/users', headers=headers, data=json.dumps(user_data))
json_data = json.loads(response.content)
user2_id = json_data['id']

# 4. Get available factors
response = requests.get(api_domain + '/api/2/mfa/users/' + str(user1_id) + '/factors', headers=headers)
json_data = json.loads(response.content)
factor_id = 0
for factor in json_data:
    if factor["name"] == "OneLogin SMS":
        factor_id = factor["factor_id"]
        break

# 5. Enroll a Factor

# mfa_data = {
#     "factor_id": str(factor_id),
#     "display_name": "OneLogin SMS"
# }

# response = requests.post(api_domain + '/api/2/users/' + str(user1_id) + '/registrations', headers=headers, data=json.dumps(mfa_data))

mfa_data = {
    "factor_id": str(factor_id),
    "display_name": "OneLogin SMS",
    "number": "+5511998215929"
}

response = requests.post(api_domain + '/api/1/users/' + str(user1_id) + '/otp_devices', headers=headers, data=json.dumps(mfa_data))

# THE ABOVE POST REQUEST WILL PRODUCE A HTTP 401 UNAUTHORIZED


# 6. Get Enrolled Factors
response = requests.get(api_domain + '/api/2/mfa/users/' + str(user1_id) + '/devices', headers=headers)
json_data = json.loads(response.content)
device_id = 0
for device in json_data:
    if factor["auth_factor_name"] == "OneLogin SMS":
        device_id = factor["device_id"]
        break

