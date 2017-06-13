# -*- coding: utf-8 -*-
from nlp.message_parser import *
from datastore import *
from flask import Flask, render_template, request, json
import os
import twilio.twiml
from twilio.rest import TwilioRestClient
import datetime
from decimal import Decimal
from dotenv import load_dotenv
import pyrebase

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

config = {
    "apiKey": "AIzaSyDJZDg3h4DOYc1sS4_zyr2u8QKkAgDnqkA",
    "authDomain": "mhacks9-7440d.firebaseapp.com",
    "databaseURL": "https://mhacks9-7440d.firebaseio.com",
    "storageBucket": "mhacks9-7440d.appspot.com",
    "messagingSenderId": "1538242320"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
token = os.environ.get('fbToken')

client = TwilioRestClient(account=os.environ.get('accountSid'),
                          token=os.environ.get('authToken'))
app = Flask(__name__)


@app.route('/', methods=['GET'])
def inbound_get():
    return "<h1>The is the Home page</h1>"


@app.route('/sms', methods=['POST'])
def inbound_sms():
    number = request.form['From']
    user = getUser(number)
    response = twilio.twiml.Response()

    if not user:
        print(createCustomer(number))
        response.message(
            'Thank you for signing up for Capital One Text Banking! To get started,try making a request like “Show '
            'me my checking account balance,” or “Transfer 20 from mychecking to my savings.” For more '
            'information, '
            'just send us a message asking for help!'
        )

    else:
        action, state_params = handle_input(number, request.form['Body'])
        resp, ask_for = gen_response(action, state_params)

        # Update fields after processing them
        updateField(number, 'action', action)
        updateField(number, 'state_params', state_params)
        updateField(number, 'ask_for', ask_for)

        confirmed = user.get('confirmed')

        response.message(resp)

        if ask_for is None:
            if confirmed == True:
                if state_params["answer"] == "y":
                    response.message("Action confirmed!")
                    if action == 'balance':
                        response.message("The current balance in your " + state_params['account'] + " account is " +
                                         getAccount(number, account=state_params['account'])['balance'])
                    elif action == 'transactions':
                        response.message('Your transaction history is:\n' + view_transfers(number['id']))
                    elif action == 'alerts':
                        response.message("Feature coming soon!")
                    elif action == 'register':
                        response.message("Feature coming soon!")
                    elif action == 'call':
                        client.calls.create(to=18773834802, from_=number['id'],
                                            url="https://df32cc8f.ngrok.com")
                    elif action == 'transfer':
                        make_transfer(number['id'], 'p2p', state_params['dest'],
                                      datetime.datetime.utcnow(), state_params['amount']),
                        response.message(
                            state_params['amount'] + " transferred from " + state_params['origin'] + " to " +
                            state_params['dest'])
                    elif action == "find":
                        response.message("Feature coming soon!")

                else:
                    response.message("Sorry about that! Please try again.")
                    action = None
                    state_params = None

                # Update fields after processing them
                updateField(number, 'action', None)
                updateField(number, 'state_params', None)
                updateField(number, 'ask_for', None)
                updateField(number, 'confirmed', False)

                print("CONFIRMED!")

                print(str(response))
                return str(response)

            if action == 'transactions':
                response.message("It looks like you're trying to view your recent transactions. Is this correct?")
            elif action == 'alerts':
                response.message("It looks like you're trying to view your alerts. Is this correct?")
            elif action == 'register':
                response.message("It sounds like you'd like to register for text alerts. Is this correct?")
            elif action == 'call':
                response.message("It sounds like you'd like to speak to customer support. Is this correct?")
            elif action == 'balance':
                response.message("It sounds like you're trying to check the balance of your " + state_params[
                    'account'] + " account. Is this correct?")
            elif action == 'transfer':
                response.message("It sounds like you're trying to transfer $" +
                                 round(Decimal(state_params["amount"]), 2) +
                                 " from " +
                                 state_params["origin"] +
                                 " to " +
                                 state_params["dest"] +
                                 ", is that correct?")
            elif action == 'find':
                locString = state_params['location'].replace(" Capital One", "")
                response.message("It sounds like you'd like to find " + locString + ", is that correct?")
            elif action == 'help':
                response.message('Don’t know where to start? Here’s everything you can do with our service:\nCheck '
                                 'your account balance\nView your recent transactions\nView your alerts\nTransfer '
                                 'money between your accounts\nTransfer money to an external account via phone '
                                 'number\nFind ATMs and Capital One banking locations nearby or in a location of your '
                                 'choice\nGet connected with a customer service representative\nSign up for text '
                                 'alerts related to your account')
                action = None
                state_params = None

            # Update fields after processing them
            updateField(number, 'confirmed', True)

        else:
            response.message(gen_response(action, state_params)[0])

    print(str(response))
    return (str(response))


if __name__ == '__main__':
    print('Running on port: {}'.format(os.environ.get('port')))
    app.run(port=int(os.environ.get('port')), debug=True)
