# creating mock data for Capital One API usage
# created by Noah Kalil - MHacks 9
# 3/25/2017

import json
import requests

apiKey = '553d42f5192db2a972b9478ce912075a'
url = 'http://api.reimaginebanking.com/customers?key=553d42f5192db2a972b9478ce912075a'
url2 = 'https://mhacks9-7440d.firebaseio.com/Customers'
url_random = 'https://randomuser.me/api/?inc=name,location&results='
url_random_1 = 'https://randomuser.me/api/?inc=name,location'

"""
def make_fake_people(n_people):
    req_url = url_random+str(n_people)
    print(req_url)
    response = requests.get(req_url, verify=False)
    api_people = json.loads(response.text)
    capone_people = list()
    for person in api_people.results:
        print(person)
    #return person

make_fake_people(5)
"""
"""
def make_person():
    random_person = requests.get(url_random_1)
    person = json.loads(random_person.text)
    address = []
    address.append(person[address].split(" ",1))
    payload = {
    "first_name": person[first],
    "last_name": person[last],
    "address": {
        "street_number": address[0],
        "street_name": address[1],
        "city": person[city],
        "state": person[state],
        "zip": person[postalcode]
        }
    }
    return payload


for i in range(10):
    random_person = make_person()
    requests.post(url2,random_person)
    print(i)
    print(random_person)
"""

def post_user(first_name, last_name, user_id):
    person = {
        "user_id": user_id,
        "first_name": first_name,
        "last_name": last_name
    }
    result = firebase.post(url2,'/Customers',person)
    print(result)


# basic customers
payload = {
  "first_name": "Joe",
  "last_name": "Schmoe",
  "address": {
    "street_number": "1234",
    "street_name": "example st",
    "city": "Ann Arbor",
    "state": "MI",
    "zip": "48109"
  }
}

person = requests.post(url,payload)
post_user(person["first_name"], person["last_name"], person["_id"])
