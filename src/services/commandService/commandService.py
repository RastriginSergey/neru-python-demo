from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from src.IBridge import IBridge
from src.request.IRequestHeaders import IRequestHeaders
from src.request.requestMethods import RequestMethods
from src.request.requestParams import RequestParams
from src.services.commandService.ICommandService import ICommandService

@dataclass
class CommandService(ICommandService):
    bridge: IBridge
    def __init__(self,bridge):
        self.bridge = bridge
    
    async def executeCommand(self,url,data = None,headers = None):
        requestParams = RequestParams()
        requestParams.url = url
        requestParams.method = RequestMethods.POST
        if data is not None:
            requestParams.data = data
        
        if headers is not None:
            requestParams.headers = headers
        
        return await self.bridge.request(requestParams)
    
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
