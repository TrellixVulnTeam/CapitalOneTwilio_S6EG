import requests
import datetime
import json
import redis
from CapitalOneTwilio.datastore import *

conn = redis.StrictRedis('localhost', charset='utf-8', decode_responses=True)
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)


# apiKey = '553d42f5192db2a972b9478ce912075a'

def create_account(number, type, nickname, rewards, balance):


def create_customer(firstname, lastname, address_number, address_st, city, state, zipcode):
    # url for create account api
    url = os.environ.get('capitalUrl') + os.environ.get('apiKey')
    body = {
        "phone_number": "+19252042443",
        "customer": {
            "first_name": firstname,
            "last_name": lastname,
            "address": {
                "street_number": address_number,
                "street_name": address_st,
                "city": city,
                "state": state,
                "zip": zipcode
            }
        },
        "accounts": {}
    }

    account = requests.post(url, json=(body['customer']))
    if account["objectCreated"]:
        body['customer'] = account["objectCreated"]
        updateDatabase((body))

        summary = "Account for " + account["objectCreated"]["first_name"] + " " + account["objectCreated"][
            "last_name"] + " successfully created"
    else:
        summary = "Failed to create account. Error code: " + account["code"]
    return summary


# view all transfers for specified id number
def view_transfers(id):
    url = 'http://api.reimaginebanking.com/accounts/416801051848956/transfers?key=553d42f5192db2a972b9478ce912075a'
    transfers = requests.get(url, id)
    summary = ''
    transaction_number = 1
    for x in transfers:
        date = datetime.datetime.fromtimestamp(
            int(transfers[x]["transaction_date"])
        ).strftime('%Y-%m-%d')
        summary += str(transaction_number) + ". " + transfers[x]["status"] + " " + transfers[x]["type"] + " of " + \
                   transfers[x]["amount"] + " on " + date
        summary += "\n"
        transaction_number += 1
    return summary


def make_transfer(id, type, to_id, timestamp, amount):
    # implement date as timestamp or "YYYY-MM-DD"
    # if transfer between accounts id == to_id
    url = 'http://api.reimaginebanking.com/accounts/642919792495030/transfers?key=553d42f5192db2a972b9478ce912075a'
    transfer_post = {
        "medium": "balance",
        "payee_id": to_id,
        "amount": amount,
        "transaction_date": timestamp,
    }
    transfer = requests.post(url, id, transfer_post)
    summary = ''
    if transfer["objectCreated"]:
        summary = "Transaction processed. " + "\n"
        summary += transfer["objectCreated"]["state"] + ["objectCreated"]["type"] + " of "
        summary += transfer["objectCreated"]["amount"]
    else:
        summary = "Transaction failed. Error code: " + transfer["code"]
    return summary


def make_deposit(id, amount):
    time = datetime.datetime.now()
    url = 'http://api.reimaginebanking.com/accounts/416801051848956/deposits?key=553d42f5192db2a972b9478ce912075a'
    deposit_post = {
        "medium": "balance",
        "transaction_date": time,
        "amount": amount
    }
    result = requests.post(url, deposit_post)
    if result["objectCreated"]:
        summary = "Transaction successful." + "\n"
        summary += result["objectCreated"]["status"] + " " + result["objectCreated"]["type"] + " of " + \
                   result["objectCreated"]["amount"]
    else:
        summary = "Transaction failed. Error code: " + result["code"]
    return summary
