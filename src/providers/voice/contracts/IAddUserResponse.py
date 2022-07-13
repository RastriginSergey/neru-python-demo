from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod



#interface
class IAddUserResponse(ABC):
    name:str
    display_name:str
