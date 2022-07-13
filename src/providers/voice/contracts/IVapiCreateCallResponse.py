from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod



#interface
class IVapiCreateCallResponse(ABC):
    conversation_uuid:str
    direction:str
    status:str
    uuid:str
