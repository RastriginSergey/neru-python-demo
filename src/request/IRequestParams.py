from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from src.request.IRequestHeaders import IRequestHeaders

T = TypeVar("T")


#interface
class IRequestParams(ABC,Generic[T]):
    method:str
    url:str
    data:T
    headers:IRequestHeaders
