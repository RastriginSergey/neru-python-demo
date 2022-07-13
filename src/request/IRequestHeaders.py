from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod



#interface
class IRequestHeaders(ABC):
    X_hyphen_Neru_hyphen_TraceId:str
    X_hyphen_Neru_hyphen_ApiAccountId:str
    X_hyphen_Neru_hyphen_ApiApplicationId:str
    X_hyphen_Neru_hyphen_InstanceId:str
    X_hyphen_Neru_hyphen_SessionId:str
    Authorization:str
