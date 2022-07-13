from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from src.IBridge import IBridge
from src.providers.logger.ILogContext import ILogContext
from src.providers.logger.ILogger import ILogger
from src.providers.logger.logContext import LogContext
from src.providers.logger.logger import Logger
from src.providers.logger.logLevels import LogLevels
from src.request.RequestHeaders import RequestHeaders
from src.services.commandService.ICommandService import ICommandService
from src.services.config.IConfig import IConfig
from src.services.jwt.IJwt import IJWT
from src.session.command import Command
from src.session.CommandHeaders import CommandHeaders
from src.session.IActionPayload import IActionPayload
from src.session.ICommand import ICommand
from src.session.IFilter import IFilter
from src.session.ISession import ISession
from src.session.wrappedCallback import WrappedCallback

@dataclass
class NeruSession(ISession):
    commandService: ICommandService
    logger: ILogger
    bridge: IBridge
    jwt: IJWT
    config: IConfig
    id: str
    def __init__(self,commandService,bridge,config,jwt,id):
        self.commandService = commandService
        self.id = id
        self.bridge = bridge
        self.config = config
        self.jwt = jwt
        self.logger = Logger(self)
    
    def createUUID(self):
        return self.bridge.uuid()
    
    def getToken(self):
        if self.config.debug is not None:
            return None
        
        return self.jwt.getToken()
    
    async def log(self,level,message,context = None):
        try:
            await self.logger.log(level,message,context)
        
        except Exception as e:
            raise Exception("Error during sending logs:" + e)
        
    
    def wrapCallback(self,route,filters):
        wrappedCallback = WrappedCallback()
        wrappedCallback.filters = filters
        wrappedCallback.id = self.createUUID()
        wrappedCallback.instanceServiceName = self.config.instanceServiceName
        wrappedCallback.sessionId = self.id
        wrappedCallback.instanceId = self.config.instanceId
        wrappedCallback.path = route
        return wrappedCallback
    
    def constructCommandHeaders(self):
        commandHeaders = CommandHeaders()
        commandHeaders.traceId = self.createUUID()
        commandHeaders.instanceId = self.config.instanceId
        commandHeaders.sessionId = self.id
        commandHeaders.apiAccountId = self.config.apiAccountId
        commandHeaders.apiApplicationId = self.config.apiApplicationId
        commandHeaders.applicationName = self.config.instanceServiceName
        commandHeaders.applicationId = self.config.applicationId
        return commandHeaders
    
    def constructRequestHeaders(self):
        requestHeaders = RequestHeaders()
        requestHeaders.X_hyphen_Neru_hyphen_SessionId = self.id
        requestHeaders.X_hyphen_Neru_hyphen_ApiAccountId = self.config.apiAccountId
        requestHeaders.X_hyphen_Neru_hyphen_ApiApplicationId = self.config.apiApplicationId
        requestHeaders.X_hyphen_Neru_hyphen_InstanceId = self.config.instanceId
        requestHeaders.X_hyphen_Neru_hyphen_TraceId = self.bridge.uuid()
        token = self.getToken()
        if token is not None:
            requestHeaders.Authorization = f'Bearer {token}'
        
        return requestHeaders
    
    async def executeAction(self,actionPayload):
        try:
            commandHeaders = self.constructCommandHeaders()
            requestHeaders = self.constructRequestHeaders()
            payload = Command(commandHeaders,actionPayload)
            url = self.config.getExecutionUrl(actionPayload.provider)
            result = await self.commandService.executeCommand(url,payload,requestHeaders)
            context = LogContext(actionPayload.action,self.bridge.jsonStringify(actionPayload.payload),self.bridge.jsonStringify(result))
            await self.logger.log(LogLevels.info,f'Executing action: {actionPayload.action}, provider: {actionPayload.provider}',context)
            return result
        
        except Exception as e:
            context = LogContext(actionPayload.action,self.bridge.jsonStringify(actionPayload.payload),e)
            await self.log(LogLevels.error,f'Error while executing action: {actionPayload.action}, provider: {actionPayload.provider}',context)
            raise Exception(e)
        
    
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
