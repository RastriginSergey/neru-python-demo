from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from src.providers.voice.contracts.IChannelSIPEndpoint import IChannelSIPEndpoint
from src.providers.voice.csChannelTypes import CSChannelTypes

@dataclass
class ChannelSIPEndpoint(IChannelSIPEndpoint):
    headers: Dict[str,str]
    uri: str
    type_: str
    username: str = None
    password: str = None
    def __init__(self,uri,headers,username = None,password = None):
        self.type_ = CSChannelTypes.SIP
        self.uri = uri
        self.headers = headers
        if username is not None:
            self.username = username
        
        if password is not None:
            self.password = password
        
    
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
