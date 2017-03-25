/**
 * Created by ashwin on 3/25/17.
 */
const express = require('express');
const app = express();
const bodyParser = require('body-parser');
const config = require('./config');
const twilio = require('twilio')(config.accountSid, config.authToken);
const twil = require('./twilioClient');
const natural = require('natural');
const nessie = require('nessie-nodejs-sdk');

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

