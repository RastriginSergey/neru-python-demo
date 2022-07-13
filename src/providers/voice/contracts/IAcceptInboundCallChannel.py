from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from src.providers.voice.contracts.IAcceptInboundCallEndpoint import IAcceptInboundCallEndpoint
from src.providers.voice.contracts.ILegId import ILegId


#interface
class IAcceptInboundCallChannel(ABC):
    type_:str
    leg_id:str
    from_:IAcceptInboundCallEndpoint
    to:IAcceptInboundCallEndpoint
    leg_ids:List[ILegId]
