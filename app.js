/**
 * Created by ashwin on 3/25/17.
 */

var express = require('express');
var app = express();
var bodyParser = require('body-parser');
var config = require('./config');
var twilio = require('twilio')(config.accountSid, config.authToken);
var twil = require('./twilioClient');
var natural = require('natural')


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
});