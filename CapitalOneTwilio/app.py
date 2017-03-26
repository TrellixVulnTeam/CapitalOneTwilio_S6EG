
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
    response.message('Thank You for using the Capital One Online Banking SMS Service')
    return str(response)

if __name__ == '__main__':
    print('Running on port: {}'.format(os.environ.get('port')))
    app.run(port=int(os.environ.get('port')), debug=True)
