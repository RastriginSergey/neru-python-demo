from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from src.IBridge import IBridge
from src.request.requestMethods import RequestMethods
from src.request.requestParams import RequestParams
from src.services.config.IConfig import IConfig
from src.session.ISession import ISession
from src.providers.logger.ILogContext import ILogContext
from src.providers.logger.ILogger import ILogger
from src.providers.logger.logAction import LogAction
from src.providers.logger.sourceTypes import SourceTypes

@dataclass
class Logger(ILogger):
    url: str
    sessionId: str
    bridge: IBridge
    config: IConfig
    provider: str = field(default = "logs-submission")
    def __init__(self,session):
        self.config = session.config
        self.bridge = session.bridge
        self.sessionId = session.id
        self.url = self.config.getExecutionUrl(self.provider)
    
    def createLogAction(self,level,message,context = None):
        logAction = LogAction()
        logAction.id = self.sessionId
        logAction.api_application_id = self.config.apiApplicationId
        logAction.api_account_id = self.config.apiAccountId
        logAction.session_id = self.bridge.uuid()
        logAction.timestamp = self.bridge.isoDate()
        logAction.log_level = level
        logAction.message = message
        logAction.source_type = SourceTypes.application
        logAction.source_id = self.config.instanceServiceName
        logAction.instance_id = self.config.instanceId
        if context is not None:
            logAction.context = context
        
        return logAction
    
    async def log(self,level,message,context = None):
        logAction = self.createLogAction(level,message,context)
        if self.config.debug:
            self.bridge.log(logAction)
        
        requestParams = RequestParams()
        requestParams.method = RequestMethods.POST
        requestParams.url = self.config.getExecutionUrl("logs-submission")
        requestParams.data = logAction
        await self.bridge.requestWithoutResponse(requestParams)
    
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
