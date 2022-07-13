from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from src.IBridge import IBridge


#interface
class IConfig(ABC):
    bridge:IBridge
    instanceServiceName:str
    applicationId:str
    apiApplicationId:str
    apiAccountId:str
    instanceId:str
    privateKey:str
    debug:bool
    appUrl:str
    assetUrl:str
    namespace:str
    @abstractmethod
    def getExecutionUrl(self,func):
        pass
