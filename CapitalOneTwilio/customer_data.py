import pyrebase
import requests
import json

cap_url = 'http://api.reimaginebanking.com/customers?key=553d42f5192db2a972b9478ce912075a'
fire_url = 'https://mhacks9-7440d.firebaseio.com'

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

person = {
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

result = db.child('Customers').push(person,token=user['idToken'])

