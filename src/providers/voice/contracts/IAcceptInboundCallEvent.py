from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from src.providers.voice.contracts.IAcceptInboundCallBody import IAcceptInboundCallBody


#interface
class IAcceptInboundCallEvent(ABC):
    type_:str
    application_id:str
    timestamp:str
    params:Dict[str,str]
    body:IAcceptInboundCallBody
    from_:str
