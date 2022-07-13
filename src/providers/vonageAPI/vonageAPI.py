from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from src.session.requestInterface import RequestInterface
from src.providers.vonageAPI.vonageAPIActions import VonageAPIActions
from src.session.actionPayload import ActionPayload
from src.providers.vonageAPI.IVonageAPI import IVonageAPI
from src.session.ISession import ISession
from src.providers.vonageAPI.contracts.invokePayload import InvokePayload

@dataclass
class VonageAPI(IVonageAPI):
    session: ISession
    provider: str = field(default = "vonage-api")
    def __init__(self,session):
        self.session = session
    
    def invoke(self,url,method,body):
        payload = InvokePayload(url,method,body)
        action = ActionPayload(self.provider,VonageAPIActions.Invoke,payload)
        return RequestInterface(self.session,action)
    
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
