from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from src.session.IFilter import IFilter
from src.session.requestInterface import RequestInterface
from src.session.requestInterfaceForCallbacks import RequestInterfaceForCallbacks
from src.providers.vonageAPI.contracts.invokePayload import InvokePayload
from src.providers.voice.contracts.acceptInboundCallPayload import AcceptInboundCallPayload
from src.providers.voice.contracts.addUserPayload import AddUserPayload
from src.providers.voice.contracts.deleteMemberPayload import DeleteMemberPayload
from src.providers.voice.contracts.earmuffPayload import EarmuffPayload
from src.providers.voice.contracts.IAcceptInboundCallEvent import IAcceptInboundCallEvent
from src.providers.voice.contracts.IChannel import IChannel
from src.providers.voice.contracts.inviteMemberPayload import InviteMemberPayload
from src.providers.voice.contracts.IPlayStreamBody import IPlayStreamBody
from src.providers.voice.contracts.ISayTextBody import ISayTextBody
from src.providers.voice.contracts.mutePayload import MutePayload
from src.providers.voice.contracts.playStopPayload import PlayStopPayload
from src.providers.voice.contracts.playStreamPayload import PlayStreamPayload
from src.providers.voice.contracts.sayStopPayload import SayStopPayload
from src.providers.voice.contracts.sayTextPayload import SayTextPayload
from src.providers.voice.contracts.transferMemberPayload import TransferMemberPayload


#interface
class IConversation(ABC):
    @abstractmethod
    def acceptInboundCall(self,event):
        pass
    @abstractmethod
    def inviteMember(self,name,channel):
        pass
    @abstractmethod
    def addUser(self,name):
        pass
    @abstractmethod
    def transferMember(self,userId,legId):
        pass
    @abstractmethod
    def deleteMember(self,memberId):
        pass
    @abstractmethod
    def sayText(self,body):
        pass
    @abstractmethod
    def sayStop(self,sayId,to = None):
        pass
    @abstractmethod
    def playStream(self,body,to = None):
        pass
    @abstractmethod
    def playStop(self,playId,to = None):
        pass
    @abstractmethod
    def earmuffOn(self,to,from_ = None):
        pass
    @abstractmethod
    def muteOn(self,to,from_ = None):
        pass
    @abstractmethod
    def listenForEvents(self,callback,filters):
        pass
    @abstractmethod
    def onConversationCreated(self,callback):
        pass
    @abstractmethod
    def onSay(self,callback):
        pass
    @abstractmethod
    def onPlay(self,callback):
        pass
    @abstractmethod
    def onSayStop(self,callback):
        pass
    @abstractmethod
    def onPlayStop(self,callback):
        pass
    @abstractmethod
    def onSayDone(self,callback):
        pass
    @abstractmethod
    def onPlayDone(self,callback):
        pass
    @abstractmethod
    def onLegStatusUpdate(self,callback):
        pass
    @abstractmethod
    def onMemberJoined(self,callback,memberName = None):
        pass
    @abstractmethod
    def onMemberInvited(self,callback,memberName = None):
        pass
    @abstractmethod
    def onMemberLeft(self,callback,memberName = None):
        pass
    @abstractmethod
    def onDTMF(self,callback):
        pass
