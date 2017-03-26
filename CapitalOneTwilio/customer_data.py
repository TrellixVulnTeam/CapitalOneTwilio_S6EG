import pyrebase
import requests
import json

cap_url = 'http://api.reimaginebanking.com/customers?key=553d42f5192db2a972b9478ce912075a'
fire_url = 'https://mhacks9-7440d.firebaseio.com'

config = {
  'apiKey': 'AIzaSyDJZDg3h4DOYc1sS4_zyr2u8QKkAgDnqkA',
  'authDomain': ' mhacks9-7440d.firebase.com',
  'databaseURL': 'https://mhacks9-7440d.firebaseio.com',
  'storageBucket': 'mhacks9-7440d.appspot.com'
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
results = db.get('/Customers')

print(results)


example_person = {
  'first_name': 'Joe',
  'last_name': 'Schmoe',
  'address': {
    'street_number': '1234',
    'street_name': 'example st',
    'city': 'Ann Arbor',
    'state': 'MI',
    'zip': '48109'
  }
}
'''
example_json_data = json.dumps(example_person)

response = requests.post(cap_url, data=example_json_data, headers = {'content-type': 'application/json'})
person = json.loads(response.text)['objectCreated']
user_info = {
    'url': fire_url,
    'first_name': person['first_name'],
    'last_name': person['last_name'],
    'user_id': person['_id']
}
data = json.dumps(user_info)
result = firebase.post('/Customers', data=data)
'''
