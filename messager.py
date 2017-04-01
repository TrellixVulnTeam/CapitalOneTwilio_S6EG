from twilio.rest import TwilioRestClient

import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)
client = TwilioRestClient(account=os.environ.get('accountSid'),
                          token=os.environ.get('authToken'))


client.messages.create(
    to=os.environ.get('fromNumber'),
    from_=os.environ.get('toNumber'),
    body="Checking",
)