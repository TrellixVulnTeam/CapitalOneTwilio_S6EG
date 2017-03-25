from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier
import re
from decimal import Decimal
import json


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
        train.append( (preprocess(d['text']), d['label']) )
    cl = NaiveBayesClassifier(train)

need_amounts = ['transfer']
need_accounts = ['balance']

def handle_input(input_msg):
    action = classify(input_msg)
    print("Action: ", action)
    if action in need_accounts:
        if re.search('checking', input_msg, re.IGNORECASE):
            print('this is for checking')
        elif re.search('savings', input_msg, re.IGNORECASE):
            print('this is for savings')
        else:
            print('Here, we respond with something like "Do you want to transfer to checking or savings?"')
    if action in need_amounts:
        money = re.compile('|'.join([
            r'\$?(\d*\.\d{1,2})\s',  # e.g., $.50, .50, $1.50, $.5, .5
            r'\$?(\d+)\s',           # e.g., $500, $5, 500, 5
            r'\$(\d+\.?)\s',         # e.g., $5.
        ]))
        amount_match = money.search(input_msg)
        if amount_match:
            amount = re.sub(r'\$', '', amount_match.group(0))
            print("Extracted amount: ", str(amount))
        else:
            print("No amount found")
        dest = ""
        origin = ""
        dest_results = re.search(r"(to|from).+(checking|savings).+(to|from).+(checking|savings)", input_msg)
        if dest_results:
            if dest_results.group(1) is 'to':
                dest = dest_results.group(2)
                origin = dest_results.group(4)
            else:
                dest = dest_results.group(4)
                origin = dest_results.group(2)
        else:
            print("no results found")
        print("Destination: ", dest, "\n", "Origin: ", origin)
while(True):
    print("Ready for input: ")
    handle_input(input())
    print("\n\n")