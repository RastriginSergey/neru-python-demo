from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from src.session.requestInterfaceForCallbacks import RequestInterfaceForCallbacks


#interface
class IVonageAI(ABC):
    @abstractmethod
    def analyze(self,analyze,callback):
        pass
    @abstractmethod
    def importModel(self,modelAssetName,callback):
        pass
