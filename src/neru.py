from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from src.session.neruSession import NeruSession
from src.IBridge import IBridge
from src.services.config.IConfig import IConfig
from src.services.jwt.jwt import JWT
from src.bridge import Bridge
from src.services.config.config import Config
from src.request.IRequest import IRequest
from src.providers.state.state import State
from src.services.jwt.IJwt import IJWT
from src.session.ISession import ISession
from src.INeru import INeru
from src.providers.state.IState import IState
from src.services.commandService.ICommandService import ICommandService
from src.services.commandService.commandService import CommandService

@dataclass
class Neru(INeru):
    commandService: ICommandService
    jwt: IJWT
    config: IConfig
    bridge: IBridge
    def __init__(self):
        self.bridge = Bridge()
        self.config = Config(self.bridge)
        self.jwt = JWT(self.bridge,self.config)
        self.commandService = CommandService(self.bridge)
    
    def createSession(self):
        id = self.bridge.uuid()
        return self.createSessionWithId(id)
    
    def createSessionWithId(self,id):
        return NeruSession(self.commandService,self.bridge,self.config,self.jwt,id)
    
    def getSessionById(self,id):
        if id is None:
            raise Exception("id is required")
        
        return self.createSessionWithId(id)
    
    def Router(self):
        return self.bridge.getRouter()
    
    def getAppUrl(self):
        return self.config.appUrl
    
    def getSessionFromRequest(self,req):
        if req is None:
            raise Exception("getSessionFromRequest: function requires request object to be provided")
        
        if req.headers is None:
            raise Exception("getSessionFromRequest: invalid request object proivided")
        
        id = req.headers["x-neru-sessionid"]
        if id is None:
            raise Exception(f'getSessionFromRequest: request does not contain \"x-neru-sessionid\" header')
        
        return self.getSessionById(id)
    
    def getGlobalState(self):
        id = f'application:{self.config.applicationId}'
        session = self.createSessionWithId(id)
        return State(session,f'application:{self.config.instanceServiceName}')
    
    def reprJSON(self):
        dict = {}
        keywordsMap = {"from_":"from","del_":"del","import_":"import","type_":"type"}
        for key in self.__dict__:
            val = self.__dict__[key]

            if type(val) is list:
                parsedList = []
                for i in val:
                    if hasattr(i,'reprJSON'):
                        parsedList.append(i.reprJSON())
                    else:
                        parsedList.append(i)
                val = parsedList

            if hasattr(val,'reprJSON'):
                val = val.reprJSON()
            if key in keywordsMap:
                key = keywordsMap[key]
            dict.__setitem__(key.replace('_hyphen_', '-'), val)
        return dict
