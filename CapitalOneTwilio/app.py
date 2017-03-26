
import requests
from flask import Flask, render_template, request, json
import os
from twilio import twiml
from twilio.rest import TwilioRestClient
from datastore import *
from dotenv import load_dotenv
import redis

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)
conn = redis.StrictRedis('localhost', charset='utf-8', decode_responses=True)

client = TwilioRestClient(account=os.environ.get('accountSid'),
                          token=os.environ.get('authToken'))
app = Flask(__name__)


@app.route('/sms', methods=['POST'])
def inbound_sms():
    isInDatabase = conn.hgetall(request.form['From'])
    response = twiml.Response()
    response.message('Thank you for signing up for Capital One Text Banking! To get started, try making a request like “Show me my checking account balance,” or “Transfer $20 from my checking to my savings.” For more information, just send us a message asking for help!')
    return str(response)

if __name__ == '__main__':
    print('Running on port: {}'.format(os.environ.get('port')))
    app.run(port=int(os.environ.get('port')), debug=True)
