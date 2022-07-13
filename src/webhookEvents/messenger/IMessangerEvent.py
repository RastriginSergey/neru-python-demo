from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from src.webhookEvents.IBaseEvent import IBaseEvent


#interface
class IMessengerEvent(IBaseEvent):
    message_type:str
