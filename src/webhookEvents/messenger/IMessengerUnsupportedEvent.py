from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from src.webhookEvents.messenger.IMessangerEvent import IMessengerEvent


#interface
class IMessengerUnsupportedEvent(IMessengerEvent):
    pass
