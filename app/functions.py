import requests
from pandas.io.json import json_normalize as j
import pandas as pd
import datetime as dt
from urllib.parse import quote
import urllib3
import json

urllib3.disable_warnings()

api_key= 'c35d26d6ecbc452cb2923b8f97b92f734fad0a50829f4136907795da2f867f9d'
private_key = 'MjZlZkJTMnFhRXdMeXhzZg=='

base_url = 'https://api.spoc.com/api/'

def authenticate(api_key, private_key):
    command = "Authenticate"
    url = base_url + command
    payload = "{'APIKey':'"+api_key+"','PrivateKey':'"+private_key+"'}"
    response = requests.post(url, data = payload, verify=False)
    key_auth = response.json()
    return key_auth

def userLogin(authCode, username):
    command = 'UserLogin'
    url = base_url + command
    payload = "{'aka':'"+username+"','authCode':'"+authCode+"'}"
    response = requests.post(url, data = payload, verify=False)
    userLogin = response.json()
    return userLogin

def getUserData(sessionID):
    command = 'FetchUserData'
    url = base_url + command +"?SessionID="+sessionID
    response = requests.get(url, verify=False)
    data = response.json()
    return data

def checkToken(sessionID):
    command = 'CheckToken'
    url = base_url + command +"?SessionID="+sessionID
    response = requests.get(url, verify=False)
    data = response.json()
    return data

def addPreference(sessionID, preference, value):
    command = 'AddPreference'
    url = base_url + command
    payload = "{'SessionID':'"+sessionID+"','Preference':'"+preference+"','Value':'"+value+"'}"
    response = requests.post(url, data = payload, verify=False)
    data = response.json()
    return data

def loginPortal(aka_username):
    user = 'temp name'
    auth_key = authenticate(api_key, private_key)
    if auth_key['status'] == 'Authenticated':
        login = userLogin(auth_key['authCode'], aka_username)
        if login['status'] == 'login_success':
            user = getUserData(login['sessionID'])
            if user['status'] == 'success':
                login_status = 'Successfully got user data'
            else: # if get user data unsuccessful
                login_status = 'Unable to get user data'
        else: #if login status != success
            login_status = 'Login Unsuccessful'
    else: # if auth_key != 'Authenticated'
        login_status ='API Keys Not Authenticated'
    return user, login_status
