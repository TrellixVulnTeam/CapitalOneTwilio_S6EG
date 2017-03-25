/**
 * Created by ashwin on 3/25/17.
 */
const config = require('./config');
const client = require('twilio')(config.accountSid, config.authToken);

module.exports.sendSms = function (to, message) {
    client.messages.create({
        body: message,
        to: config.toNumber,
        from: config.fromNumber
//  mediaUrl: imageUrl
    }, function (err, data) {
        if (err) {
            console.error('Could not notify administrator');
            console.error(err);
        } else {
            console.log('Administrator notified');
            console.log(data)
        }
    });
};