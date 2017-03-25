from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier

with open('training.json', 'r') as fp:
    cl = NaiveBayesClassifier(fp, format="json")

def preprocess(message):
    message = message.lower()
    return message

def classify(message):
    message = preprocess(message)
    cl.classify(message)

