# creating mock data for Capital One API usage
# created by Noah Kalil - MHacks 9
# 3/25/2017

import urllib2
import json

apiKey = '553d42f5192db2a972b9478ce912075a'
url = 'http://api.reimaginebanking.com/customers?key=553d42f5192db2a972b9478ce912075a'
url2 = 'https://mhacks9-7440d.firebaseio.com/Customers'

for i in range(10):
    response = urllib2.urlopen(url)

    data = json.load(response)
    request.post(url2,data)
