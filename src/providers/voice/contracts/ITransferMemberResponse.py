from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from src.providers.voice.contracts.IInviteMemberResponse import IInviteMemberResponse


#interface
class ITransferMemberResponse(IInviteMemberResponse):
    pass
