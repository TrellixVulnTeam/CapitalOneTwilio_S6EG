from flask import Flask, render_template, request
import os
from os.path import join, dirname
from dotenv import load_dotenv

app = Flask(__name__)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def handle():
    print(request.form['message'])
    return 'Success'


if __name__ == '__main__':
    print('Running on port: {}'.format(os.environ.get('port')))
    app.run(port=os.environ.get('port'))
