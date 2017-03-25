
import requests
from flask import Flask, render_template, request
import os
from twilio import twiml
from twilio.rest import TwilioRestClient
import urllib
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

client = TwilioRestClient(account=os.environ.get('accountSid'),
                          token=os.environ.get('authToken'))
app = Flask(__name__)


@app.route('/sms', methods=['POST'])
def inbound_sms():
    response = twiml.Response()
    response.message('Thank you for texting! Searching for your song now')

    song_title = urllib.parse.quote(request.form['Body'])

    from_number = request.form['From']
    to_number = request.form['To']

    client.calls.create(to=from_number, from_=to_number,
                        url='https://298d36bd.ngrok.io/call?track={}'
                        .format(song_title))
    return str(response)

@app.route('/call', methods=['POST'])
def outbound_call():
    song_title = request.args.get('track')
    track_url = get_track_url(song_title)

    response = twiml.Response()
    response.play(track_url)
    return str(response)

def get_track_url(song_title):
    spotify_url = 'https://api.spotify.com/v1/search'
    params = {'q': song_title, 'type': 'track'}

    spotify_response = requests.get(spotify_url, params=params).json()
    track_url = spotify_response['tracks']['items'][0]['preview_url']
    return track_url

if __name__ == '__main__':
    print('Running on port: {}'.format(os.environ.get('port')))
    app.run(port=int(os.environ.get('port')), debug=True)
