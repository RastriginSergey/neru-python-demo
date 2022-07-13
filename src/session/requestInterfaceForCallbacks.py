from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from src.session.IPayloadWithCallback import IPayloadWithCallback
from src.session.IActionPayload import IActionPayload
from src.session.ISession import ISession

@dataclass
class RequestInterfaceForCallbacks:
    action: IActionPayload[IPayloadWithCallback]
    session: ISession
    def __init__(self,session,action):
        self.session = session
        self.action = action
    
    async def execute(self):
        await self.session.executeAction(self.action)
        return self.action.payload.callback.id
    
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
