# -*- coding: utf-8 -*-

from DIRAC import gLogger, gConfig, S_OK, S_ERROR
from DIRAC.Core.DISET.RequestHandler import RequestHandler

tmpGlobalStore = {}

def initializeTransferRequestHandler(serviceInfo):
  """ initialize handler """

  gLogger.info("Initialize TransferRequestHandler.")

  return S_OK()

class TransferRequestHandler(RequestHandler):
  """
  This is for:
    * create a request to transfer data
  """

  def initialize(self):
    credDict = self.getRemoteCredentials()
    gLogger.info(credDict)
    self.user = credDict["username"]

    tmpGlobalStore.setdefault( self.user, 
                              {"endpoint":{}
                              } )

  types_serverIsOK = []
  def export_serverIsOK(self):
    return S_OK()

  types_getEndPoint = []
  def export_getEndPoint(self):
    ep = tmpGlobalStore[self.user]["endpoint"]

    return S_OK( ep )

  types_setEndPoint = [str, str]
  def export_setEndPoint(self, name, url):
    gLogger.info(name)
    gLogger.info(url)

    tmpGlobalStore[self.user]["endpoint"][name] = url

    return S_OK()

  types_create = [ list, str, str ]
  def export_create(self, filelist, ep_from, ep_to):
    gLogger.info(filelist)
    gLogger.info(ep_from)
    gLogger.info(ep_to)
    return S_OK()