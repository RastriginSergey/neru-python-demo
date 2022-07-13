from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from src.IBridge import IBridge
from src.providers.logger.ILogContext import ILogContext
from src.request.RequestHeaders import RequestHeaders
from src.services.commandService.ICommandService import ICommandService
from src.services.config.IConfig import IConfig
from src.session.CommandHeaders import CommandHeaders
from src.session.IActionPayload import IActionPayload
from src.session.IFilter import IFilter
from src.session.wrappedCallback import WrappedCallback


#interface
class ISession(ABC):
    id:str
    commandService:ICommandService
    bridge:IBridge
    config:IConfig
    @abstractmethod
    def createUUID(self):
        pass
    @abstractmethod
    def getToken(self):
        pass
    @abstractmethod
    def log(self,level,message,context):
        pass
    @abstractmethod
    def wrapCallback(self,route,filters):
        pass
    @abstractmethod
    def constructCommandHeaders(self):
        pass
    @abstractmethod
    def constructRequestHeaders(self):
        pass
    @abstractmethod
    def executeAction(self,actionPayload):
        pass
