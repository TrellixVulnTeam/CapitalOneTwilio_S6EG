/**
 * Created by ashwin on 3/25/17.
 */
const express = require('express');
const app = express();
const bodyParser = require('body-parser');
const config = require('./config');
const twilio = require('twilio')(config.accountSid, config.authToken);
const twil = require('./twilioClient');
const nessie = require('nessie-nodejs-sdk');
const firebase = require('firebase');
var natural = require('natural'),
    stemmer = natural.LancasterStemmer,
    classifier = new natural.BayesClassifier(stemmer);

//NLP Training
classifier.addDocument("Check checking balance", 'balance');
classifier.addDocument("Check my checking balance.", 'balance');
classifier.addDocument("View my checking balance", 'balance');
classifier.addDocument("What is my checking balance?.", 'balance');
classifier.addDocument("Check savings balance", 'balance');
classifier.addDocument("Check my savings balance", 'balance');
classifier.addDocument("View my savings balance.", 'balance');
classifier.addDocument("What is my savings balance?", 'balance');
classifier.addDocument("What is my balance?", 'balance');
classifier.addDocument("Check my balance", 'balance');
classifier.addDocument("View my balance?", 'balance');
classifier.addDocument("Balance", 'balance');

classifier.addDocument("Check recent transactions", 'transactions');
classifier.addDocument("View recent transactions", 'transactions');
classifier.addDocument("Recent transactions", 'transactions');
classifier.addDocument("Check my transactions", 'transactions');
classifier.addDocument("View my transactions", 'transactions');
classifier.addDocument("What are my recent transactions?", 'transactions');
classifier.addDocument("My transactions", 'transactions');
classifier.addDocument("Transactions", 'transactions');

classifier.addDocument("Check recent alerts", 'alerts');
classifier.addDocument("View recent alerts", 'alerts');
classifier.addDocument("Recent alerts", 'alerts');
classifier.addDocument("Check my alerts", 'alerts');
classifier.addDocument("View my alerts", 'alerts');
classifier.addDocument("What are my recent alerts?", 'alerts');
classifier.addDocument("My alerts", 'alerts');
classifier.addDocument("Alerts", 'alerts');

classifier.addDocument("Transfer $50 from Checking to Savings", 'transfer');
classifier.addDocument("Transfer $20.33 from Savings to Checking", 'transfer');
classifier.addDocument("Send $100 from Checking to Savings", 'transfer');
classifier.addDocument("Transfer $50 to Checking from Savings", 'transfer');
classifier.addDocument("Send $300.00 to Savings from Checking", 'transfer');
classifier.addDocument("Transfer", 'transfer');

classifier.addDocument("Find ATMs nearby", 'find');
classifier.addDocument("Find ATMs near me", 'find');
classifier.addDocument("Find ATMs near Ann Arbor", 'find');
classifier.addDocument("Find ATMs in New York", 'find');
classifier.addDocument("Find atms nearby", 'find');
classifier.addDocument("Find atms nearby", 'find');
classifier.addDocument("Where are ATMs nearby?", 'find');
classifier.addDocument("Where are ATMs in Cleveland?", 'find');
classifier.addDocument("Are there any ATMs near me?", 'find');
classifier.addDocument("Find", 'find');

classifier.addDocument("Deposit check", 'deposit');
classifier.addDocument("Check deposit", 'deposit');
classifier.addDocument("Deposit", 'deposit');
classifier.addDocument("Deposit a check", 'deposit');
classifier.addDocument("Deposit my check", 'deposit');

classifier.addDocument("Call a representative", 'call');
classifier.addDocument("Call an agent", 'call');
classifier.addDocument("Call customer support", 'call');
classifier.addDocument("Call support", 'call');
classifier.addDocument("Contact a representative", 'call');
classifier.addDocument("Contact customer support", 'call');
classifier.addDocument("Call Billing", 'call');

classifier.addDocument("Sign up for text alerts", 'register');
classifier.addDocument("Sign up for email alerts", 'register');
classifier.addDocument("Sign up for phone alerts", 'register');
classifier.addDocument("register for text alerts", 'register');
classifier.addDocument("register for email alerts", 'register');

classifier.addDocument("Help", 'help');
classifier.addDocument("Help me", 'help');
classifier.addDocument("Help", 'help');


classifier.train();
// Set up Nessie
nessie.setApiKey(config.apiKey);

// parse application/x-www-form-urlencoded
app.use(bodyParser.urlencoded({extended: false}));

// parse application/json
app.use(bodyParser.json());


app.set('port', process.env.PORT || 3000);

app.get('/', (req, res) => {
    res.send('Hello World!');
});

app.post('/send', (req, res) => {
    twil.sendSms(config.sendingNumber, req.body.message);
    console.log(req.body.message);
    res.send('hello');
});

app.listen(3000, () => {
    console.log(`App Running on port ${app.get('port')}`);
    console.log(nessie.account.getAll()._multipart.body);
});

