from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from src.session.requestInterface import RequestInterface
from src.providers.vonageAPI.contracts.invokePayload import InvokePayload


#interface
class IVonageAPI(ABC):
    @abstractmethod
    def invoke(self,url,method,body):
        pass
