from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from src.providers.logger.ILogContext import ILogContext


#interface
class ILogger(ABC):
    @abstractmethod
    def log(self,level,message,context = None):
        pass
