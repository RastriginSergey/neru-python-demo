from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod



#interface
class IAssets(ABC):
    @abstractmethod
    def getAssetLink(self,assetPath,duration):
        pass
