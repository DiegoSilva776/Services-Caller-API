# -*- coding: utf-8 -*-

import time
import datetime
import http.client
import urllib
import json

from requests_futures.sessions import FuturesSession
from utils.NetworkingUtils import NetworkingUtils
from utils.Logger import Logger

'''
    Make requests to the services
'''
class PingController():

    def __init__(self):
        self.TAG = "PingController"

        self.netUtils = NetworkingUtils()
        self.logUtils = Logger()
        self.session = FuturesSession()

    '''
        Make a request to verify if all the listed services are up and running
    '''
    def pingServices(self, key):
        response = {
            "msg" : "Failed to ping services"
        }

        try:

            if key == self.netUtils.key:

                for service in self.netUtils.services:
                    self.session.get(service.url, background_callback=self.parseAsyncResponse)

                    service.status = False
                    service.msg = ""

            else:
                response["msg"] = "{0}{1}".format(response["msg"], "Invalid key.")

        except urllib.error.HTTPError as httpe:
            print("{0}: Failed to pingService: {1}".format(self.TAG, httpe))

        except urllib.error.URLError as urle:
            print("{0}: Failed to pingService: {1}".format(self.TAG, urle))

        return "The pingServices process finished at {0}".format(datetime.datetime.utcnow())

    '''
        Process the response of the async request that was sent to the urls
    '''
    def parseAsyncResponse(self, session, response):

        if response is not None:

            if response.url is not None and response.content is not None:
                service = self.netUtils.getServiceByUrl(response.url)

                if service is not None:
                    service.msg = response.content.decode(self.netUtils.UTF8_DECODER)

                    if self.netUtils.MANDATORY_TERM_SUCCESS_STATUS_RESPONSE in service.msg:
                        service.status = True

                    service.verifiedAt = self.logUtils.get_utc_iso_timestamp()

                    print("\n{0}".format(json.dumps(service.getSerializable())))

    '''
        Return a list o the services with information about their current status and the last 
        time this controller tried to call them
    '''
    def returnStatusServices(self, key):
        response = {
            "msg" : "Failed to return the status of the services",
            "status_services" : []
        }

        try:

            if key == self.netUtils.key:
                print("The key is valid. Starting to make requests ...")

                for service in self.netUtils.services:
                    response["status_services"].append(service.getSerializable())

                response["msg"] = "Here is the status of the services listed in the configuration file."

            else:
                response["msg"] = "{0}. {1}".format(response["msg"], "Invalid key.")

        except Exception as e:
            print("{0}: Failed to returnStatusServices: {1}".format(self.TAG, e))

        return json.dumps(response)
