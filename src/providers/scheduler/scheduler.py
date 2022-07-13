from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from src.session.requestInterface import RequestInterface
from src.providers.scheduler.schedulerActions import SchedulerActions
from src.session.actionPayload import ActionPayload
from src.providers.scheduler.IScheduler import IScheduler
from src.providers.scheduler.contracts.startAtPayload import StartAtPayload
from src.providers.scheduler.contracts.cancelSchedulePayload import CancelSchedulePayload
from src.providers.scheduler.contracts.IStartAtParams import IStartAtParams
from src.session.ISession import ISession
from src.session.requestInterfaceForCallbacks import RequestInterfaceForCallbacks
from src.session.IPayloadWithCallback import IPayloadWithCallback

@dataclass
class Scheduler(IScheduler):
    session: ISession
    provider: str = field(default = "vonage-scheduler")
    def __init__(self,session):
        self.session = session
    
    def startAt(self,params):
        startAtPayload = StartAtPayload()
        startAtPayload.startAt = params.startAt
        startAtPayload.callback = self.session.wrapCallback(params.callback,[])
        if params.payload is not None:
            startAtPayload.payload = params.payload
        
        if params.interval is not None:
            startAtPayload.interval = params.interval
        
        if params.id is not None:
            startAtPayload.id = params.id
        
        action = ActionPayload(self.provider,SchedulerActions.create,startAtPayload)
        return RequestInterfaceForCallbacks(self.session,action)
    
    def cancel(self,scheduleId):
        payload = CancelSchedulePayload(scheduleId)
        action = ActionPayload(self.provider,SchedulerActions.Cancel,payload)
        return RequestInterface(self.session,action)
    
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
