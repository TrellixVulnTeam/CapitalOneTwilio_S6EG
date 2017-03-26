#-*- coding: utf-8 -*-
from decimal import Decimal
from parse import *
import requests
from flask import Flask, render_template, request, json
import os
from twilio import twiml
from twilio.rest import TwilioRestClient
from functions import *
from datastore import *
from textblob import TextBlob
import datetime
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
    action, state_params = handle_input(request.form['Body'], action, state_params, ask_for)
    response, ask_for = gen_response(action, state_params)

    response = twiml.Response()
    if not isInDatabase:
        response.message("""Thank you for signing up for Capital One Text Banking! To get started, 
                        try making a request like “Show me my checking account balance,” or “Transfer $20 from my 
                        checking to my savings.” For more information, just send us a message asking for help!""")
    else:
        if ask_for is None:
            if action == 'transactions':
                response.message("It looks like you're trying to view your recent transactions. Is this correct?")
            elif action == 'alerts':
                response.message("It looks like you're trying to view your alerts. Is this correct?")
            elif action == 'register':
                response.message("It sounds like you'd like to register for text alerts. Is this correct?")
            elif action == 'call':
                response.message("It sounds like you'd like to speak to customer support. Is this correct?")
            elif action == 'balance':
                response.message("It sounds like you're trying to check the balance of your "+ state_params['account']+ " account. Is this correct?")
            elif action == 'transfer':
                response.message("It sounds like you're trying to transfer $"+ round(Decimal(state_params["amount"]), 2)+ " from "+ state_params["origin"]+ " to "+ state_params["dest"]+ ", is that correct?")
            elif action == 'find':
                locString = state_params['location'].replace(" Capital One", "")
                response.message("It sounds like you'd like to find "+ locString + ", is that correct?")
            elif action == 'help':
                response.message("""Don’t know where to start? Here’s everything you can do with our service:
                                    Check your account balance
                                    View your recent transactions
                                    View your alerts
                                    Transfer money between your accounts
                                    Transfer money to an external account via phone number
                                    Find ATMs and Capital One banking locations nearby or in a location of your choice
                                    Get connected with a customer service representative
                                    Sign up for text alerts related to your account""")
                action = None
                state_params = None
            elif action == 'confirmation':
                #NEED TO FIX
                if state_params["answer"] == "y":
                    response.message("Action confirmed!")
                    if action == 'balance':
                        response.message("The current balance in your " + state_params['account'] + " account is " + getAccount(request.form['From'], account=state_params['account'])['balance'])
                    elif action == 'transactions':
                        response.message('Your transaction history is:\n' + view_transfers(request.form['From']['id']))
                    elif action == 'alerts':
                        response.message("Feature coming soon!")
                    elif action == 'register':
                        response.message("Feature coming soon!")
                    elif action == 'call':
                        client.calls.create(to=18773834802, from_=request.form['From']['id'], url="https://df32cc8f.ngrok.com")
                    elif action == 'transfer':
                        make_transfer(request.form['From']['id'], 'p2p', state_params['dest'], datetime.datetime.utcnow(), state_params['amount']),
                        response.message(state_params['amount'] + " transferred from " + state_params['origin'] + " to " + state_params['dest'])
                    elif action == "find":
                        response.message("Feature coming soon!")
                    #send(action)
                    #send(state_params)
                    action = None
                    state_params = None
                else:
                    response.message("Sorry about that! Please try again.")
                    action = None
                    state_params = None            
        else:
            response.message(gen_response(action, state_params))
            # print("Secretly, I want to know the", ask_for)
            # print(response, "\n\n")

    
    return str(response)

if __name__ == '__main__':
    print('Running on port: {}'.format(os.environ.get('port')))
    app.run(port=int(os.environ.get('port')), debug=True)
