from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier
from parser import *
import re
from decimal import Decimal

need_amounts = ['transfer']
need_accounts = ['balance']

def handle_input(input_msg):
  action = cl.classify(input_msg)
  print("Action: "+action)
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
  handle_input(input())

money = '$6,150,593.22'
value = Decimal(re.sub(r'[^\d.]', '', money))
print(value)
