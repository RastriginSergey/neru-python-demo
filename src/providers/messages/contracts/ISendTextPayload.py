from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from src.providers.messages.contracts.IMessageContact import IMessageContact
from src.providers.messages.contracts.ISendTextMessagePayload import ISendTextMessagePayload


#interface
class ISendTextPayload(ABC):
    from_:IMessageContact
    to:IMessageContact
    message:ISendTextMessagePayload
