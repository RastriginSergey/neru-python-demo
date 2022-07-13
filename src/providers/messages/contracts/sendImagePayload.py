from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from src.providers.messages.contracts.ISendImagePayload import ISendImagePayload
from src.providers.messages.contracts.IMessageContact import IMessageContact
from src.providers.messages.contracts.ISendImageContent import ISendImageContent

@dataclass
class SendImagePayload(ISendImagePayload):
    content: ISendImageContent
    to: IMessageContact
    from_: IMessageContact
    def __init__(self,from_,to,content):
        self.from_ = from_
        self.to = to
        self.content = content
    
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
