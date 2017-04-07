import requests
import os
import json
from dotenv import load_dotenv
import pyrebase

config = {
    "apiKey": "AIzaSyDJZDg3h4DOYc1sS4_zyr2u8QKkAgDnqkA",
    "authDomain": "mhacks9-7440d.firebaseapp.com",
    "databaseURL": "https://mhacks9-7440d.firebaseio.com",
    "storageBucket": "mhacks9-7440d.appspot.com",
    "messagingSenderId": "1538242320"
}

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

firebase = pyrebase.initialize_app(config)
db = firebase.database()
token = os.environ.get('fbToken')

def getAccount(number, account='All'):
        accounts = getUser(number)['accounts']
        return accounts if account=='All' else accounts[account]

def createCustomer(number, payload=None):
    url = os.environ.get('capitalUrl') + 'customers?key={}' \
        .format(os.environ.get('apiKey'))
    body = {
        "customer": {
            "first_name": payload['first_name'] if payload else "Buddy",
            "last_name": payload['last_name'] if payload else "Guy",
            "address": {
                "street_number": payload['street_number'] if payload else "1234",
                "street_name": payload['street_name'] if payload else "Main St",
                "city": payload['city'] if payload else "Ann Arbor",
                "state": payload['state'] if payload else "MI",
                "zip": payload['zipcode'] if payload else "48109"
            }
        },
        "action": "None",
        "state_params": "None",
        "ask_for": "None"
    }

    customer = requests.post(url, json=(body['customer'])).json()
    if customer["objectCreated"]:
        body['customer'] = customer["objectCreated"]

        # Retrieve Accounts
        accounts = requests.get(os.environ.get('capitalUrl')+'customers/' + body['customer']['_id']+ '/ accounts?key='+os.environ.get('apiKey')).json()
        temp_acct = {
            'Checking': {},
            'Credit Card': {},
            'Savings': {}
        }

        has_checking = False
        has_saving = False
        has_credit = False
        for i in range(len(accounts)):
            if has_checking == True and has_saving == True and has_credit == True:
                break
            elif accounts[i]['type'] == "Checking" and has_checking == False:
                temp_acct['Checking'] = accounts[i]
                has_checking = True
            elif accounts[i]['type'] == "Saving" and has_saving == False:
                temp_acct['Saving'] = accounts[i]
                has_saving = True
            elif accounts[i]['type'] == "Credit Card" and has_credit == False:
                temp_acct['Credit Card'] = accounts[i]
                has_credit = True
        body['accounts'] = temp_acct
        updateDatabase(number, body)

        summary = "Customer " + customer["objectCreated"]["first_name"] + " " + customer["objectCreated"][
            "last_name"] + " successfully created"
    else:
        summary = "Failed to create customer. Error code: " + customer["code"]
    return summary


def createAccount(number, payload=None):
    user = getUser(number)
    payload = {
        "type": payload['type'] if payload else "Credit Card", # Credit Card, Checkings, Savings
        "nickname": payload['nickname'] if payload else "Checking",
        "rewards": payload['rewards'] if payload else 0,
        "balance": payload['balance'] if payload else 0
    }

    url = os.environ.get('capitalUrl') + 'customers/' \
          + user['customer']['_id'] \
          + '/accounts/?key=' + os.environ.get('apiKey')

    account = requests.post(url, json=(payload)).json()
    if account["objectCreated"]:
        obj = account["objectCreated"]
        user['accounts'][obj['type']] = obj
        updateDatabase(number, user)

        summary = obj['nickname'] + " account successfully created"
    else:
        summary = "Failed to create customer. Error code: " + account["code"]
    return summary


def getUser(number):
    query = db.child("Customers").child(number).get(token).val()
    return json.loads(json.dumps(query))

def updateDatabase(number, user):
    db.child("Customers").child(number).update(user, token)

def updateField(number, key, value):
    user = getUser(number)
    user[key] = value
    updateDatabase(number, user)


def deleteAccount(number, id=""):
    requests.delete(os.environ.get('capitalUrl')+'accounts/'+id+'?key='+os.environ.get('apiKey'))
