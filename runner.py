import argparse
import json
import datastore

class Runner():
    def __init__(self, user=None):
        self.user = user

    def createUser(self, file):
        if file:
            with open(file) as f:
                self.user = json.load(f)


def parse_arguments():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-i", "--init",
                            help="Initialize with phone number",
                            required=False,
                            default=None,
                            action='store_true')


    # Creates a dictionary of keys = argument flag, and value = argument
    args = vars(arg_parser.parse_args())
    return args['init']

if __name__ == '__main__':
    args = parse_arguments()
    app = Runner(datastore.getUser(args))
    print(app.user)