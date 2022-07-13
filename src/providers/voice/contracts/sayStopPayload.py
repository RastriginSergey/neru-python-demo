from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from src.providers.voice.contracts.ISayStopPayload import ISayStopPayload
from src.providers.voice.csEvents import CSEvents
from src.providers.voice.contracts.ISayStopBody import ISayStopBody
from src.providers.voice.contracts.sayStopBody import SayStopBody

@dataclass
class SayStopPayload(ISayStopPayload):
    body: ISayStopBody
    type_: str
    to: str = None
    def __init__(self,sayId,to = None):
        self.type_ = CSEvents.AudioSayStop
        self.body = SayStopBody(sayId)
        if to is not None:
            self.to = to
        
    
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
