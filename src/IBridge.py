from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from src.request.requestParams import RequestParams
from src.services.jwt.jwtPayload import JWTPayload
from src.providers.logger.ILogAction import ILogAction


#interface
class IBridge(ABC):
    @abstractmethod
    def substring(self,str,start,end = None):
        pass
    @abstractmethod
    def jsonStringify(self,data):
        pass
    @abstractmethod
    def jsonParse(self,json):
        pass
    @abstractmethod
    def getEnv(self,name):
        pass
    @abstractmethod
    def request(self,params):
        pass
    @abstractmethod
    def requestWithoutResponse(self,params):
        pass
    @abstractmethod
    def uuid(self):
        pass
    @abstractmethod
    def isoDate(self):
        pass
    @abstractmethod
    def jwtSign(self,payload,privateKey,algorithm):
        pass
    @abstractmethod
    def jwtVerify(self,token,privateKey,algorithm):
        pass
    @abstractmethod
    def getSystemTime(self):
        pass
    @abstractmethod
    def log(self,logAction):
        pass
    @abstractmethod
    def getObjectKeys(self,obj):
        pass
    @abstractmethod
    def getRouter(self):
        pass
