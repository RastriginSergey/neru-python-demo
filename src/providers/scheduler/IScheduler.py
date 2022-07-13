from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from src.session.requestInterface import RequestInterface
from src.session.requestInterfaceForCallbacks import RequestInterfaceForCallbacks
from src.providers.scheduler.contracts.cancelSchedulePayload import CancelSchedulePayload
from src.providers.scheduler.contracts.IStartAtParams import IStartAtParams


#interface
class IScheduler(ABC):
    @abstractmethod
    def startAt(self,params):
        pass
    @abstractmethod
    def cancel(self,scheduleId):
        pass
