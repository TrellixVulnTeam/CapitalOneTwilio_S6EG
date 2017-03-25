from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier
import re
from decimal import Decimal
import json

with open('training.json', 'r') as fp:
    data = json.loads(fp.read())
    train = []
    for d in data:
        train.append( (d['text'].lower(), d['label']) )
    cl = NaiveBayesClassifier(train)

def preprocess(message):
    message = message.lower()
    return message

def classify(message):
    message = preprocess(message)
    return cl.classify(message)

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
        print("extract amount here")

while(True):
    print("Ready for input: ")
    handle_input(input())
    print("\n\n")

money = '$6,150,593.22'
value = Decimal(re.sub(r'[^\d.]', '', money))
print(value)