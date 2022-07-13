from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod



#interface
class IStateCommand(ABC):
    operation:str
    namespace:str
    key:str
    args:List[str]
