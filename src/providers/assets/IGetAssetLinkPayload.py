from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod



#interface
class IGetAssetLinkPayload(ABC):
    cmd:str
    path:str
    duration:str
