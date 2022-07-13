from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod



#interface
class IMutePayload(ABC):
    type_:str
    to:str
    from_:str
