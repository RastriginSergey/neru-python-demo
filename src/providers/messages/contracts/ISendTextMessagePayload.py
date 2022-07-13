from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from src.providers.messages.contracts.ISendTextContent import ISendTextContent


#interface
class ISendTextMessagePayload(ABC):
    content:ISendTextContent
