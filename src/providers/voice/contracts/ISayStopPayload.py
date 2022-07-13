from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from src.providers.voice.contracts.ISayStopBody import ISayStopBody


#interface
class ISayStopPayload(ABC):
    type_:str
    body:ISayStopBody
    to:str
