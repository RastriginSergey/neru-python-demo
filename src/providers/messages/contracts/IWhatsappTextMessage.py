from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from src.providers.messages.contracts.IBaseMessage import IBaseMessage


#interface
class IWhatsappTextMessage(IBaseMessage):
    text:str
