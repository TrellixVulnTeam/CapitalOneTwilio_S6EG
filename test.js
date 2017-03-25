/**
 * Created by ashwin on 3/25/17.
 */
var request = require('request');

// Set the headers
var headers = {
    'User-Agent': 'Super Agent/0.0.1',
    'Content-Type': 'application/json'
};

// Configure the request
var options = {
    url: 'http://localhost:3000/send',
    method: 'POST',
    headers: headers,
    form: {'message': 'Success'}
};

// Start the request
request(options, function (error, response, body) {
    if (!error && response.statusCode == 200) {
        // Print out the response body
        console.log(body)
    }
});