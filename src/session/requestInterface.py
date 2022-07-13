from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from src.session.ISession import ISession
from src.session.IActionPayload import IActionPayload

T = TypeVar("T")

@dataclass
class RequestInterface(Generic[T]):
    action: IActionPayload[T]
    session: ISession
    def __init__(self,session,action):
        self.session = session
        self.action = action
    
    def onSuccess(self,route):
        self.action.successCallback = self.session.wrapCallback(route,[])
        return self
    
    def onError(self,route):
        self.action.errorCallback = self.session.wrapCallback(route,[])
        return self
    
    async def execute(self):
        return await self.session.executeAction(self.action)
    
    async def executeWithNoResult(self):
        return await self.session.executeAction(self.action)
    
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
