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
            'missing_resp': 'Which account do you want to transfer to? Enter "Checking," "Savings," or a phone number.'
        },
        'origin': {
            'missing_resp': 'Which account do you want to transfer from? Enter "Checking" or "Savings."'
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
    'register': '',
    'confirmation': {
        'answer': {
            'missing_resp': 'Please enter yes or no (y/n).'
        }
    }
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
            local_dest = re.search(r"(to|from).+(checking|savings).+(to|from).+(checking|savings)", input_msg)
            ext_origin = re.search(r"from.+(checking|savings)", input_msg)
            ext_dest = re.search(r"to.+([+]1\d\d\d[-]?\d\d\d[-]?\d\d\d\d)$", input_msg)
            if local_dest:
                if local_dest.group(1) is 'to':
                    state_params['dest'] = local_dest.group(2)
                    state_params['origin'] = local_dest.group(4)
                else:
                    state_params['origin'] = local_dest.group(2)
                    state_params['dest'] = local_dest.group(4)
            elif ext_dest and ext_origin:
                state_params['origin'] = ext_origin.group(1)
                state_params['dest'] = ext_dest.group(1)
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
                    state_params['location'] = input_msg + " Capital One"
    elif action == "transactions":
        print("Transacting!")
        state_params['transactions'] = "get transactions"
    elif action == "alerts":
        print("Alerting!")
        state_params['alerts'] = "get alerts"
    elif action == "register":
        print("Registering!")
        state_params['register'] = "register"
    elif action == "confirmation":
        if input_msg == "yes" or input_msg == "y":
            state_params["answer"] = "y"
        elif input_msg == "no" or input_msg == "n":
            state_params["answer"] = "n"
        else:
            print("This should never happen.")
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
            state_params['location'] = state_params['location'].replace(" Capital One", "")
            print("It sounds like you'd like to find ", state_params["location"], ", is that correct?")
        elif action == 'help':
            #SEND HELP MESSAGE
            continue
        confirm = handle_input(input(), "confirmation", state_params, None)
        if state_params["answer"] == "y":
            #SEND ACTION
            print("Action confirmed!")
            action = None
            state_params = None
        else:
            print("Sorry about that!")
            state_params = None
            continue
        
    else:
       print("Secretly, I want to know the", ask_for)
    print(response, "\n\n")