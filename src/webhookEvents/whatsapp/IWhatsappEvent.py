from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from src.webhookEvents.IBaseEvent import IBaseEvent
from src.webhookEvents.whatsapp.IProfileName import IProfileName
from src.webhookEvents.whatsapp.IMessageEventContext import IMessageEventContext


#interface
class IWhatsappEvent(IBaseEvent):
    profile:IProfileName
    context:IMessageEventContext
    provider_message:str
    message_type:str
