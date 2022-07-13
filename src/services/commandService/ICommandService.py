from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from src.request.IRequestHeaders import IRequestHeaders


#interface
class ICommandService(ABC):
    @abstractmethod
    def executeCommand(self,url,data = None,headers = None):
        pass
