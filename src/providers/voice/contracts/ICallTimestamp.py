from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod



#interface
class ICallTimestamp(ABC):
    invited:str
    joined:str
    left:str
