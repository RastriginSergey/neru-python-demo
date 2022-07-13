from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from src.providers.voice.contracts.IChannelEndpoint import IChannelEndpoint


#interface
class IChannelVBCEndpoint(IChannelEndpoint):
    extension:str
