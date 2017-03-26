from twilio.rest import TwilioRestClient

import os

client = TwilioRestClient(account=os.environ.get('accountSid'),
                          token=os.environ.get('authToken'))

client.messages.create(
    to="+15558675309",
    from_="+15017250604",
    body="This is the ship that made the Kessel Run in fourteen parsecs?",
)