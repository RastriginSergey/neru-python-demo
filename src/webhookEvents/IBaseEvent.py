from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod



#interface
class IBaseEvent(ABC):
    channel:str
    message_uuid:str
    to:str
    from_:str
    timestamp:str
    client_ref:str
