from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from src.providers.scheduler.contracts.IIntervalParams import IIntervalParams
from src.session.IPayloadWithCallback import IPayloadWithCallback

T = TypeVar("T")


#interface
class IStartAtPayload(IPayloadWithCallback,Generic[T]):
    startAt:str
    interval:IIntervalParams
    payload:T
    id:str
