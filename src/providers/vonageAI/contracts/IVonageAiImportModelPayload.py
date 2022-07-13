from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from src.session.IPayloadWithCallback import IPayloadWithCallback
from src.providers.vonageAI.contracts.IImportPayload import IImportPayload


#interface
class IVonageAiImportModelPayload(IPayloadWithCallback):
    import_:IImportPayload
