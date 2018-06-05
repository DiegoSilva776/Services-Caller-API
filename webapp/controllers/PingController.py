# -*- coding: utf-8 -*-

import time
import datetime
import http.client
import urllib
import json

from bs4 import BeautifulSoup

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

    '''
        Make a request to verify if all the listed services are up and running
    '''
    def pingServices(self):
        try:
            i = 1

            while i == 1:

                for service in self.netUtils.SERVICES:
                    service.status = False
                    service.msg = ""

                    # Make a request to get the HTML which contains the list of Cities of SIOPS
                    conn = http.client.HTTPConnection(service.url)
                    conn.request('GET', "", headers={
                        'cache-control': "no-cache"
                    })

                    # Process the response
                    res = conn.getresponse()
                    data = res.read()
                    service.msg = data.decode(self.netUtils.ISO_DATA_DECODER)

                    if service.msg is not None:

                        if self.netUtils.MANDATORY_TERM_SUCCESS_STATUS_RESPONSE in service.msg:
                            service.status = True

                    service.verifiedAt = self.logUtils.get_utc_iso_timestamp()

                time.sleep(self.netUtils.TIMEOUT_CALL_SERVICE)

        except urllib.error.HTTPError as httpe:
            print("{0}: Failed to pingService: {1}".format(self.TAG, httpe))

        except urllib.error.URLError as urle:
            print("{0}: Failed to pingService: {1}".format(self.TAG, urle))

        return "The pingServices process finished at {0}".format(datetime.datetime.utcnow())

    '''
        Return a list o the services with information about their current status and the last 
        time this controller tried to call them
    '''
    def returnStatusServices(self):
        response = {
            "msg" : "{0} Failed to return the status of the services".format(self.TAG),
            "status_services" : []
        }

        try:

            for service in self.netUtils.SERVICES:
                response["status_services"].append(service.getSerializable())

            response["msg"] = "Here is the status of the services listed in the configuration file."

        except Exception as e:
            response["msg"] = "{0} Failed to returnStatusServices : {1}".format(self.TAG, e)

        return json.dumps(response)