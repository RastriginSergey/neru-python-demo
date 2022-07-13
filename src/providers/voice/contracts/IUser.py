from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod



#interface
class IUser(ABC):
    id:str
    name:str
