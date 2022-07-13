from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from src.session.requestInterface import RequestInterface
from src.session.requestInterfaceForCallbacks import RequestInterfaceForCallbacks
from src.providers.vonageAPI.contracts.invokePayload import InvokePayload
from src.providers.voice.contracts.vapiCreateCallPayload import VapiCreateCallPayload
from src.providers.voice.conversation import Conversation
from src.providers.voice.contracts.IVapiEventParams import IVapiEventParams
from src.providers.voice.contracts.IPhoneContact import IPhoneContact
from src.providers.voice.contracts.IChannelPhoneEndpoint import IChannelPhoneEndpoint


#interface
class IVoice(ABC):
    @abstractmethod
    def onInboundCall(self,callback,to,from_ = None):
        pass
    @abstractmethod
    def createConversation(self,name = None,displayName = None):
        pass
    @abstractmethod
    def onVapiAnswer(self,callback):
        pass
    @abstractmethod
    def onVapiEvent(self,params):
        pass
    @abstractmethod
    def vapiCreateCall(self,from_,to,ncco):
        pass
    @abstractmethod
    def uploadNCCO(self,uuid,ncco):
        pass
    @abstractmethod
    def getConversation(self,id,name):
        pass
