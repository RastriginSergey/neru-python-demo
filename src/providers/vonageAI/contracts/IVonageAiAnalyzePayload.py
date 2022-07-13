from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from src.session.IPayloadWithCallback import IPayloadWithCallback


#interface
class IVonageAiAnalyzePayload(IPayloadWithCallback):
    analyze:str
