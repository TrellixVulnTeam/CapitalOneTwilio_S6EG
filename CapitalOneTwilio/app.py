
import requests
from flask import Flask, render_template, request, json
import os
from twilio import twiml
from twilio.rest import TwilioRestClient
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

client = TwilioRestClient(account=os.environ.get('accountSid'),
                          token=os.environ.get('authToken'))
app = Flask(__name__)


@app.route('/sms', methods=['POST'])
def inbound_sms():
    response = twiml.Response()

    r = requests.get('http://api.reimaginebanking.com/customers?key={}'
                     .format(os.environ.get('apiKey')))

    data = r.json()
    payload = ''
    for i in range(len(r.json())):
        payload += 'First Name: {}\nLast Name: {}\n'\
        .format(data[i]['first_name'], data[i]['last_name'])

    response.message(payload)
    print(payload)

    return str(response)

if __name__ == '__main__':
    print('Running on port: {}'.format(os.environ.get('port')))
    app.run(port=int(os.environ.get('port')), debug=True)
