#!/usr/bin/env python

import argparse
from flask import Flask, request, redirect, url_for, render_template
from werkzeug import secure_filename
import ConfigParser
import os
import re
import sys
import ujson as json

DEBUG = True

# construct application object
app = Flask(__name__)
app.config.from_object(__name__)

def load_config(server_ini):
    P = ConfigParser.RawConfigParser()

    P.opionxform = str
    P.read(server_ini)

    CFG = {}
    for section in P.sections():
        CFG[section] = dict(P.items(section))

    for (k, v) in CFG['server'].iteritems():
        app.config[k] = v
    return CFG


def run(**kwargs):
    app.run(**kwargs)



@app.route('/p')
def process():
    if request.method == 'POST':
        filename = request.files['csvfile']


@app.route('/')
def index():
    '''Top-level web page'''
    return render_template('index.html')


# Main block
def process_arguments(args):

    parser = argparse.ArgumentParser(description='entrofy web server')

    parser.add_argument('-i',
                        '--ini',
                        dest='ini',
                        required=False,
                        type=str,
                        default='server.ini',
                        help='Path to server.ini file')

    parser.add_argument('-p',
                        '--port',
                        dest='port',
                        required=False,
                        type=int,
                        default=5000,
                        help='Port')

    parser.add_argument('--host',
                        dest='host',
                        required=False,
                        type=str,
                        default='0.0.0.0',
                        help='host')

    return vars(parser.parse_args(args))


if __name__ == '__main__':
    parameters = process_arguments(sys.argv[1:])

    CFG = load_config(parameters['ini'])

    port = parameters['port']

    if os.environ.get('ENV') == 'production':
        port = int(os.environ.get('PORT'))

    run(host=parameters['host'], port=port, debug=DEBUG, processes=3)
