from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod



#interface
class ICreateConversationPayload(ABC):
    name:str
    display_name:str
