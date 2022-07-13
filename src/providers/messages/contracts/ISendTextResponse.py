from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from src.providers.messages.contracts.ISendResponse import ISendResponse


#interface
class ISendTextResponse(ISendResponse):
    pass
