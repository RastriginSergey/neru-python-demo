from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from src.session.requestInterface import RequestInterface
from src.session.requestInterfaceForCallbacks import RequestInterfaceForCallbacks
from src.providers.vonageAPI.contracts.invokePayload import InvokePayload
from src.providers.messages.contracts.IBaseMessage import IBaseMessage
from src.providers.messages.contracts.IMessageContact import IMessageContact
from src.providers.messages.contracts.ISendImageContent import ISendImageContent
from src.providers.messages.contracts.sendImagePayload import SendImagePayload
from src.providers.messages.contracts.sendTextPayload import SendTextPayload
from src.providers.messages.contracts.unsubscribeEventsPayload import UnsubscribeEventsPayload


#interface
class IMessages(ABC):
    @abstractmethod
    def send(self,message):
        pass
    @abstractmethod
    def sendText(self,from_,to,message):
        pass
    @abstractmethod
    def sendImage(self,from_,to,imageContent):
        pass
    @abstractmethod
    def listenMessages(self,from_,to,callback):
        pass
    @abstractmethod
    def listenEvents(self,from_,to,callback):
        pass
    @abstractmethod
    def onMessage(self,callback,from_,to):
        pass
    @abstractmethod
    def onMessageEvents(self,callback,from_,to):
        pass
    @abstractmethod
    def unsubscribeEvents(self,id):
        pass
