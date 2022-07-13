from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from src.providers.state.state import State
from src.request.IRequest import IRequest
from src.session.neruSession import NeruSession


#interface
class INeru(ABC):
    @abstractmethod
    def createSession(self):
        pass
    @abstractmethod
    def createSessionWithId(self,id):
        pass
    @abstractmethod
    def getSessionById(self,id):
        pass
    @abstractmethod
    def Router(self):
        pass
    @abstractmethod
    def getAppUrl(self):
        pass
    @abstractmethod
    def getSessionFromRequest(self,req):
        pass
    @abstractmethod
    def getGlobalState(self):
        pass
