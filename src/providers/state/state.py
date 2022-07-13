from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from src.IBridge import IBridge
from src.services.commandService.ICommandService import ICommandService
from src.session.ISession import ISession
from src.providers.state.IState import IState
from src.providers.state.IStateCommand import IStateCommand
from src.providers.state.stateCommand import StateCommand
from src.providers.state.stateOperations import StateOperations

@dataclass
class State(IState):
    commandService: ICommandService
    session: ISession
    bridge: IBridge
    url: str
    namespace: str
    provider: str = field(default = "client-persistence-api")
    def __init__(self,session,namespace):
        self.bridge = session.bridge
        self.url = session.config.getExecutionUrl(self.provider)
        self.namespace = namespace
        self.session = session
        self.commandService = session.commandService
    
    def createCommand(self,op,key,args):
        return StateCommand(op,self.namespace,key,args)
    
    async def executeCommand(self,command):
        return await self.commandService.executeCommand(self.url,command,self.session.constructRequestHeaders())
    
    async def set(self,key,value):
        payload = []
        payload.append(self.bridge.jsonStringify(value))
        command = self.createCommand(StateOperations.SET,key,payload)
        return await self.executeCommand(command)
    
    async def get(self,key):
        payload = []
        command = self.createCommand(StateOperations.GET,key,payload)
        result = await self.executeCommand(command)
        return self.bridge.jsonParse(result)
    
    async def delete(self,key):
        payload = []
        command = self.createCommand(StateOperations.DEL,key,payload)
        return await self.executeCommand(command)
    
    async def hdel(self,htable,key):
        payload = [key]
        command = self.createCommand(StateOperations.HDEL,htable,payload)
        return await self.executeCommand(command)
    
    async def hexists(self,htable,key):
        payload = [key]
        command = self.createCommand(StateOperations.HEXISTS,htable,payload)
        return await self.executeCommand(command)
    
    async def hgetall(self,htable):
        payload = []
        command = self.createCommand(StateOperations.HGETALL,htable,payload)
        response = await self.executeCommand(command)
        result = {}
        for i in range(0,response.count,2):
            result[response[i]] = self.bridge.jsonParse(response[i + 1])
        
        return result
    
    async def hmget(self,htable,keys):
        command = self.createCommand(StateOperations.HMGET,htable,keys)
        response = await self.executeCommand(command)
        result = []
        for i in range(0,response.count):
            result.append(self.bridge.jsonParse(response[i]))
        
        return result
    
    async def hvals(self,htable):
        payload = []
        command = self.createCommand(StateOperations.HVALS,htable,payload)
        response = await self.executeCommand(command)
        result = []
        for i in range(0,response.count):
            result.append(self.bridge.jsonParse(response[i]))
        
        return result
    
    async def hget(self,htable,key):
        payload = [key]
        command = self.createCommand(StateOperations.HGET,htable,payload)
        result = await self.executeCommand(command)
        return self.bridge.jsonParse(result)
    
    async def hset(self,htable,keyValuePairs):
        payload = []
        keys = self.bridge.getObjectKeys(keyValuePairs)
        for i in range(0,keys.count):
            payload.append(keys[i])
            payload.append(keyValuePairs[keys[i]])
        
        command = self.createCommand(StateOperations.HSET,htable,payload)
        return await self.executeCommand(command)
    
    async def rpush(self,list,value):
        payload = [self.bridge.jsonStringify(value)]
        command = self.createCommand(StateOperations.RPUSH,list,payload)
        return await self.executeCommand(command)
    
    async def lpush(self,list,value):
        payload = [self.bridge.jsonStringify(value)]
        command = self.createCommand(StateOperations.LPUSH,list,payload)
        return await self.executeCommand(command)
    
    async def llen(self,list):
        payload = []
        command = self.createCommand(StateOperations.LLEN,list,payload)
        return await self.executeCommand(command)
    
    async def lrange(self,list,startPos = 0,endPos = -1):
        args = [self.bridge.jsonStringify(startPos),self.bridge.jsonStringify(endPos)]
        command = self.createCommand(StateOperations.LRANGE,list,args)
        response = await self.executeCommand(command)
        result = []
        for i in range(0,response.count):
            result.append(self.bridge.jsonParse(response[i]))
        
        return result
    
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
