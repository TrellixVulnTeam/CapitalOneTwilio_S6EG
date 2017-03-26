import redis
import requests
import os
import json
from dotenv import load_dotenv
from redisworks import Root

conn = redis.StrictRedis('localhost', charset='utf-8', decode_responses=True)
root = Root()

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)


def getAccount(number, account='All'):
        return root[number]['accounts'][account]


def createCustomer(payload=None):
    url = os.environ.get('capitalUrl') + 'customers?key={}' \
        .format(os.environ.get('apiKey'))
    body = {
        "phone_number": os.environ.get('fromNumber'),
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
        }
    }

    customer = requests.post(url, json=(body['customer'])).json()
    if customer["objectCreated"]:
        body['customer'] = customer["objectCreated"]

        # Retrieve Accounts
        accounts = requests.get(os.environ.get('capitalUrl')+'accounts?key='+os.environ.get('apiKey')).json()
        temp_acct = {
            'Checking': {}
            'Credit Card': {}
            'Savings': {}
        }
        has_checking = False
        has_saving = False
        has_credit = False
        for i in range(accounts):
            if has_checking == True && has_saving == True && has_credit == True:
                break
            elif account[i]['type'] == "Checking" && has_checking == False:
                temp_acct['Checking'] = account[i]
                has_checking == True;
            elif account[i]['type'] == "Saving" && has_saving == False:
                temp_acct['Saving'] = account[i]
                has_saving == True;
            elif account[i]['type'] == "Credit Card" && has_credit == False:
                temp_acct['Credit Card'] = account[i]
                has_credit == True;
        body['accounts'] = temp_acct
        updateDatabase((body))

        summary = "Customer " + customer["objectCreated"]["first_name"] + " " + customer["objectCreated"][
            "last_name"] + " successfully created"
    else:
        summary = "Failed to create customer. Error code: " + customer["code"]
    return summary


def createAccount(number, payload=None):
    user = getUser(number)
    payload = {
        "type": payload['type'] if payload else "Credit Card",
        "nickname": payload['nickname'] if payload else "Checking",
        "rewards": payload['rewards'] if payload else 0,
        "balance": payload['balance'] if payload else 0
    }

    print(user)
    print(os.environ.get('apiKey'))
    url = os.environ.get('capitalUrl') + 'customers/' \
          + user['customer']['_id'] \
          + '/accounts/?key=' + os.environ.get('apiKey')
    print(url)

    account = requests.post(url, json=(payload)).json()
    if account["objectCreated"]:
        obj = account["objectCreated"]
        print(root[user['phone_number']])
        root[user['phone_number']] = user
        updateDatabase(user)

        summary = obj['nickname'] + " account successfully created"
    else:
        summary = "Failed to create customer. Error code: " + account["code"]
    return summary


def getUser(number):
    return root[number]


def updateDatabase(user):
    root[user['phone_number']] = user
    root.flush()

def deleteAccount(number, id=None):
    accounts = requests.get(os.environ.get('capitalUrl') + 'accounts?key=' + os.environ.get('apiKey')).json()
    for i in range(len(accounts)):
        url = (os.environ.get('capitalUrl')+'accounts/'+accounts[i]['_id']+'?key='+os.environ.get('apiKey'))
        requests.delete(url)

if __name__ == '__main__':
    num = os.environ.get('fromNumber')
    print(createCustomer())
    #print(createAccount(num))
    # print(createAccount(num, {
    #     'type': 'Credit Card',
    #     'nickname': 'Savings',
    #     'rewards': 500,
    #     'balance': 1000
    # }))
