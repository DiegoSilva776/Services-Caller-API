# -*- coding: utf-8 -*-

import os

from flask import Flask
from flask import request

from werkzeug.serving import WSGIRequestHandler
from controllers.PingController import PingController

# Construction
app = Flask(__name__)
pingController = PingController()

# Routing
@app.route('/')
def index():
    return 'Started ServicesCaller API v0.0.2'

@app.route('/start/')
def startCallingServices():
    try:
        key = request.headers.get("key")
        return pingController.pingServices(key)

    except ValueError as e:
        return 'Failed to startCallingServices {0}'.format(e)

    return "Started routine to call listed services"

@app.route('/status/')
def returnStatusServices():
    try:
        key = request.headers.get("key")
        return pingController.returnStatusServices(key)

    except ValueError as e:
        return 'Failed to returnStatusServices {0}'.format(e)

# Initilization
if __name__ == '__main__':
    app.run(host='0.0.0.0')
