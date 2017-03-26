import requests
import datetime
import pyrebase
import json

apiKey = '553d42f5192db2a972b9478ce912075a'

def create_account(firstname,lastname,address_number,address_st,city,state,zipcode):
    # url for create account api
    url = 'http://api.reimaginebanking.com/customers?key=553d42f5192db2a972b9478ce912075a'
    person = {
        "first_name": firstname,
        "last_name": lastname,
        "address": {
            "street_number": address_number,
            "street_name": address_st,
            "city": city,
            "state": state,
            "zip": zipcode
            }
        }
    account = requests.post(url,person)
    if account["objectCreated"]:
        config = {
          'apiKey': 'AIzaSyDJZDg3h4DOYc1sS4_zyr2u8QKkAgDnqkA',
          'authToken': 'b2vBy3Ph9nyyUXaJ3CssM5EnTd0Xmzu2i4j8OTQC',
          'authDomain': ' mhacks9-7440d.firebase.com',
          'databaseURL': 'https://mhacks9-7440d.firebaseio.com',
          'storageBucket': 'mhacks9-7440d.appspot.com',
          'serviceAccount': './MHacks9-fac130f64d40.json'
        }
        firebase = pyrebase.initialize_app(config)
        user = firebase.auth().sign_in_with_email_and_password('ashwin.gokhale98@gmail.com', 'Ashwin98')

        db = firebase.database()

        result = db.child('Customers').push(account["objectCreated"],token=user['idToken'])
        summary = "Account for " + account["objectCreated"]["first_name"] + " " + account["objectCreated"]["last_name"] + " successfully created"
    else:
        summary = "Failed to create account. Error code: " + account["code"]
    return summary

# view all transfers for specified id number
def view_transfers(id):
    url = 'http://api.reimaginebanking.com/accounts/416801051848956/transfers?key=553d42f5192db2a972b9478ce912075a'
    transfers = requests.get(url, id)
    summary
    transaction_number = 1
    for x in transfers:
        date = datetime.datetime.fromtimestamp(
            int(transfers[x]["transaction_date"])
        ).strftime('%Y-%m-%d')
        summary += str(transaction_number) + ". " + transfers[x]["status"] + " " + transfers[x]["type"] + " of " +  transfers[x]["amount"] + " on " + date
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
    summary
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
    result = requests.post(url,deposit_post)
    if result["objectCreated"]:
        summary = "Transaction successful." + "\n"
        summary += result["objectCreated"]["status"] + " " + result["objectCreated"]["type"] + " of "  + result["objectCreated"]["amount"]
    else:
        summary = "Transaction failed. Error code: " + result["code"]
    return summary
