# -*- coding: utf-8 -*-

import os

from flask import Flask
from flask import request

from celery import Celery
from werkzeug.serving import WSGIRequestHandler

from controllers.PingController import PingController

# Construction
app = Flask(__name__)

# Routing
@app.route('/')
def hello():
    return 'ServicesCaller API'

'''
    Endpoints used to scrap data from SIOPS and feed the database.
'''
@app.route('/ping_listed_services/')
def pingListedService():
    try:
        pingController = PingController()
        return pingController.pingServices()

    except ValueError:
        return 'Failed to pingListedService'

'''
    Initilization
'''
if __name__ == '__main__':
    app.run(host='0.0.0.0')
