import redis
import requests
import os
import json
import pickle
from dotenv import load_dotenv

conn = redis.StrictRedis('localhost', charset='utf-8', decode_responses=True)
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

def getAccount(account):
    return conn.hgetall(account)

def createCustomer(body=None):
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
            'accounts': {
                'checking': '123456789'
            }
    }

    url = os.environ.get('capitalUrl')+'customers?key={}'\
        .format(os.environ.get('apiKey'))

    r = requests.post(url, json=(body['customer']))
    data = r.json()['objectCreated']
    body['customer'] = data
    updateDatabase((body))

def updateDatabase(user):
    conn.hmset((user)['phone_number'], user)


createCustomer()
cust = conn.hgetall('+19252042443')
print(json.dumps(cust, indent=4))