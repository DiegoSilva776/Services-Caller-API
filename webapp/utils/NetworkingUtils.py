# -*- coding: utf-8 -*-

import json

from models.Service import Service

'''
    NetworkingUtils is responsible for holding the external URLs and the default parameters 
    of each URL used by the API.
'''
class NetworkingUtils():

    def __init__(self):
        self.TAG = "NetworkingUtils"
        self.PATH_SERVICES_CONFIG_FILE = "config/services.json"
        self.HTML_PARSER = 'html.parser'
        self.ISO_DATA_DECODER = 'iso8859-15'
        self.TIMEOUT_CALL_SERVICE = 60
        self.MANDATORY_TERM_SUCCESS_STATUS_RESPONSE = "API"
        self.SERVICES = []

        self.initListServices()

    def initListServices(self):
        try:
            data = open(self.PATH_SERVICES_CONFIG_FILE).read()
            services = json.loads(data)

            for serviceFromList in services:
                service = Service()

                if "url" in serviceFromList:
                    service.url = serviceFromList["url"]

                if "name" in serviceFromList:
                    service.name = serviceFromList["name"]

                self.SERVICES.append(service)

        except Exception as e:
            print("{0}: Failed to initListServices: {1}".format(self.TAG, e))
