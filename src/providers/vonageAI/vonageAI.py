from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from src.providers.vonageAI.vonageAIActions import VonageAIActions
from src.session.actionPayload import ActionPayload
from src.providers.vonageAI.IVonageAI import IVonageAI
from src.session.ISession import ISession
from src.session.requestInterfaceForCallbacks import RequestInterfaceForCallbacks
from src.providers.vonageAI.contracts.vonageAiAnalyzePayload import VonageAiAnalyzePayload
from src.providers.vonageAI.contracts.importPayload import ImportPayload
from src.providers.vonageAI.contracts.vonageAiImportModelPayload import VonageAiImportModelPayload
from src.session.IPayloadWithCallback import IPayloadWithCallback

@dataclass
class VonageAI(IVonageAI):
    session: ISession
    provider: str = field(default = "vonage-overai")
    def __init__(self,session):
        self.session = session
    
    def analyze(self,analyze,callback):
        payload = VonageAiAnalyzePayload(analyze,self.session.wrapCallback(callback,[]))
        action = ActionPayload(self.provider,VonageAIActions.Analyze,payload)
        return RequestInterfaceForCallbacks(self.session,action)
    
    def importModel(self,modelAssetName,callback):
        modelAsset = ImportPayload(modelAssetName)
        wrappedCallback = self.session.wrapCallback(callback,[])
        payload = VonageAiImportModelPayload(modelAsset,wrappedCallback)
        action = ActionPayload(self.provider,VonageAIActions.ImportModel,payload)
        return RequestInterfaceForCallbacks(self.session,action)
    
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
