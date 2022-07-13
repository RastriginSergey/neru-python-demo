from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod



#interface
class IFilter(ABC):
    path:str
    op:str
    values:List[str]
