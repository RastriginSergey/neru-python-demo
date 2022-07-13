from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from src.session.requestInterface import RequestInterface
from src.providers.vonageAPI.contracts.invokePayload import InvokePayload
from src.providers.voice.contracts.createConversationResponse import CreateConversationResponse
from src.providers.voice.conversation import Conversation
from src.providers.vonageAPI.vonageAPI import VonageAPI
from src.session.actionPayload import ActionPayload
from src.providers.voice.voiceActions import VoiceActions
from src.providers.voice.IVoice import IVoice
from src.session.requestInterfaceForCallbacks import RequestInterfaceForCallbacks
from src.session.ISession import ISession
from src.providers.vonageAPI.IVonageAPI import IVonageAPI
from src.providers.voice.contracts.IVapiEventParams import IVapiEventParams
from src.providers.voice.contracts.IPhoneContact import IPhoneContact
from src.providers.voice.contracts.createConversationPayload import CreateConversationPayload
from src.providers.voice.contracts.IChannelPhoneEndpoint import IChannelPhoneEndpoint
from src.providers.voice.contracts.vapiAnswerCallBack import VapiAnswerCallBack
from src.providers.voice.contracts.vapiEventCallBackPayload import VapiEventCallBackPayload
from src.providers.voice.contracts.IVapiCreateCallPayload import IVapiCreateCallPayload
from src.providers.voice.contracts.vapiCreateCallPayload import VapiCreateCallPayload
from src.providers.voice.contracts.onInboundCallPayload import OnInboundCallPayload
from src.IBridge import IBridge
from src.session.IPayloadWithCallback import IPayloadWithCallback

@dataclass
class Voice(IVoice):
    bridge: IBridge
    vonageApi: IVonageAPI
    session: ISession
    provider: str = field(default = "vonage-voice")
    regionURL: str = field(default = "https://api.nexmo.com")
    def __init__(self,session,regionURL = None):
        self.session = session
        self.bridge = session.bridge
        self.vonageApi = VonageAPI(self.session)
        if regionURL is not None:
            self.regionURL = regionURL
        
    
    def onInboundCall(self,callback,to,from_ = None):
        payload = OnInboundCallPayload(self.session.wrapCallback(callback,[]),to,from_)
        action = ActionPayload(self.provider,VoiceActions.ConversationSubscribeInboundCall,payload)
        return RequestInterfaceForCallbacks(self.session,action)
    
    async def createConversation(self,name = None,displayName = None):
        try:
            conversationName = name
            conversationDisplayName = displayName
            if name is None:
                conversationId = self.bridge.substring(self.session.createUUID(),0,5)
                conversationName = f'name_cs_{conversationId}'
            
            if displayName is None:
                conversationDisplayName = f'dn_{name};'
            
            payload = CreateConversationPayload(name,displayName)
            url = "https://api.nexmo.com/v0.3/conversations"
            method = "POST"
            res = await self.vonageApi.invoke(url,method,payload).execute()
            return Conversation(res.id,name,self.session)
        
        except Exception as err:
            raise Exception(err)
        
    
    def onVapiAnswer(self,callback):
        payload = VapiAnswerCallBack(self.session.wrapCallback(callback,[]))
        action = ActionPayload(self.provider,VoiceActions.VapiSubscribeInboundCall,payload)
        return RequestInterfaceForCallbacks(self.session,action)
    
    def onVapiEvent(self,params):
        payload = VapiEventCallBackPayload()
        payload.callback = self.session.wrapCallback(params.callback,[])
        if params.vapiUUID is not None:
            payload.vapiId = params.vapiUUID
        
        elif params.conversationID is not None:
            payload.conversationID = params.conversationID
        
        action = ActionPayload(self.provider,VoiceActions.VapiSubscribeEvent,payload)
        return RequestInterfaceForCallbacks(self.session,action)
    
    def vapiCreateCall(self,from_,to,ncco):
        vapiCreateCallPayload = VapiCreateCallPayload(from_,to,ncco)
        return self.vonageApi.invoke(f'{self.regionURL}/v1/calls',"POST",vapiCreateCallPayload)
    
    def uploadNCCO(self,uuid,ncco):
        return self.vonageApi.invoke(f'{self.regionURL}/v1/calls/{uuid}',"PUT",ncco)
    
    def getConversation(self,id,name):
        return Conversation(id,name,self.session)
    
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
