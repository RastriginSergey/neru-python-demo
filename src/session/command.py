from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from src.session.IActionPayload import IActionPayload
from src.session.ICommand import ICommand
from src.session.ICommandHeaders import ICommandHeaders

T = TypeVar("T")

@dataclass
class Command(ICommand,Generic[T]):
    actions: List[IActionPayload[T]]
    header: ICommandHeaders
    def __init__(self,headers,action):
        self.header = headers
        self.actions = [action]
    
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
