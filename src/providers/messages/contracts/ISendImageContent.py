from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from src.providers.messages.contracts.IImageData import IImageData


#interface
class ISendImageContent(ABC):
    type_:str
    image:IImageData
