from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from src.session.IWrappedCallback import IWrappedCallback


#interface
class IPayloadWithCallback(ABC):
    callback:IWrappedCallback
