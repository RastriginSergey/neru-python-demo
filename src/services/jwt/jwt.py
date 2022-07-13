from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from src.services.jwt.jwtPayload import JWTPayload
from src.IBridge import IBridge
from src.services.config.IConfig import IConfig
from src.services.jwt.IJwt import IJWT

@dataclass
class JWT(IJWT):
    config: IConfig
    bridge: IBridge
    _token: str = field(default = None)
    ttl: int = field(default = 300)
    expiresIn: int = None
    def __init__(self,bridge,config):
        self.bridge = bridge
        self.config = config
    
    def getToken(self):
        try:
            if self._token is None or self.isExpired():
                self.updateToken()
            
            return self._token
        
        except Exception as e:
            raise Exception(f'Error verifying JWT: {e}')
        
    
    def updateToken(self):
        expiresIn = self.bridge.getSystemTime() + self.ttl
        self._token = self.mintToken(expiresIn)
        self.expiresIn = expiresIn
    
    def isExpired(self):
        nowInSeconds = self.bridge.getSystemTime()
        twentySeconds = 20
        twentySecondsAgoFromNow = nowInSeconds - twentySeconds
        return self.expiresIn >= twentySecondsAgoFromNow
    
    def mintToken(self,exp):
        now = self.bridge.getSystemTime()
        payload = JWTPayload()
        payload.api_account_id = self.config.apiAccountId
        payload.api_application_id = self.config.apiApplicationId
        payload.sub = self.config.instanceServiceName
        payload.iat = now
        payload.exp = exp
        return self.bridge.jwtSign(payload,self.config.privateKey,"RS256")
    
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
