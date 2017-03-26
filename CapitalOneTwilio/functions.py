import requests
import datetime

apiKey = '553d42f5192db2a972b9478ce912075a'

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
        summary += str(transaction_number) + '. ' + transfers[x]["status"] + " " transfers[x]["type"] + " of " +  transfers[x]["amount"] + " on " + date
        summary += "\n"
        transaction_number += 1
    return summary

def make_transfer(id, type, to_id, timestamp, amount):
    # implement date as timestamp or "YYYY-MM-DD"
    # if transfer between accounts id == to_id
    url = 'http://api.reimaginebanking.com/accounts/642919792495030/transfers?key=553d42f5192db2a972b9478ce912075a'
    transfer-post = {
        "medium": "balance",
        "payee_id": to_id,
        "amount": amount,
        "transaction_date": timestamp,
    }
    transfer = requests.post(url, id, transfer-post)
    summary
    if transfer["objectCreated"]:
        summary = "Transaction processed. " + "\n"
        summary += transfer["objectCreated"]["state"] + ["objectCreated"]["type"] + " of "
        summary += transfer["objectCreated"]["amount"]
    else
        summary = "Transaction failed"
    return summary
