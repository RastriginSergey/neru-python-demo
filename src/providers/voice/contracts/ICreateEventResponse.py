from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod



#interface
class ICreateEventResponse(ABC):
    id:str
    timestamp:str
    href:str
