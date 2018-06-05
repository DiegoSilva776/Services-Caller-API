# -*- coding: utf-8 -*-

class Service():

    def __init__(self):
        self.name = ""
        self.url = ""
        self.msg = ""
        self.status = False
        self.verifiedAt = ""

    def getSerializable(self):
        serializableObject = {
            "name" : self.name,
            "url" : self.url,
            "msg" : self.msg,
            "status" : self.status,
            "verified_at" : self.verifiedAt
        }

        return serializableObject
