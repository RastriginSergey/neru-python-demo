from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod



#interface
class IVapiEventParams(ABC):
    callback:str
    vapiUUID:str
    conversationID:str
