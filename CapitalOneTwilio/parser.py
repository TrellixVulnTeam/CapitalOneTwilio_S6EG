from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier
import re
from decimal import Decimal
import json

print("Loading...")

reqs = {
    'balance': {
        'account': {
            'missing_resp': 'Which account would you like to check?'
        }
    },
    'transactions':'',
    'alerts':'',
    'transfer': {
        'amount': {
            'missing_resp': "Please enter an amount to transfer."
        },
        'dest': {
            'missing_resp': 'Which account do you want to transfer to?'
        },
        'origin': {
            'missing_resp': 'Which account do you want to transfer from?'
        }
    },
    'find': {
        'facility':{
            'missing_resp': 'What are you looking for?'
        },
        'location': {
            'optional': True
        }
    },
    'call': '',
    'help': '',
    'register': ''
}

accounts = ['checking', 'savings']
facilities = ['atm', 'office', 'bank', 'location', 'store', 'capital one']

moneyregex = re.compile('|'.join([
    r'\$?(\d*\.\d{1,2})[^A-z]+',  # e.g., $.50, .50, $1.50, $.5, .5
    r'\$?(\d+)[^A-z]+',           # e.g., $500, $5, 500, 5
    r'\$(\d+\.?)[^A-z]+',         # e.g., $5.
]))

def preprocess(message):
    message = message.lower()
    return message

def classify(message):
    message = preprocess(message)
    return cl.classify(message)

with open('training.json', 'r') as fp:
    data = json.loads(fp.read())
    train = []
    for d in data:
        train.append((preprocess(d['text']), d['label']))
    cl = NaiveBayesClassifier(train)

def handle_input(input_msg, action=None, state_params=None, ask_for=None):
    print("INPUT: Action:", action, "Params:", state_params, "Asking for:", ask_for)
    if action is None:
        action = classify(input_msg)
    action_reqs = reqs[action]
    if state_params is None:
        state_params = dict()
    if action == 'balance':
        print("Checking Balance!")
        if ask_for in accounts:
            for account in accounts:
                if re.search(account, input_msg, re.IGNORECASE):
                    state_params[ask_for] = account
                    break
        else:
            for account in accounts:
                if re.search(account, input_msg, re.IGNORECASE):
                    state_params['account'] = account
                    print("found",account)
                    break
    elif action == 'transfer':
        print("Transferring!")
        if ask_for in ['origin','dest']:
            for account in accounts:
                if re.search(account, input_msg, re.IGNORECASE):
                    state_params[ask_for] = account
                    break
        elif ask_for == 'amount':
            amount_match = moneyregex.search(input_msg)
            if amount_match:
                state_params['amount'] = re.sub(r'[\$\s]*', '', amount_match.group(0))
        else:
            amount_match = moneyregex.search(input_msg)
            if amount_match:
                state_params['amount'] = re.sub(r'[\$\s]*', '', amount_match.group(0))
            dest_results = re.search(r"(to|from).+(checking|savings).+(to|from).+(checking|savings)", input_msg)
            if dest_results:
                if dest_results.group(1) is 'to':
                    state_params['dest'] = dest_results.group(2)
                    state_params['origin'] = dest_results.group(4)
                else:
                    state_params['origin'] = dest_results.group(2)
                    state_params['dest'] = dest_results.group(4)
    elif action == 'call':
        print("Calling!")
        state_params['call'] = "make call"
    elif action == 'help':
        print("Helping!")
        state_params['help'] = "get help"
    elif action == 'find':
        print("Finding!")
        if ask_for == "facility":
            for facility in facilities:
                if re.search(facility, input_msg, re.IGNORECASE):
                    state_params[ask_for] = facility
                    break
        else:
            for facility in facilities:
                if re.search(facility, input_msg, re.IGNORECASE):
                    state_params['facility'] = facility
                    state_params['location'] = input_msg + "Capital One"
    elif action == "transactions":
        print("Transacting!")
        state_params['transactions'] = "get transactions"
    elif action == "alerts":
        print("Alerting!")
        state_params['alerts'] = "get alerts"
    elif action == "register":
        print("Registering!")
        state_params['register'] = "register"
    print("OUTPUT: Action:", action, "Params:", state_params)
    return action, state_params

def gen_response(action, state_params):
    action_reqs = reqs[action]
    for param in action_reqs:
        if param not in state_params and 'optional' not in action_reqs[param]:
            return action_reqs[param]['missing_resp'], param

    return 'default response', None

action = None
state_params = None
ask_for = None

while(True):
    print("Ready for input: ")
    action, state_params = handle_input(input(), action, state_params, ask_for)
    response, ask_for = gen_response(action, state_params)
    if ask_for is None:
        if action == 'transactions':
            print("It looks like you're trying to view your recent transactions. Is this correct?")
        elif action == 'alerts':
            print("It looks like you're trying to view your alerts. Is this correct?")
        elif action == 'register':
            print("It sounds like you'd like to register for text alerts. Is this correct?")
        elif action == 'call':
            print("It sounds like you'd like to speak to customer support. Is this correct?")
        elif action == 'balance':
            print("It sounds like you're trying to check the balance of your ", 
            state_params['account'], " account. Is this correct?")
        elif action == 'transfer':
            print("It sounds like you're trying to transfer $", round(Decimal(state_params["amount"]), 2), " from ", 
            state_params["origin"], " to ", state_params["dest"], ", is that correct?")
        elif action == 'find':
            print("It sounds like you'd like to find a ", state_params["facility"], 
            " ", state_params["location"], ", is that correct?")
        action = None
        state_params = None
        
    else:
       print("Secretly, I want to know the", ask_for)
    print(response, "\n\n")