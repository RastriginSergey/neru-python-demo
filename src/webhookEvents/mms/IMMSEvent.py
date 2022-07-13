from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from src.webhookEvents.IBaseEvent import IBaseEvent


#interface
class IMMSEvent(IBaseEvent):
    message_type:str
