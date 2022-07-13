from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from src.providers.messages.contracts.IMessageContact import IMessageContact
from src.providers.messages.contracts.ISendImageContent import ISendImageContent


#interface
class ISendImagePayload(ABC):
    from_:IMessageContact
    to:IMessageContact
    content:ISendImageContent
