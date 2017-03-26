import redis
import requests
import os
import json
from dotenv import load_dotenv

conn = redis.StrictRedis('localhost', charset='utf-8', decode_responses=True)
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)


def getAccount(number, account):
    if account != 'All':
        return conn.hgetall(number)['accounts'][account]
    else:
        return conn.hgetall(number)['accounts']


def createCustomer(payload=None):
    # url for create account api

    url = os.environ.get('capitalUrl') + 'customers?key={}'\
        .format(os.environ.get('apiKey'))
    body = {
        "phone_number": "+19252042443",
        "customer": dict([
            ("first_name", payload['first_name'] if payload else "Buddy"),
            ("last_name", payload['last_name'] if payload else "Guy"),
            ("address", dict([
                ("street_number", payload['street_number'] if payload else "1234"),
                ("street_name", payload['street_name'] if payload else "Main St"),
                ("city", payload['city'] if payload else "Ann Arbor"),
                ("state", payload['state'] if payload else "MI"),
                ("zip", payload['zipcode'] if payload else "48109")
                ]).__dict__
            )
        ]),
    "accounts": dict().__dict__
    }

    customer = requests.post(url, json=(body['customer'])).json()
    if customer["objectCreated"]:
        body['customer'] = customer["objectCreated"]
        updateDatabase((body))

        summary = "customer for " + customer["objectCreated"]["first_name"] + " " + customer["objectCreated"][
            "last_name"] + " successfully created"
    else:
        summary = "Failed to create customer. Error code: " + customer["code"]
    return summary

def create_account(number,payload=None):
    user = getUser(number)
    payload = {
        "type": payload['type'] if payload else "Credit Card",
        "nickname": payload['string'] if payload else "Checking",
        "rewards": payload['rewards'] if payload else 0,
        "balance": payload['balance'] if payload else 0
    }

    url = os.environ.get('capitalUrl') + 'customers/' \
          + json.loads(serialize(user['customer']))['_id'] \
          + '/accounts/?key=' + os.environ.get('apiKey')

    account = requests.post(url, json=(payload)).json()
    if account["objectCreated"]:
        obj = account["objectCreated"]
        user['accounts'] = json.loads(serialize(user['accounts']))
        user['accounts'][obj['nickname']] = obj['_id']
        updateDatabase((user))

        summary = obj['nickname'] + " account successfully created"
    else:
        summary = "Failed to create customer. Error code: " + account["code"]
    return summary

    data = r.json()['objectCreated']
    user['accounts'][data['nickname']] = data
    updateDatabase((user))




def createAccount(body=None):
    if body == None:
        body = {
            'phone_number': '+19252042443',
            'customer': {
                'first_name': 'Buddy',
                'last_name': 'Guy',
                'address': {
                    'street_number': '1234',
                    'street_name': 'Main st',
                    'city': 'Ann Arbor',
                    'state': 'MI',
                    'zip': '48109'
                }
            },
            'accounts': {}
        }

    url = os.environ.get('capitalUrl') + 'customers?key={}' \
        .format(os.environ.get('apiKey'))

    r = requests.post(url, json=(body['customer']))
    data = r.json()['objectCreated']
    body['customer'] = data
    updateDatabase((body))


def getUser(number):
    return conn.hgetall(number) if (number != True and False) else conn.hgetall(os.environ.get('fromNumber'))


def updateDatabase(user):
    conn.hmset((user)['phone_number'], user)

def serialize(string):
    return string.replace("'", '"')


if __name__ == '__main__':
    cust = conn.hgetall('+19252042443')
    cust['customer'] = json.loads(serialize(cust['customer']))
    #cust['accounts'] = json.loads(serialize(cust['accounts']))
    print(create_account(cust['phone_number']))
    print(type(getAccount(cust['phone_number'], 'All')))