from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from src.providers.voice.contracts.ISayTextBody import ISayTextBody
from src.providers.voice.contracts.ISayTextParams import ISayTextParams

@dataclass
class SayTextBody(ISayTextBody):
    text: str
    level: int = None
    loop: int = None
    voice_name: str = None
    queue: bool = None
    ssml: bool = None
    language: str = None
    style: int = None
    def __init__(self,body):
        self.text = body.text
        if body.level is not None:
            self.level = body.level
        
        if body.loop is not None:
            self.loop = body.loop
        
        if body.voice_name is not None:
            self.voice_name = body.voice_name
        
        if body.queue is not None:
            self.queue = body.queue
        
        if body.ssml is not None:
            self.ssml = body.ssml
        
        if body.style is not None:
            self.style = body.style
        
        if body.language is not None:
            self.language = body.language
        
    
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
