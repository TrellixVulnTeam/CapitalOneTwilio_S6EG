import redis
import requests
import os
import json
from dotenv import load_dotenv
from redisworks import Root
from decimal import Decimal
import datetime

conn = redis.StrictRedis('localhost', charset='utf-8', decode_responses=True)
root = Root(host='localhost', return_object=True)

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

sets = (set, frozenset)

from builtins import int
strings = (str, bytes)  # which are both basestring
numbers = (int, float, complex, datetime.datetime, datetime.date, Decimal)
items = 'items'
import builtins
from collections import MutableMapping, Iterable


TYPE_IDENTIFIER = '!__'
bTYPE_IDENTIFIER = TYPE_IDENTIFIER.encode('utf-8')
ITEM_DIVIDER = '|==|'
bITEM_DIVIDER = ITEM_DIVIDER.encode('utf-8')

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
DATE_FORMAT = "%Y-%m-%d"

# In addition to built in types:
OTHER_STANDARD_TYPES = {'Decimal': Decimal, 'datetime': datetime.datetime, 'date': datetime.date}

TYPE_FORMATS = {
    numbers: "num",
    sets: "set",
    MutableMapping: "dict",
    Iterable: "list",
    "obj": "obj",
    strings: "str"
}

for i in TYPE_FORMATS:
    TYPE_FORMATS[i] = TYPE_IDENTIFIER + TYPE_FORMATS[i] + ITEM_DIVIDER +\
                      '{actual_type}' + ITEM_DIVIDER + '{value}'

def getAccount(number, account='All'):
        accounts = getUser(number)['accounts']
        return accounts if account=='All' else accounts[account]

def createCustomer(number, payload=None):
    url = os.environ.get('capitalUrl') + 'customers?key={}' \
        .format(os.environ.get('apiKey'))
    body = {
        "phone_number": number,
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
        updateDatabase(body['phone_number'], body)

        summary = "Customer " + customer["objectCreated"]["first_name"] + " " + customer["objectCreated"][
            "last_name"] + " successfully created"
    else:
        summary = "Failed to create customer. Error code: " + customer["code"]
    return summary


def createAccount(number, payload=None):
    user = getUser(number)
    print(user)

    #print(root.return_object)

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
        #print(root[user['phone_number']])
        user['accounts'][obj['type']] = obj
        #print(user)

        #root[user['phone_number']] = user
        updateDatabase(number, user)

        summary = obj['nickname'] + " account successfully created"
    else:
        summary = "Failed to create customer. Error code: " + account["code"]
    return summary


def getUser(number):
    return root.load([number])[number]

def updateDatabase(number, user):
    root.flush()
    root.save(number, user)


def deleteAccount(number, id=None):
    accounts = requests.get(os.environ.get('capitalUrl') + 'accounts?key=' + os.environ.get('apiKey')).json()
    for i in range(len(accounts)):
        url = (os.environ.get('capitalUrl')+'accounts/'+accounts[i]['_id']+'?key='+os.environ.get('apiKey'))
        requests.delete(url)

def kevinsalgo():


if __name__ == '__main__':
    for num in os.environ.get('numbers'):
        createCustomer(num)
        createAccount(num)
        user = getUser(num)

