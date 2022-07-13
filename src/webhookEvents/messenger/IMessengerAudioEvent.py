from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from src.webhookEvents.IUrlObject import IUrlObject
from src.webhookEvents.messenger.IMessangerEvent import IMessengerEvent


#interface
class IMessengerAudioEvent(IMessengerEvent):
    audio:IUrlObject
