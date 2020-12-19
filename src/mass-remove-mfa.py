# pip install pipenv
# pipenv install requests
from mysecrets import ONELOGIN_CLIENT_ID, ONELOGIN_CLIENT_SECRET

import requests
import json

def get_onelogin_headers():
    r = requests.post(api_domain + '/auth/oauth2/v2/token',
    auth=(ONELOGIN_CLIENT_ID, ONELOGIN_CLIENT_SECRET),
    json={
        "grant_type": "client_credentials"
    }
    )
    response = r.json()

    access_token = response['access_token']
    return {'Authorization': 'Bearer ' + access_token, 'content-type': 'application/json'}

def get_user_ids():
    response = requests.get(api_domain + '/api/2/roles?name=Test', headers=headers)
    json_data = json.loads(response.content)
    user_ids = []
    for role in json_data:
        if role["name"] == "Test":
            user_ids = role["users"]
            break

    print("user ids under the Test role:")
    print("=============================")
    print(user_ids)
    print()
    return user_ids

def remove_factor_for_each_user(user_ids, factor_name):
    for user_id in user_ids:
        print("looking for devices enrolled with: " + factor_name)
        print("==================================================")
        print("user id: " + str(user_id))
        device_id = get_enrolled_mfa_device(user_id, factor_name)
        if device_id:
            print("enrolled device id: " + str(device_id))
            print("removing MFA enrolled with device id: " + str(device_id))
            remove_mfa_device(user_id, device_id)

        else:
            print("no enrolled device")
        print()

def get_enrolled_mfa_device(user_id, factor_name):
    response = requests.get(api_domain + '/api/1/users/' + str(user_id) + '/otp_devices', headers=headers)
    json_data = json.loads(response.content)
    device_id = 0
    for device in json_data["data"]["otp_devices"]:
        if device["auth_factor_name"] == factor_name:
            device_id = device["id"]
            break
    return device_id

def remove_mfa_device(user_id, device_id):
    response = requests.delete(api_domain + '/api/1/users/' + str(user_id) + '/otp_devices/' + str(device_id), headers=headers)
    json_data = json.loads(response.content)
    print("removal result: " + json_data["status"]["message"])

api_domain = 'https://api.us.onelogin.com'
factor_name = "OneLogin Protect"

# 1. Complete the following steps using the OneLogin API.
headers = get_onelogin_headers()
# 2. Get the role named "Test". 
user_ids = get_user_ids()
# 3. Remove factor for each user
remove_factor_for_each_user(user_ids, factor_name)
