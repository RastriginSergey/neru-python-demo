from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from src.providers.voice.contracts.IEarmuffPayload import IEarmuffPayload
from src.providers.voice.csEvents import CSEvents

@dataclass
class EarmuffPayload(IEarmuffPayload):
    to: str
    type_: str
    from_: str = None
    def __init__(self,enable,to,from_ = None):
        if enable:
            self.type_ = CSEvents.EarmuffOn
        
        else: 
            self.type_ = CSEvents.EarmuffOff
        
        self.to = to
        if from_ is not None:
            self.from_ = from_
        
    
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
