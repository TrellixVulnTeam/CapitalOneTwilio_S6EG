# creating mock data for Capital One API usage
# created by Noah Kalil - MHacks 9
# 3/25/2017

import urllib2
import curl
import json

apiKey = '553d42f5192db2a972b9478ce912075a'

for i in range(10)
    url = 'http://api.reimaginebanking.com/customers?key=553d42f5192db2a972b9478ce912075a'
    response = urllib2.urlopen(url)

    data = json.load(response)
    curl -X POST -d 'data' \
        'https://mhacks9-7440d.firebaseio.com/Customers.json'