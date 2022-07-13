from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from src.providers.scheduler.contracts.IUntilParams import IUntilParams


#interface
class IIntervalParams(ABC):
    cron:str
    until:IUntilParams
