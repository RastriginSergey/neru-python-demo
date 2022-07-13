from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from src.providers.voice.contracts.ISayTextBody import ISayTextBody


#interface
class ISayTextPayload(ABC):
    type_:str
    body:ISayTextBody
