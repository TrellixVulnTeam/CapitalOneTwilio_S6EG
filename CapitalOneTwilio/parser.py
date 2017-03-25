from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier

with open('training.json', 'r') as fp:
    cl = NaiveBayesClassifier(fp, format="json")

