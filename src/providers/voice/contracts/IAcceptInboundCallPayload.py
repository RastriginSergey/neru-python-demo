from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from src.providers.voice.contracts.IUser import IUser
from src.providers.voice.contracts.IChannel import IChannel
from src.providers.voice.contracts.IMedia import IMedia


#interface
class IAcceptInboundCallPayload(ABC):
    user:IUser
    knocking_id:str
    channel:IChannel
    state:str
    media:IMedia
