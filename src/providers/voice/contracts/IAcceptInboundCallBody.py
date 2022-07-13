from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from src.providers.voice.contracts.IUser import IUser
from src.providers.voice.contracts.IChannel import IChannel


#interface
class IAcceptInboundCallBody(ABC):
    user:IUser
    channel:IChannel
