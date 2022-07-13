from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from src.request.IRequestHeaders import IRequestHeaders

@dataclass
class RequestHeaders(IRequestHeaders):
    X_hyphen_Neru_hyphen_SessionId: str
    X_hyphen_Neru_hyphen_InstanceId: str
    X_hyphen_Neru_hyphen_ApiApplicationId: str
    X_hyphen_Neru_hyphen_ApiAccountId: str
    X_hyphen_Neru_hyphen_TraceId: str
    Authorization: str = None
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
