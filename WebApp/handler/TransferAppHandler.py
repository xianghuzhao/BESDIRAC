#!/usr/bin/env python
#-*- coding: utf-8 -*-

from WebAppDIRAC.Lib.WebHandler import WebHandler, WErr
from DIRAC.Core.DISET.RPCClient import RPCClient
import datetime

class TransferAppHandler(WebHandler):
    AUTH_PROPS = "authenticated"

    # = dataset management =
    # == list ==
    def web_datasetList(self):
        # use RPCClient
        transferRequest = RPCClient("Transfer/Dataset")
        condDict = {}
        orderby = []
        start = 0
        limit = 50
        res = transferRequest.showtotal(condDict)
        self.log.always(res)
        #  {'OK': True, 'rpcStub': (('Transfer/Dataset', {'skipCACheck': False, 'keepAliveLapse': 150, 'delegatedGroup': 'bes_user', 'delegatedDN': '/C=CN/O=HEP/OU=PHYS/O=IHEP/CN=Tian Yan', 'timeout': 600}), 'showtotal', ({},)), 'Value': 68L} 
        limit = res["Value"]

        res = transferRequest.show(condDict, orderby, start, limit)
        self.log.always(res)
        # {'OK': True, 
        #  'rpcStub': (('Transfer/Dataset', {'delegatedDN': '/C=CN/O=HEP/OU=PHYS/O=IHEP/CN=Tian Yan', 'timeout': 600, 'skipCACheck': False, 'keepAliveLapse': 150, 'delegatedGroup': 'bes_user'}), 'show', ({}, [], 0, 68L)), 
        #  'Value': (
        #            (1L, 'my-dataset', 'lintao'), 
        #            (2L, 'jpsi-test', 'besdirac02.ihep.ac.cn'), 
        #            (3L, 'jpsi-test-10', 'besdirac02.ihep.ac.cn'), 
        #           )
        # } 
        data = []
        if res["OK"]:
            for id, dataset, owner in res["Value"]:
                data.append({
                    "id": id,
                    "owner": owner, 
                    "dataset": dataset,
                })
        self.write({"result": data})
    def web_datasetListFiles(self):
        self.log.debug(self.request.arguments)
        value = 0
        if self.request.arguments.get("datasetid", None):
            value = int(self.request.arguments["datasetid"][0])
        data = []
        for i in range(value):
            data.append({
                "id": i,
                "file": "/p/%d"%i,
            })
        self.write({"result": data})
    # == create ==
    # == delete ==

    # = transfer request (not including file list) =
    # == list ==
    def web_requestList(self):
        # create dummy data
        data = []
        for i in range(10):
            data.append({
                "id": i,
                "owner": "lintao", 
                "dataset": "lintao%d"%i,
                "srcSE": "IHEP-USER",
                "dstSE": "UCAS-USER",
                "protocol": "DMS", 
                "submitTime": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M [UTC]"),
                "status": "OK",
            })
        self.write({"result": data})

    # == new ==
    # create a new transfer request
    def web_requestNew(self):
        # validate
        # * dataset
        # * srcse
        # * dstse
        # * protocol
        self.log.debug(self.request.arguments)
        valid_list = ["dataset", "srcse", "dstse", "protocol"]
        build_input_param = {}
        for k in valid_list:
            if not self.request.arguments.has_key(k):
                raise WErr( 400, "Missing %s" % k )
            build_input_param[k] = self.request.arguments[k][0]
        self.log.debug(build_input_param)
        # check the data
        ## SE
        if build_input_param["dstse"] == build_input_param["srcse"]:
            raise WErr( 400, "dstse and srcse are same" )
        ## protocol
        if build_input_param["protocol"] not in ["DIRACDMS", "DIRACFTS"]:
            raise WErr( 400, "protocol %s is wrong"%build_input_param["protocol"] )

        self.set_status(200)
        self.finish()
        self.log.debug("finish")

    # = file list of one request =
    # == list ==
    def web_requestListFiles(self):
        self.log.debug(self.request.arguments)
        value = 0
        if self.request.arguments.get("reqid", None):
            value = int(self.request.arguments["reqid"][0])
        data = []
        for i in range(value):
            data.append({
                "id": i,
                "LFN": "/p/%d"%i,
                "starttime": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M [UTC]"),
                "finishtime": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M [UTC]"),
                "status": "OK",
                "error": "",
            })
        self.write({"result": data})


