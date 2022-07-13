from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from src.providers.state.IStateCommand import IStateCommand
from src.providers.state.stateCommand import StateCommand


#interface
class IState(ABC):
    @abstractmethod
    def createCommand(self,op,key,args):
        pass
    @abstractmethod
    def executeCommand(self,command):
        pass
    @abstractmethod
    def set(self,key,value):
        pass
    @abstractmethod
    def get(self,key):
        pass
    @abstractmethod
    def delete(self,key):
        pass
    @abstractmethod
    def hdel(self,htable,key):
        pass
    @abstractmethod
    def hexists(self,htable,key):
        pass
    @abstractmethod
    def hgetall(self,htable):
        pass
    @abstractmethod
    def hmget(self,htable,keys):
        pass
    @abstractmethod
    def hvals(self,htable):
        pass
    @abstractmethod
    def hget(self,htable,key):
        pass
    @abstractmethod
    def hset(self,htable,keyValuePairs):
        pass
    @abstractmethod
    def rpush(self,list,value):
        pass
    @abstractmethod
    def lpush(self,list,value):
        pass
    @abstractmethod
    def llen(self,list):
        pass
    @abstractmethod
    def lrange(self,list,startPos,endPos):
        pass
