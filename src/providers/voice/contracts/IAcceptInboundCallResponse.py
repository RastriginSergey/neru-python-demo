from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from src.providers.voice.contracts.ICallTimestamp import ICallTimestamp
from src.providers.voice.contracts.IAcceptInboundCallChannel import IAcceptInboundCallChannel


#interface
class IAcceptInboundCallResponse(ABC):
    id:str
    user_id:str
    state:str
    timestamp:ICallTimestamp
    channel:IAcceptInboundCallChannel
    href:str
