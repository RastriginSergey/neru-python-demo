from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from src.providers.voice.contracts.IChannel import IChannel
from src.providers.voice.contracts.IChannelEndpoint import IChannelEndpoint

@dataclass
class Channel(IChannel):
    type_: str
    id: str
    preanswer: bool = field(default = False)
    to: IChannelEndpoint = None
    from_: IChannelEndpoint = None
    headers: Dict[str,str] = None
    cpa: bool = None
    ring_timeout: int = None
    can_hear: List[str] = None
    can_speak: List[str] = None
    cpa_time: int = None
    max_length: int = None
    knocking_id: str = None
    content_hyphen_type: str = None
    def __init__(self):
        pass
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
