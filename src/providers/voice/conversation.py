from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from src.session.requestInterface import RequestInterface
from src.providers.vonageAPI.contracts.invokePayload import InvokePayload
from src.providers.voice.csEvents import CSEvents
from src.providers.voice.voiceActions import VoiceActions
from src.providers.vonageAPI.vonageAPI import VonageAPI
from src.session.filter import Filter
from src.session.actionPayload import ActionPayload
from src.providers.voice.IConversation import IConversation
from src.session.ISession import ISession
from src.providers.vonageAPI.IVonageAPI import IVonageAPI
from src.session.requestInterfaceForCallbacks import RequestInterfaceForCallbacks
from src.session.IFilter import IFilter
from src.providers.voice.contracts.transferMemberPayload import TransferMemberPayload
from src.providers.voice.contracts.sayStopPayload import SayStopPayload
from src.providers.voice.contracts.IPlayStreamBody import IPlayStreamBody
from src.providers.voice.contracts.playStreamPayload import PlayStreamPayload
from src.providers.voice.contracts.playStopPayload import PlayStopPayload
from src.providers.voice.contracts.reason import Reason
from src.providers.voice.contracts.deleteMemberPayload import DeleteMemberPayload
from src.providers.voice.contracts.ISayTextBody import ISayTextBody
from src.providers.voice.contracts.sayTextPayload import SayTextPayload
from src.providers.voice.contracts.earmuffPayload import EarmuffPayload
from src.providers.voice.contracts.audioSettings import AudioSettings
from src.providers.voice.contracts.media import Media
from src.providers.voice.contracts.IChannel import IChannel
from src.providers.voice.contracts.channel import Channel
from src.providers.voice.contracts.IAcceptInboundCallEvent import IAcceptInboundCallEvent
from src.providers.voice.contracts.acceptInboundCallPayload import AcceptInboundCallPayload
from src.providers.voice.contracts.inviteMemberPayload import InviteMemberPayload
from src.providers.voice.contracts.mutePayload import MutePayload
from src.providers.voice.contracts.neruPayloadWithCallback import NeruPayloadWithCallback
from src.providers.voice.contracts.addUserPayload import AddUserPayload
from src.session.IPayloadWithCallback import IPayloadWithCallback

@dataclass
class Conversation(IConversation):
    baseUrl: str
    vonageAPI: IVonageAPI
    session: ISession
    name: str
    id: str
    provider: str = field(default = "vonage-voice")
    def __init__(self,id,name,session):
        self.id = id
        self.name = name
        self.session = session
        self.vonageAPI = VonageAPI(self.session)
        self.baseUrl = "https://api.nexmo.com/v0.3"
    
    def acceptInboundCall(self,event):
        audioSettings = AudioSettings(True,False,False)
        media = Media(audioSettings,True)
        channel = Channel()
        channel.id = event.body.channel.id
        channel.type_ = event.body.channel.type_
        channel.to = event.body.channel.to
        channel.from_ = event.body.channel.from_
        payload = AcceptInboundCallPayload(event.body.user.id,event.from_,channel,media)
        url = f'{self.baseUrl}/conversations/{self.id}/members'
        method = "POST"
        return self.vonageAPI.invoke(url,method,payload)
    
    def inviteMember(self,name,channel):
        payload = InviteMemberPayload(name,channel)
        url = f'{self.baseUrl}/conversations/{self.id}/members'
        method = "POST"
        return self.vonageAPI.invoke(url,method,payload)
    
    def addUser(self,name):
        payload = AddUserPayload(name)
        url = f'{self.baseUrl}/users'
        method = "POST"
        return self.vonageAPI.invoke(url,method,payload)
    
    def transferMember(self,userId,legId):
        payload = TransferMemberPayload(userId,legId)
        url = f'{self.baseUrl}/conversations/{self.id}/members'
        method = "POST"
        return self.vonageAPI.invoke(url,method,payload)
    
    def deleteMember(self,memberId):
        reason = Reason("123","leaving conversation")
        payload = DeleteMemberPayload(reason)
        url = f'{self.baseUrl}/conversations/{self.id}/members/{memberId}'
        method = f'PATCH'
        return self.vonageAPI.invoke(url,method,payload)
    
    def sayText(self,params):
        payload = SayTextPayload(params)
        method = "POST"
        url = f'{self.baseUrl}/conversations/{self.id}/events'
        return self.vonageAPI.invoke(url,method,payload)
    
    def sayStop(self,sayId,to = None):
        payload = SayStopPayload(sayId,to)
        url = f'{self.baseUrl}/conversations/{self.id}/events'
        method = "POST"
        return self.vonageAPI.invoke(url,method,payload)
    
    def playStream(self,body,to = None):
        payload = PlayStreamPayload(body,to)
        url = f'{self.baseUrl}/conversations/{self.id}/events'
        method = "POST"
        return self.vonageAPI.invoke(url,method,payload)
    
    def playStop(self,playId,to = None):
        payload = PlayStopPayload(playId,to)
        url = f'{self.baseUrl}/conversations/{self.id}/events'
        method = "POST"
        return self.vonageAPI.invoke(url,method,payload)
    
    def earmuff(self,enable,to,from_ = None):
        payload = EarmuffPayload(enable,to,from_)
        url = f'{self.baseUrl}/conversations/{self.id}/events'
        method = "POST"
        return self.vonageAPI.invoke(url,method,payload)
    
    def earmuffOn(self,to,from_ = None):
        return self.earmuff(True,to,from_)
    
    def earmuffOff(self,to,from_ = None):
        return self.earmuff(False,to,from_)
    
    def mute(self,enable,to,from_ = None):
        payload = MutePayload(enable,to,from_)
        url = f'{self.baseUrl}/conversations/{self.id}/events'
        method = "POST"
        return self.vonageAPI.invoke(url,method,payload)
    
    def muteOn(self,to,from_ = None):
        return self.mute(True,to,from_)
    
    def muteOff(self,to,from_ = None):
        return self.mute(False,to,from_)
    
    def listenForEvents(self,callback,filters):
        payload = NeruPayloadWithCallback(self.session.wrapCallback(callback,filters),self.id)
        action = ActionPayload(self.provider,VoiceActions.ConversationSubscribeEvent,payload)
        return RequestInterfaceForCallbacks(self.session,action)
    
    def onConversationCreated(self,callback):
        filters = [Filter("type","contains",[CSEvents.ConversationCreated]),Filter("body.name","contains",[self.name])]
        return self.listenForEvents(callback,filters)
    
    def onSay(self,callback):
        filters = [Filter("type","contains",[CSEvents.AudioSay]),Filter(f'conversation_id',f'contains',[self.id])]
        return self.listenForEvents(callback,filters)
    
    def onPlay(self,callback):
        filters = [Filter("type","contains",[CSEvents.AudioPlay]),Filter("conversation_id","contains",[self.id])]
        return self.listenForEvents(callback,filters)
    
    def onSayStop(self,callback):
        filters = [Filter("type","contains",[CSEvents.AudioSayStop]),Filter(f'conversation_id',f'contains',[self.id])]
        return self.listenForEvents(callback,filters)
    
    def onPlayStop(self,callback):
        filters = [Filter("type","contains",[CSEvents.AudioPlayStop]),Filter(f'conversation_id',f'contains',[self.id])]
        return self.listenForEvents(callback,filters)
    
    def onSayDone(self,callback):
        filters = [Filter("type","contains",[CSEvents.AudioSayDone]),Filter(f'conversation_id',f'contains',[self.id])]
        return self.listenForEvents(callback,filters)
    
    def onPlayDone(self,callback):
        filters = [Filter("type","contains",[CSEvents.AudioPlayDone]),Filter(f'conversation_id',f'contains',[self.id])]
        return self.listenForEvents(callback,filters)
    
    def onLegStatusUpdate(self,callback):
        filters = [Filter("type","contains",[CSEvents.LegStatusUpdate]),Filter(f'conversation_id',f'contains',[self.id])]
        return self.listenForEvents(callback,filters)
    
    def onMemberJoined(self,callback,memberName = None):
        filters = [Filter("type","contains",[CSEvents.MemberJoined]),Filter(f'conversation_id',f'contains',[self.id])]
        if memberName is not None:
            filters.append(Filter(f'body.user.name',f'contains',[memberName]))
        
        return self.listenForEvents(callback,filters)
    
    def onMemberInvited(self,callback,memberName = None):
        filters = [Filter("type","contains",[CSEvents.MemberInvited]),Filter(f'conversation_id',f'contains',[self.id])]
        if memberName is not None:
            filters.append(Filter("body.user.name","contains",[memberName]))
        
        return self.listenForEvents(callback,filters)
    
    def onMemberLeft(self,callback,memberName = None):
        filters = [Filter("type","contains",[CSEvents.MemberLeft]),Filter(f'conversation_id',f'contains',[self.id])]
        if memberName is not None:
            filters.append(Filter("body.user.name","contains",[memberName]))
        
        return self.listenForEvents(callback,filters)
    
    def onDTMF(self,callback):
        filters = [Filter("type","contains",[CSEvents.AudioDTMF]),Filter(f'conversation_id',f'contains',[self.id])]
        return self.listenForEvents(callback,filters)
    
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
