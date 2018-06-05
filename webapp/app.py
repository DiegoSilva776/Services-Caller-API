# -*- coding: utf-8 -*-

import os

from flask import Flask
from flask import request

from celery import Celery
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
        return pingController.pingServices()

    except ValueError:
        return 'Failed to startCallingServices'

@app.route('/status/')
def returnStatusServices():
    try:
        return pingController.returnStatusServices()

    except ValueError:
        return 'Failed to returnStatusServices'

    return 'Started ServicesCaller API v0.0.1'

# Initilization
if __name__ == '__main__':
    app.run(host='0.0.0.0')
