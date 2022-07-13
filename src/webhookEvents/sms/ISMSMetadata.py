from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod



#interface
class ISMSMetadata(ABC):
    num_messages:str
    keyword:str
