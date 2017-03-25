from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier

with open('training.json', 'r') as fp:
    cl = NaiveBayesClassifier(fp, format="json")

def preprocess(message):
    message = message.lower()
    return message
    
test = [("I want to talk to an agent.", 'call'),
        ("Transfer $65 from Checking to Savings", 'transfer'),
        ("Find ATMs near me", 'find'),
        ("What's my checking balance?", 'check')]

for line in test:
    line = preprocess(line)
    print(cl.classify(line[0]))

